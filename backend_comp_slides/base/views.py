from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from .serializers import FilteredUserSerializer, UserSerializer, SlideSerializer, RunSerializer, SlideRunSerializer
from .models import User, Slide, SlideImage, Run, SlideRun
from django.db.models import Q

from random import choice


# extra views

@api_view(['GET'])
def getDisciplines(request):
    slides = Slide.objects.all().values_list('prof_discipline', flat=True)
    return Response(data=slides, status=status.HTTP_200_OK)


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

    if not request.data['username'] or not request.data['password']:
        return Response(data={'error': "Empty fields detected"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=request.data['username']).exists():
        return Response(data={'error': "Username already in use"}, status=status.HTTP_400_BAD_REQUEST)

    if len(request.data['password']) < 8:
        return Response(data={'error': "Password is too short"}, status=status.HTTP_400_BAD_REQUEST)

    hashed_password = make_password(request.data['password'])
    request.data['password'] = hashed_password

    user = UserSerializer(data=request.data)

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
def getRandomSlide(request, pk=None):
    try:
        # TODO: trocar isso para o certo
        slide = Slide.objects.order_by('?').first()
        first_hint = SlideImage.objects.get(
            Q(slide__id=slide.id) & Q(hint_index=0))

        response = {
            "slide_image_path": first_hint.image.name,
            "hints_amount": slide.hints_amount,
            "difficulty_level": slide.difficulty_level
        }

        # if no run id is passed, then its the first slide
        if not pk:
            # creating run
            run = RunSerializer(data={
                "id_user": request.user.id,
                "current_hint": first_hint.id
            })

            if not run.is_valid():
                return Response(data={'error': "Invalid run creation"}, status=status.HTTP_400_BAD_REQUEST)

            run = run.save()
            response['run_id'] = run.id
            response['slides_left_amount'] = run.slides_left

        # if there is a run id, then append the new slide to it
        else:
            run = Run.objects.get(id=pk)

            if run.slides_left == 0:
                return Response(data={'error': "Run finished"}, status=status.HTTP_400_BAD_REQUEST)

            run.current_hint = first_hint
            run.slides_left -= 1
            run.save()

            response['run_id'] = run.id
            response['slides_left_amount'] = run.slides_left

        # creating slide run associated to the slide and the run
        slide_run = SlideRunSerializer(data={
            "original_slide": slide.id,
            "run_id": run.id,
            "has_hit": False,
        })

        if not slide_run.is_valid():
            return Response(data={'error': "Invalid slide_run creation"}, status=status.HTTP_400_BAD_REQUEST)

        slide_run = slide_run.save()
        response['slide_run_id'] = slide_run.id

        return Response(data=response, status=status.HTTP_200_OK)

    except Run.DoesNotExist:
        return Response(data={'error': "Invalid run"}, status=status.HTTP_400_BAD_REQUEST)

    except SlideImage.DoesNotExist:
        return Response(data={'error': "Invalid hint"}, status=status.HTTP_400_BAD_REQUEST)

    except Slide.DoesNotExist:
        return Response(data={'error': "Invalid slide"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getHint(request, pk):
    try:
        run = Run.objects.get(id=pk)
        user = User.objects.get(username=run.id_user)

        if not user or user.username != request.user.username:
            raise User.DoesNotExist

        current_hint = SlideImage.objects.get(id=run.current_hint.id)

        next_hint = SlideImage.objects.get(
            Q(slide=current_hint.slide) &
            Q(hint_index=current_hint.hint_index+1)
        )

        user.hints_used += 1
        user.save()

        run.hints_used += 1
        run.current_hint = next_hint
        run.save()

        slide = Slide.objects.get(id=current_hint.slide.id)
        slide.hints_used += 1
        slide.save()

        response = {
            "slide_image_path": next_hint.image.name,
        }

        return Response(data=response, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response(data={'error': "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

    except Run.DoesNotExist:
        return Response(data={'error': "Invalid run"}, status=status.HTTP_400_BAD_REQUEST)

    except SlideImage.DoesNotExist:
        return Response(data={'error': "Invalid hint"}, status=status.HTTP_400_BAD_REQUEST)

    except Slide.DoesNotExist:
        return Response(data={'error': "Invalid slide"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getAnswerSlide(request, pk):
    try:
        run = Run.objects.get(id=pk)
        user = User.objects.get(username=run.id_user)

        if not user or user.username != request.user.username:
            raise User.DoesNotExist

        current_hint = SlideImage.objects.get(id=run.current_hint.id)
        slide = Slide.objects.get(id=current_hint.slide.id)
        slide_final = SlideImage.objects.get(
            Q(slide=slide) &
            Q(hint_index=slide.hints_amount-1)
        )

        slide_run = SlideRun.objects.get(Q(original_slide=slide.id) & Q(run_id=run.id))

        answer = False

        if slide.prof_discipline.lower() == request.data['answer'].lower():
            slide.hits += 1
            user.hits += 1
            run.hits += 1
            answer = True
            slide_run.has_hit = True
        else:
            slide.misses += 1
            user.misses += 1
            run.misses += 1
            slide_run.has_hit = False

        slide.save()
        user.save()
        run.save()
        slide_run.save()

        return Response(data={"answer": answer, "slide_image_path": slide_final.image.name, "slide": slide.prof_discipline}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response(data={'error': "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

    except Run.DoesNotExist:
        return Response(data={'error': "Invalid run"}, status=status.HTTP_400_BAD_REQUEST)

    except SlideImage.DoesNotExist:
        return Response(data={'error': "Invalid hint"}, status=status.HTTP_400_BAD_REQUEST)

    except Slide.DoesNotExist:
        return Response(data={'error': "Invalid slide"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getHistoryRun(request, pk=None):
    try:
        run = Run.objects.get(id = pk)
        slides_run = SlideRun.objects.filter(run_id=run.id)

        response = SlideRunSerializer(slides_run)
        return Response(data={"slides_run": response}, status=status.HTTP_200_OK)

    except Run.DoesNotExist:
        return Response(data={'error': "Invalid run"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getAlternatives(request, pk):
    try:
        run = Run.objects.get(id=pk)
        user = User.objects.get(username=run.id_user)

        if not user or user.username != request.user.username:
            raise User.DoesNotExist

    # TODO: finish this later

    # this function selects the alternatives to display in with the slide during the game
    # it has to make sure that one of them is the right one and the others vary...

    except User.DoesNotExist:
        return Response(data={'error': "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

    except Run.DoesNotExist:
        return Response(data={'error': "Invalid run"}, status=status.HTTP_400_BAD_REQUEST)

    except SlideImage.DoesNotExist:
        return Response(data={'error': "Invalid hint"}, status=status.HTTP_400_BAD_REQUEST)

    except Slide.DoesNotExist:
        return Response(data={'error': "Invalid slide"}, status=status.HTTP_400_BAD_REQUEST)
