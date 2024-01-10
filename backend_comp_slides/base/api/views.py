from .serializers import FilteredUserSerializer, UserSerializer, SlideSerializer, RunSerializer, SlideRunSerializer
from ..models import User, Slide, SlideImage, Run, SlideRun
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from random import choice

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions, status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



# extra views

@api_view(["GET"])
def getDisciplines(request):
    slides = Slide.objects.all().values_list("prof_discipline", flat=True)
    return Response(data=slides, status=status.HTTP_200_OK)


# user views

@api_view(["GET"])
def getUsers(request):
    users = User.objects.all()
    users_serialized = FilteredUserSerializer(users, many=True)

    return Response(data=users_serialized.data, status=status.HTTP_200_OK)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

@api_view(["POST"])
def addUser(request):

    if not request.data["username"] or not request.data["password"]:
        return Response(data={"error": "Empty fields detected"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=request.data["username"]).exists():
        return Response(data={"error": "Username already in use"}, status=status.HTTP_400_BAD_REQUEST)

    if len(request.data["password"]) < 8:
        return Response(data={"error": "Password is too short"}, status=status.HTTP_400_BAD_REQUEST)

    hashed_password = make_password(request.data["password"])
    request.data["password"] = hashed_password

    user = UserSerializer(data=request.data)

    if user.is_valid():
        user.save()
        return Response(user.data, status=status.HTTP_201_CREATED)
    else:
        return Response(data={"error": "Invalid user fields"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addMessageToUser(request, pk):

    try:
        user = User.objects.get(id=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    message = request.data["message"].strip()

    if len(message) > 200:
        return Response(data={"error": "Message is too long (>200 caracters)"}, status=status.HTTP_403_FORBIDDEN)

    logged_user = User.objects.get(username=request.user.username)
    if int(pk) != int(logged_user.id):
        return Response(data={"error": "User not allowed"}, status=status.HTTP_403_FORBIDDEN)

    user.message = message
    user.save()

    return Response(data=message)


# slide views

def create_slide_alternatives(slide):
    # fetching three slides to append as possible answers
    all_slides_randomly_sorted = Slide.objects.order_by("?")
    slide_alternatives = [slide]
    for option in all_slides_randomly_sorted:
        if option.id==slide.id:
            continue
            
        if len(slide_alternatives)>=4:
            break
        
        slide_alternatives.append(option)
    
    return slide_alternatives



def create_new_slide_run(slide, run, slide_alternatives):
    new_slide_run = SlideRunSerializer(data={
        "original_slide": slide.id,
        "run_id": run.id,
        "has_hit": 0,
        "has_missed": 0,
        "hints_used": 0,
        "points": 0,
        "slide_alternatives": [slide.id for slide in slide_alternatives],
    })

    if not new_slide_run.is_valid():
        return Response(data={"error": "Invalid slide run creation"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return new_slide_run.save()


def slide_run_has_ended(slide_run):
    return slide_run.hints_used == slide_run.original_slide.hints_amount

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getRandomSlide(request, pk=None):
    try:

        # if no run id is passed, then its the first slide
        if not pk:

            all_slides_randomly_sorted = Slide.objects.order_by("?")
            random_slide = all_slides_randomly_sorted.first()
            first_hint = SlideImage.objects.get(
                Q(slide__id=random_slide.id) & Q(hint_index=0))

            slide_alternatives = create_slide_alternatives(random_slide)
            
            new_run = RunSerializer(data={
                "id_user": request.user.id,
                "current_hint": first_hint.id,
            })

            if not new_run.is_valid():
                return Response(data={"error": "Invalid run creation"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                new_run = new_run.save()


            new_slide_run = create_new_slide_run(random_slide, new_run, slide_alternatives)
            
            response = {
                "run_id": new_run.id,
                "slides_left_amount": new_run.slides_left,
                "slide_image_path": first_hint.image.name,
                "hints_used": 0,
                "hints_total": random_slide.hints_amount,
                "difficulty_level": random_slide.difficulty_level,
                "slide_alternatives": [alternative.prof_discipline for alternative in new_slide_run.slide_alternatives.all()],
                "slide_run_id": new_slide_run.id
            }

        # if there is a run id, then append the new slide_run to it
        else:
            current_run = Run.objects.get(id=pk)

            if current_run.slides_left == 0:
                return Response(data={"error": "Run finished"}, status=status.HTTP_301_MOVED_PERMANENTLY)

            current_slide_run = None
            slide_runs_of_specifique_run = SlideRun.objects.filter(Q(run_id=current_run.id))
            for slide_run in slide_runs_of_specifique_run:
                if not slide_run.has_hit and not slide_run.has_missed:
                    current_slide_run = slide_run

            if current_slide_run == None or slide_run_has_ended(current_slide_run):
                
                all_slides_randomly_sorted = Slide.objects.order_by("?")
                random_slide = all_slides_randomly_sorted.first()
                first_hint = SlideImage.objects.get(Q(slide__id=random_slide.id) & Q(hint_index=0))

                slide_alternatives = slide_alternatives = create_slide_alternatives(random_slide)
                current_slide_run = create_new_slide_run(random_slide, current_run, slide_alternatives)
                
                current_run.current_hint = first_hint
                current_run.save()

                
            response = {
                "run_id": current_run.id,
                "slides_left_amount": current_run.slides_left,
                "slide_image_path": current_run.current_hint.image.name,
                "hints_used": current_slide_run.hints_used,
                "hints_total": current_slide_run.original_slide.hints_amount,
                "difficulty_level": current_slide_run.original_slide.difficulty_level,
                "slide_alternatives": [slide.prof_discipline for slide in current_slide_run.slide_alternatives.all()],
                "slide_run_id": current_slide_run.id
            }

        return Response(data=response, status=status.HTTP_200_OK)

    except Run.DoesNotExist:
        return Response(data={"error": "Invalid run"}, status=status.HTTP_400_BAD_REQUEST)

    except SlideImage.DoesNotExist:
        return Response(data={"error": "Invalid hint"}, status=status.HTTP_400_BAD_REQUEST)

    except Slide.DoesNotExist:
        return Response(data={"error": "Invalid slide"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def getHint(request, pk):
    try:
        current_run = Run.objects.get(id=pk)
        user = User.objects.get(username=current_run.id_user)

        if not user or user.username != request.user.username:
            raise User.DoesNotExist

        current_hint = SlideImage.objects.get(id=current_run.current_hint.id)
        next_hint = SlideImage.objects.get(
            Q(slide=current_hint.slide) &
            Q(hint_index=current_hint.hint_index+1)
        )

        user.total_hints_used += 1
        user.save()

        current_run.current_hint = next_hint
        current_run.save()

        current_slide = Slide.objects.get(id=current_hint.slide.id)
        current_slide_run = SlideRun.objects.filter(Q(has_hit=False) & Q(has_missed=False) & Q(original_slide=current_slide)).first()
        current_slide_run.hints_used += 1
        current_slide_run.save()

        response = {
            "slide_image_path": next_hint.image.name,
        }

        return Response(data=response, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response(data={"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

    except Run.DoesNotExist:
        return Response(data={"error": "Invalid run"}, status=status.HTTP_400_BAD_REQUEST)

    except SlideImage.DoesNotExist:
        return Response(data={"error": "Invalid hint (no more hints for this slide)"}, status=status.HTTP_400_BAD_REQUEST)

    except Slide.DoesNotExist:
        return Response(data={"error": "Invalid slide"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def getAnswerSlide(request, pk):
    try:
        current_run = Run.objects.get(id=pk)
        user = User.objects.get(username=current_run.id_user)

        if not user or user.username != request.user.username:
            raise User.DoesNotExist

        current_hint = SlideImage.objects.get(id=current_run.current_hint.id)
        slide = Slide.objects.get(id=current_hint.slide.id)
        slide_image_final = SlideImage.objects.get(
            Q(slide=slide) &
            Q(hint_index=slide.hints_amount)
        )

        current_slide_run = SlideRun.objects.get(Q(run_id=current_run.id) & Q(has_hit=False) & Q(has_missed=False))

        answer = False
        if slide.prof_discipline.lower() == request.data["answer"].lower():
            slide.total_hits += 1
            user.total_hits += 1
            current_run.slides_left -= 1
            answer = True
            current_slide_run.has_hit = True
        else:
            slide.total_misses += 1
            user.total_misses += 1
            current_run.slides_left -= 1
            current_slide_run.has_missed = False

        slide.save()
        user.save()
        current_run.save()
        current_slide_run.save()

        return Response(data={"answer": answer, "slide_image_path": slide_image_final.image.name, "slide": slide.prof_discipline}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response(data={"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

    except Run.DoesNotExist:
        return Response(data={"error": "Invalid run"}, status=status.HTTP_400_BAD_REQUEST)

    except SlideImage.DoesNotExist:
        return Response(data={"error": "Invalid hint"}, status=status.HTTP_400_BAD_REQUEST)

    except Slide.DoesNotExist:
        return Response(data={"error": "Invalid slide"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getHistoryRun(request, pk=None):
    try:
        run = Run.objects.get(id = pk)
        slides_run = SlideRun.objects.filter(run_id=run.id)

        response = SlideRunSerializer(slides_run)
        return Response(data={"slides_run": response}, status=status.HTTP_200_OK)

    except Run.DoesNotExist:
        return Response(data={"error": "Invalid run"}, status=status.HTTP_400_BAD_REQUEST)