from django.contrib import admin
from django.urls import path, include
from .views import apiOverview, addUser, getUsers, addMessageToUser, loginUser

urlpatterns = [
    path("", apiOverview),
    path("user/create/", addUser, name='create-user'),
    path("user/list/", getUsers, name='list-users'),
    path("user/message/<str:pk>", addMessageToUser, name='add-message-user'),
    path("user/login/", loginUser, name="login-user"),
]
