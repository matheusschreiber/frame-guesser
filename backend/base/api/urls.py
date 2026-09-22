from base.api.modules.movie import addMovie, generateHints, listMovies, listMoviesAdmin
from base.api.modules.user import (
    MyTokenObtainPairView,
    addMessageToUser,
    createUser,
    getMessages,
    getUsers,
)
from base.api.views import getAnswerMovie, getHint, getHistoryRun, getNextMovie
from django.urls import path  # type: ignore
from rest_framework_simplejwt.views import (  # type: ignore
    TokenRefreshView,
)

urlpatterns = [
    path('user/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', createUser, name='create_user'),
    path("user/list/", getUsers, name='list_users'),
    path("user/message/", addMessageToUser, name='add_message_user'),
    path("user/message/list/", getMessages, name="list_messages"),

    path("movie/new/", addMovie, name="add_movie"),
    path("movie/list/admin/", listMoviesAdmin, name="list_movies_admin"),
    path("movie/list/", listMovies, name="list_movies"),
    path("movie/generate-hints/", generateHints, name="generate_hints"),
    path("movie/<str:pk>", getNextMovie, name="get_next_movie"),
    path("movie/hint/<str:pk>", getHint, name="hint_movie"),
    path("movie/answer/<str:pk>", getAnswerMovie, name="answer_movie"),

    path("history/<str:pk>", getHistoryRun, name='get_history'),
]
