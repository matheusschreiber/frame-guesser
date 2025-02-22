from django.contrib import admin
from django.urls import path, include
from .views import *

from rest_framework_simplejwt.views import (TokenRefreshView,)

urlpatterns = [
    path('user/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', createUser, name='create_user'),
    path("user/list/", getUsers, name='list_users'),
    path("user/message/", addMessageToUser, name='add_message_user'),
    path("user/message/list/", getMessages, name="list_messages"),

    path("slide/random", getRandomSlide, name="no_run_random_slide"),
    path("slide/random/<str:pk>", getRandomSlide, name="random_slide"),
    path("slide/hint/<str:pk>", getHint, name="hint_slide"),
    path("slide/answer/<str:pk>", getAnswerSlide, name="answer_slide"),

    path("disciplines/", getDisciplines, name="get_disciplines"),
    path("history/<str:pk>", getHistoryRun, name='get_history')
]
