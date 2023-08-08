from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from .serializers import FilteredUserSerializer, UserSerializer, SlideSerializer, RunSerializer
from .models import User, Slide, SlideImage, Run
from django.db.models import Q

from random import choice


# user views

@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    users_serialized = FilteredUserSerializer(users, many=True)
    return Response(data=users_serialized.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def loginUser(request):
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
def addUser(request):

    # FIXME: tirar isso
    request.data['username'] = request.data['username'].strip().lower()
    user = UserSerializer(data=request.data)

    if User.objects.filter(**request.data).exists():
        return Response(data={'error': "Username already in use"}, status=status.HTTP_201_CREATED)

    if user.is_valid():
        user.save()
        return Response(user.data, status=status.HTTP_201_CREATED)
    else:
        return Response(data={'error': "Invalid user fields"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def addMessageToUser(request, pk):

    try:
        user = User.objects.get(id=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    message = request.data['message'].strip()

    if len(message) > 200:
        return Response(data={'error': "Message is too long (>200 caracters)"}, status=status.HTTP_403_FORBIDDEN)

    logged_user = User.objects.get(username=request.user.username)
    if int(pk) != int(logged_user.id):
        return Response(data={'error': "User not allowed"}, status=status.HTTP_403_FORBIDDEN)

    user.message = message
    user.save()

    return Response(data=message)


# slide views

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getRandomSlide(request, pk):

    # slides = Slide.objects.all()
    # slide = choice(slides)

    slide = Slide.objects.get(
        prof_discipline="Matheus Schreiber | Tecnicas de Busca")  # FIXME: provisorio

    if not slide:
        return Response(data={'error': "No slides registered"}, status=status.HTTP_400_BAD_REQUEST)

    first_hint = SlideImage.objects.get(Q(slide=slide) & Q(hint_index=0))

    if not first_hint:
        return Response(data={'error': "No hints for this slide"}, status=status.HTTP_400_BAD_REQUEST)

    response = {
        "slide_provisory": slide.prof_discipline,  # FIXME: provisorio
        "slide_image_path": "/static/" + first_hint.image.name,
    }

    # if no run id is passed, then its the first slide
    if not pk:
        run = RunSerializer(data={
            "id_user": request.user.id,
            "current_hint": first_hint.id
        })

        if not run.is_valid():
            return Response(data={'error': "Invalid run creation"}, status=status.HTTP_400_BAD_REQUEST)

        run.save()
        response['run_id'] = run.id

    # if there is a run id, then append the new slide to it
    else:
        run = Run.objects.get(id=pk)

        if not run:
            return Response(data={'error': "Invalid run"}, status=status.HTTP_400_BAD_REQUEST)

        if run.slides_left == 0:
            return Response(data={'error': "Run finished"}, status=status.HTTP_400_BAD_REQUEST)

        run.current_hint = first_hint.id
        run.slides_left -= 1
        run.save()

        response['run_id'] = run.id

    return Response(data=response, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getHint(request, pk):
    run = Run.objects.get(id=pk)

    if not run:
        return Response(data={'error': "Invalid run"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(username=request.user.username)

    if not user or user.username != request.user.username:
        return Response(data={'error': "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

    current_hint = SlideImage.objects.get(id=run.current_hint.id)

    if not current_hint:
        return Response(data={'error': "Invalid slide image"}, status=status.HTTP_400_BAD_REQUEST)

    next_hint = SlideImage.objects.get(
        Q(slide=current_hint.slide) &
        Q(hint_index=current_hint.hint_index+1)
    )

    if not next_hint:
        return Response(data={'error': "No hints left"}, status=status.HTTP_400_BAD_REQUEST)

    user.hints_used += 1
    user.save()

    run.hints_used += 1
    run.save()

    slide = Slide.objects.get(id=current_hint.slide.id)

    if not slide:
        return Response(data={'error': "Invalid slide"}, status=status.HTTP_400_BAD_REQUEST)

    slide.hints_used += 1
    slide.save()

    response = {
        "slide_image_path": "/static/" + next_hint.image.name,
    }

    return Response(data=response, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getAnswerSlide(request, pk):
    run = Run.objects.get(id=pk)

    if not run:
        return Response(data={'error': "Invalid run"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(username=request.user.username)

    if not user or user.username != request.user.username:
        return Response(data={'error': "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

    current_hint = SlideImage.objects.get(id=run.current_hint)

    if not current_hint:
        return Response(data={'error': "Invalid slide image"}, status=status.HTTP_400_BAD_REQUEST)

    slide = Slide.objects.get(id=current_hint.slide.id)

    if not slide:
        return Response(data={'error': "Invalid slide"}, status=status.HTTP_400_BAD_REQUEST)

    slide_final = SlideImage.objects.get(
        Q(slide=slide) &
        Q(hint_index=slide.hints_amount-1)
    )

    if not slide_final:
        return Response(data={'error': "Invalid final slide"}, status=status.HTTP_400_BAD_REQUEST)

    if slide.prof_discipline == request.data['answer']:
        slide.hits += 1
        user.hits += 1
        run.hits += 1

        slide.save()
        user.save()
        run.save()

        return Response(data={"answer": True, "slide_image_path": slide_final}, status=status.HTTP_200_OK)

    else:
        slide.misses += 1
        user.misses += 1
        run.misses += 1

        slide.save()
        user.save()
        run.save()

        return Response(data={"answer": False, "slide_image_path": slide_final}, status=status.HTTP_200_OK)
