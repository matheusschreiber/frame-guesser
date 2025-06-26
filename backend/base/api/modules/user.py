from django.contrib.auth.hashers import make_password

from base.api.serializers import *
from base.models import *

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

import re

@api_view(["GET"])
def getUsers(request):
    users = User.objects.all()
    users_serialized = FilteredUserSerializer(users, many=True)

    return Response(data=users_serialized.data, status=status.HTTP_200_OK)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
def createUser(request):
    if not request.data["username"] or not request.data["password"]:
        return Response(
            data={"error": "Ainda existem campos para preencher"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=request.data["username"]).exists():
        return Response(
            data={"error": "Nome de usuário em uso!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if len(request.data["username"]) >= 25:
        return Response(
            data={"error": "O nome de usuário deve possuir até 25 characteres"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if len(request.data["password"]) < 8:
        return Response(
            data={"error": "A senha deve ter mais de 8 caracteres"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    hashed_password = make_password(request.data["password"])
    request.data["password"] = hashed_password

    user = UserSerializer(data=request.data)

    if user.is_valid():
        user.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(
            data={"error": "Invalid user fields"}, status=status.HTTP_400_BAD_REQUEST
        )


def profanity_filter(text: str):
    with open("profanity_words.txt") as f:
        profanity_words = f.read().splitlines()

    pattern = re.compile(
        r"\b(?:" + "|".join(profanity_words) + r")\b", flags=re.IGNORECASE
    )
    filtered_text = pattern.sub(lambda x: "*" * len(x.group()), text)

    return filtered_text


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addMessageToUser(request):
    try:
        message_text = request.data["message"].strip()

        if len(message_text) > 200:
            return Response(
                data={"error": "Mensagem é muito longa (>200 caracteres)"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if len(message_text) == 0:
            return Response(
                data={"error": "Mensagem em branco?? Sério??"},
                status=status.HTTP_403_FORBIDDEN,
            )

        logged_user = User.objects.get(username=request.user.username)

        user_messages_amount = Message.objects.filter(user=logged_user).count()
        user_runs_amount = Run.objects.filter(user=logged_user).count()

        if user_messages_amount >= user_runs_amount:
            return Response(
                data={"error": "É permitida apenas uma mensagem por sessão"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_message = MessageSerializer(
            data={"text": profanity_filter(message_text), "user": logged_user.id}
        )

        if new_message.is_valid():
            new_message.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                data={"error": "Erro ao salvar a mensagem"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except User.DoesNotExist:
        return Response(
            data={"error": "Usuário não encontrado"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as erro:
        print(erro)

        return Response(
            data={"error": "Problema inesperado"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
def getMessages(request):
    messages = list()

    for message in Message.objects.all():
        messages.append({"username": message.user.username, "text": message.text})

    return Response(data=messages, status=status.HTTP_200_OK)