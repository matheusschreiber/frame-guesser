from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import UserSerializer, SlideSerializer
from .models import User

# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_overview = {
      'get all users':'/users/',
      'get user by id':'/users/:id',
      'get all slides':'/slides/',
      'get slide by id': '/slides/:id',
      'get random slide': '/slides/random',
    }

    # TODO: adicionar resto do CRUD como documentação

    return JsonResponse(api_overview, safe=False)


@api_view(['POST'])
def addUser(request):

    user = UserSerializer(data=request.data)
 
    if User.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This user already exists')
 
    if user.is_valid():
        user.save()
        return Response(user.data)
    else:
        return Response(data=user.data, status=status.HTTP_400_BAD_REQUEST)
