from base.api.modules.movie import (
    addMovie,
    generateHints,
    getAnswerMovie,
    getHint,
    getHistoryRun,
    getNextMovie,
    listMoviesAdmin,
    listMoviesTitles,
)
from base.api.modules.user import (
    MyTokenObtainPairView,
    messagesHandler,
    usersHandler,
)
from django.urls import path  # type: ignore
from rest_framework_simplejwt.views import (  # type: ignore
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', usersHandler, name='users_create_and_list'),
    path("users/messages/", messagesHandler, name='message_create_and_list'),

    path("movies/", addMovie, name="movies_create"),
    path("movies/titles/", listMoviesTitles, name="list_movies_titles"),
    path("movies/next/<str:pk>", getNextMovie, name="get_next_movie"),
    path("movies/admin/", listMoviesAdmin, name="list_movies_admin"),
    path("movies/hints/", generateHints, name="generate_hints"),
    path("movies/hints/<str:pk>", getHint, name="hint_movie"),
    path("movies/answer/<str:pk>", getAnswerMovie, name="answer_movie"),
    
    path("history/<str:pk>", getHistoryRun, name='get_history'),
]
