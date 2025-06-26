from rest_framework.serializers import ModelSerializer
from base.models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class FilteredUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = [
            "username",
            "total_points",
            "total_hits",
            "total_misses",
            "total_hints_used",
        ]

class SlideSerializer(ModelSerializer):
    class Meta:
        model = Slide
        fields = "__all__"

class RunSerializer(ModelSerializer):
    class Meta:
        model = Run
        fields = [
            "user",
            "slides_left",
            "total_points",
        ]

class SlideRunSerializer(ModelSerializer):
    class Meta:
        model = SlideRun
        fields = "__all__"

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"