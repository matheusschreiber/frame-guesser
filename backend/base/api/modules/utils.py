from base.api.serializers import *
from base.models import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(["GET"])
def getDisciplines(request):
    slides = Slide.objects.all().values_list("prof_discipline", flat=True)
    return Response(data=slides, status=status.HTTP_200_OK)