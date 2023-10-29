from rest_framework.serializers import ModelSerializer
from base.models import User, Slide, SlideImage, Run, SlideRun


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class FilteredUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['username', 'message',
                  'points', 'hits', 'misses', 'hints_used']


class SlideSerializer(ModelSerializer):

    class Meta:
        model = Slide
        fields = '__all__'

# class SlideImageSerializer(ModelSerializer):

#     class Meta:
#         model = SlideImage
#         fields = '__all__'


class RunSerializer(ModelSerializer):

    class Meta:
        model = Run
        fields = '__all__'

class SlideRunSerializer(ModelSerializer):

    class Meta:
        model = SlideRun
        fields = '__all__'
