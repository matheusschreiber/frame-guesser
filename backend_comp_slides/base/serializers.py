from rest_framework.serializers import ModelSerializer
from base.models import User, Slide, SlideImages


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class FilteredUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['username', 'email', 'id',
                  'message', 'points', 'hits', 'misses', 'tips_used']


class SlideSerializer(ModelSerializer):

    class Meta:
        model = Slide
        fields = '__all__'

# class SlideImageSerializer(ModelSerializer):

#     class Meta:
#         model = SlideImages
#         fields = '__all__'