from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from .serializers import FilteredUserSerializer, UserSerializer, SlideSerializer
from .models import User

# user views


@api_view(['GET'])
def apiOverview(request):
    api_overview = {
        'get all users': '/users/',
        'get user by id': '/users/:id',
        'get all slides': '/slides/',
        'get slide by id': '/slides/:id',
        'get random slide': '/slides/random',
    }

    # TODO: adicionar resto do CRUD como documentação

    return JsonResponse(api_overview, safe=False)


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

    # if request.user.is_authenticated:
    #     return Response(status=status.HTTP_200_OK)

    # username = request.data['username'].strip().lower()
    # password = request.data['password']

    # if not User.objects.filter(username=username):
    #     return Response(data={'error': "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # user = authenticate(username=username, password=password)

    # if user is not None:
    #     login(request, user)
    #     return Response(status=status.HTTP_200_OK)
    # else:
    #     return Response(data={'error': "User/Password dont match"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def addUser(request):

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

    if not pk == user.id:
        return Response(data={'error': "User not allowed"}, status=status.HTTP_403_FORBIDDEN)

    user.message = message
    user.save()

    return Response(data=message)


# slide views

# @api_view(['GET'])
# @login_required(login_url='login')
# def getRandomSlide(request):
