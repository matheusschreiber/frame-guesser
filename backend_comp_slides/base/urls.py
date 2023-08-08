from django.contrib import admin
from django.urls import path, include
from .views import addUser, getUsers, \
    addMessageToUser, loginUser, getRandomSlide, \
    getHint, getAnswerSlide

urlpatterns = [
    path("user/create/", addUser, name='create-user'),
    path("user/list/", getUsers, name='list-users'),
    path("user/message/<str:pk>", addMessageToUser, name='add-message-user'),
    path("user/login/", loginUser, name="login-user"),
    path("slide/random", getRandomSlide, name="no-run-random-slide"),
    path("slide/random/<str:pk>", getRandomSlide, name="random-slide"),
    path("slide/hint/<str:pk>", getHint, name="hint-slide"),
    path("slide/answer/<str:pk>", getAnswerSlide, name="answer-slide")

]
