from rest_framework.serializers import ModelSerializer
from base.models import User, Slide

class UserSerializer(ModelSerializer):
  
  class Meta:
    model = User
    fields = '__all__'    


class SlideSerializer(ModelSerializer):
  
  class Meta:
    model = Slide
    fields = '__all__'    