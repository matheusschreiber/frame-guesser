from django.contrib import admin
from django.urls import path, include
from .views import apiOverview, addUser, getUsers, \
    addMessageToUser, loginUser, getRandomSlide, updateUserStats, getHint

urlpatterns = [
    path("", apiOverview),
    path("user/create/", addUser, name='create-user'),
    path("user/list/", getUsers, name='list-users'),
    path("user/message/<str:pk>", addMessageToUser, name='add-message-user'),
    path("user/login/", loginUser, name="login-user"),
    path("user/update/", updateUserStats, name="update-stats-user"),
    path("slide/random/<str:pk>", getRandomSlide, name="random-slide"),
    path("slide/hint/<str:pk>", getHint, name="hint-slide")

]
