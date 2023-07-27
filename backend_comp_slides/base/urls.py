from django.contrib import admin
from django.urls import path, include
from .views import apiOverview, addUser

urlpatterns = [
    path("", apiOverview),
    path("user/", addUser)
]
