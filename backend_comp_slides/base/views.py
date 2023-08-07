from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from .serializers import FilteredUserSerializer, UserSerializer, SlideSerializer
from .models import User, Slide, SlideImages
from django.db.models import Q

from random import choice


@api_view(['GET'])
def apiOverview(request):
    api_overview = {
        # 'get all users': '/users/',
        # 'get user by id': '/users/:id',
        # 'get all slides': '/slides/',
        # 'get slide by id': '/slides/:id',
        # 'get random slide': '/slides/random',
    }

    return JsonResponse(api_overview, safe=False)


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

    request.data['username'] = request.data['username'].strip().lower() # FIXME: tirar isso
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


@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateUserStats(request):
    logged_user = User.objects.get(username=request.user.username)

    session = {
        'hits': request.data['hits'],
        'misses': request.data['misses'],
        'hints_used': request.data['hits'],
    }

    session['points'] = session['hits']*10 - session['hints_used']

    logged_user.hits += session['hits']
    logged_user.misses += session['misses']
    logged_user.hints_used += session['hits']
    logged_user.points += session['points']

    logged_user.save()

    return Response(data={'points': session['points']}, status=status.HTTP_200_OK)


# slide views

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getRandomSlide(request):
    slides = Slide.objects.all()

    if len(slides) > 0:
        # slide = choice(slides)
        slide = Slide.objects.get(prof_discipline="Matheus Schreiber | Tecnicas de Busca") # FIXME: provisorio

        if not slide:
            return Response(data={'error': "No slides registered"}, status=status.HTTP_400_BAD_REQUEST)


        first_hint = SlideImages.objects.get(Q(slide=slide) & Q(hint_index=0))

        if not first_hint:
            return Response(data={'error': "No hints for this slide", 'slide': slide.prof_discipline}, status=status.HTTP_400_BAD_REQUEST)
        
        response = {
            "slide_provisory": slide.prof_discipline,
            "slide_id": first_hint.slide.id,
            "slide_image": "/static/" + first_hint.image.name,
        }

        return Response(data=response, status=status.HTTP_200_OK)
    else:
        return Response(data=[], status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def updateSlideStats(request, pk):
    slide = Slide.objects.get(id=pk)

    session = {
        'hits': request.data['hits'],
        'misses': request.data['misses'],
        'hints_used': request.data['hits'],
    }

    slide.hits += session['hits']
    slide.misses += session['misses']
    slide.hints_used += session['hits']

    slide.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def getHint(request, pk):
    current_hint = SlideImages.objects.get(id=pk)
    next_hint = SlideImages.objects.filter(
        Q(slide=current_hint.slide) &
        Q(hint_index=current_hint.hint_index+1)
    )

    if not next_hint:
        return Response(data={'error': "No hints left"}, status=status.HTTP_400_BAD_REQUEST)
    else:

        #TODO: adicionar update de status do usuario aqui (ja que ele usou uma dica)

        response = {
            "slide_id": next_hint[0].id,
            "slide_image": next_hint[0].image,
        }

        return Response(data=response, status=status.HTTP_200_OK)