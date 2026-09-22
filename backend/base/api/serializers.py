from base.models import Message, Movie, MovieRun, Run, User
from rest_framework.serializers import ModelSerializer  # type: ignore


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class FilteredUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = [  # noqa: RUF012
            "username",
            "total_points",
            "total_hits",
            "total_misses",
            "total_hints_used",
        ]

class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"

class RunSerializer(ModelSerializer):
    class Meta:
        model = Run
        fields = [  # noqa: RUF012
            "user",
            "movies_left",
            "total_points",
        ]

class MovieRunSerializer(ModelSerializer):
    class Meta:
        model = MovieRun
        fields = "__all__"

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"