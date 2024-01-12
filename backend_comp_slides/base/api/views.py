from .serializers import *
from ..models import *

from django.contrib.auth.hashers import make_password
from django.db.models import Q
from random import choice

import re
import json

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
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
def createUser(request):
    if not request.data["username"] or not request.data["password"]:
        return Response(
            data={"error": "Ainda existem campos para preencher"}, status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=request.data["username"]).exists():
        return Response(
            data={"error": "Nome de usuário em uso!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    if len(request.data["username"]) >=25:
        return Response(
            data={"error": "O nome de usuário deve possuir até 25 characteres"}, status=status.HTTP_400_BAD_REQUEST
        )

    if len(request.data["password"]) < 8:
        return Response(
            data={"error": "A senha deve ter mais de 8 caracteres"}, status=status.HTTP_400_BAD_REQUEST
        )

    hashed_password = make_password(request.data["password"])
    request.data["password"] = hashed_password

    user = UserSerializer(data=request.data)
    
    if user.is_valid():
        user.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(
            data={"error": "Invalid user fields"}, status=status.HTTP_400_BAD_REQUEST
        )


def profanity_filter(text:str):
    
    with open('profanity_words.txt') as f:
        profanity_words = f.read().splitlines()

    pattern = re.compile(r'\b(?:' + '|'.join(profanity_words) + r')\b', flags=re.IGNORECASE)
    filtered_text = pattern.sub(lambda x: '*' * len(x.group()), text)

    return filtered_text


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addMessageToUser(request):
    try:
        message_text = request.data["message"].strip()

        if len(message_text) > 200:
            return Response(
                data={"error": "Mensagem é muito longa (>200 caracteres)"},
                status=status.HTTP_403_FORBIDDEN,
            )
    
        if len(message_text) == 0:
            return Response(
                data={"error": "Mensagem em branco?? Sério??"},
                status=status.HTTP_403_FORBIDDEN,
            )

        logged_user = User.objects.get(username=request.user.username)

        user_messages_amount = Message.objects.filter(user=logged_user).count()
        user_runs_amount = Run.objects.filter(user=logged_user).count()

        if user_messages_amount>=user_runs_amount:
            return Response(data={"error": "É permitida apenas uma mensagem por sessão"}, status=status.HTTP_400_BAD_REQUEST)

        new_message = MessageSerializer(
            data={
                "text": profanity_filter(message_text),
                "user": logged_user.id
            }
        )

        if new_message.is_valid():
            new_message.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(data={"error": "Erro ao salvar a mensagem"}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response(
            data={"error": "Usuário não encontrado"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as erro:
        print(erro)


        return Response(
            data={"error": "Problema inesperado"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
def getMessages(request):
    messages = list()

    for message in Message.objects.all():
        messages.append({
            "username": message.user.username,
            "text": message.text
        })
    

    return Response(data=messages, status=status.HTTP_200_OK)

# slide views


def create_slide_alternatives(slide):
    # fetching three slides to append as possible answers
    all_slides_randomly_sorted = Slide.objects.order_by("?")
    slide_alternatives = [slide]
    for option in all_slides_randomly_sorted:
        if option.id == slide.id:
            continue

        if len(slide_alternatives) >= 4:
            break

        slide_alternatives.append(option)

    return slide_alternatives


def create_new_slide_run(slide, run, slide_alternatives):
    new_slide_run = SlideRunSerializer(
        data={
            "original_slide": slide.id,
            "run_id": run.id,
            "has_hit": 0,
            "has_missed": 0,
            "hints_used": 0,
            "points": 0,
            "slide_alternatives": [slide.id for slide in slide_alternatives],
        }
    )

    if not new_slide_run.is_valid():
        return Response(
            data={"error": "Invalid slide run creation"},
            status=status.HTTP_400_BAD_REQUEST,
        )
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
                Q(slide__id=random_slide.id) & Q(hint_index=0)
            )

            slide_alternatives = create_slide_alternatives(random_slide)

            new_run = RunSerializer(
                data={
                    "user": request.user.id,
                    "current_hint": first_hint.id,
                    "slides_left": Config.objects.all().first().max_slides_per_run
                }
            )

            if not new_run.is_valid():
                return Response(
                    data={"error": "Invalid run creation"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                new_run = new_run.save()

            new_slide_run = create_new_slide_run(
                random_slide, new_run, slide_alternatives
            )

            response = {
                "run_id": new_run.id,
                "slides_left_amount": new_run.slides_left,
                "slide_image_path": first_hint.image.name,
                "hints_used": 0,
                "hints_total": random_slide.hints_amount,
                "difficulty_level": random_slide.difficulty_level,
                "slide_alternatives": [
                    alternative.prof_discipline
                    for alternative in new_slide_run.slide_alternatives.all()
                ],
                "slide_run_id": new_slide_run.id,
            }

        # if there is a run id, then append the new slide_run to it
        else:
            current_run = Run.objects.get(id=pk)

            if current_run.slides_left == 0:
                return Response(
                    data={"error": "Run finished"},
                    status=status.HTTP_301_MOVED_PERMANENTLY,
                )

            current_slide_run = None
            slide_runs_of_specifique_run = SlideRun.objects.filter(
                Q(run_id=current_run.id)
            )
            for slide_run in slide_runs_of_specifique_run:
                if not slide_run.has_hit and not slide_run.has_missed:
                    current_slide_run = slide_run

            if current_slide_run == None or slide_run_has_ended(current_slide_run):
                all_slides_randomly_sorted = Slide.objects.order_by("?")
                random_slide = all_slides_randomly_sorted.first()
                first_hint = SlideImage.objects.get(
                    Q(slide__id=random_slide.id) & Q(hint_index=0)
                )

                slide_alternatives = slide_alternatives = create_slide_alternatives(
                    random_slide
                )
                current_slide_run = create_new_slide_run(
                    random_slide, current_run, slide_alternatives
                )

                current_run.current_hint = first_hint
                current_run.save()

            response = {
                "run_id": current_run.id,
                "slides_left_amount": current_run.slides_left,
                "slide_image_path": current_run.current_hint.image.name,
                "hints_used": current_slide_run.hints_used,
                "hints_total": current_slide_run.original_slide.hints_amount,
                "difficulty_level": current_slide_run.original_slide.difficulty_level,
                "slide_alternatives": [
                    slide.prof_discipline
                    for slide in current_slide_run.slide_alternatives.all()
                ],
                "slide_run_id": current_slide_run.id,
            }

        return Response(data=response, status=status.HTTP_200_OK)

    except Run.DoesNotExist:
        return Response(
            data={"error": "Invalid run"}, status=status.HTTP_400_BAD_REQUEST
        )

    except SlideImage.DoesNotExist:
        return Response(
            data={"error": "Invalid hint"}, status=status.HTTP_400_BAD_REQUEST
        )

    except Slide.DoesNotExist:
        return Response(
            data={"error": "Invalid slide"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def getHint(request, pk):
    try:
        current_run = Run.objects.get(id=pk)
        user = User.objects.get(username=current_run.user)

        if not user or user.username != request.user.username:
            raise User.DoesNotExist

        current_hint = SlideImage.objects.get(id=current_run.current_hint.id)
        next_hint = SlideImage.objects.get(
            Q(slide=current_hint.slide) & Q(hint_index=current_hint.hint_index + 1)
        )

        user.total_hints_used += 1
        user.save()

        current_run.current_hint = next_hint
        current_run.save()

        current_slide = Slide.objects.get(id=current_hint.slide.id)
        current_slide_run = SlideRun.objects.filter(
            Q(has_hit=False) & Q(has_missed=False) & Q(original_slide=current_slide)
        ).first()
        current_slide_run.hints_used += 1
        current_slide_run.save()

        response = {
            "slide_image_path": next_hint.image.name,
        }

        return Response(data=response, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response(
            data={"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST
        )

    except Run.DoesNotExist:
        return Response(
            data={"error": "Invalid run"}, status=status.HTTP_400_BAD_REQUEST
        )

    except SlideImage.DoesNotExist:
        return Response(
            data={"error": "Invalid hint (no more hints for this slide)"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Slide.DoesNotExist:
        return Response(
            data={"error": "Invalid slide"}, status=status.HTTP_400_BAD_REQUEST
        )


def calculate_points_on_win(current_run):
    total_hints_available = current_run.original_slide.hints_amount
    hints_usage = total_hints_available - current_run.hints_used
    hints_factor = hints_usage / total_hints_available
    max_points = Config.objects.all().first().max_points_per_slide_run

    return hints_factor * max_points


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def getAnswerSlide(request, pk):
    try:
        current_run = Run.objects.get(id=pk)
        user = User.objects.get(username=current_run.user)

        if not user or user.username != request.user.username:
            raise User.DoesNotExist

        current_hint = SlideImage.objects.get(id=current_run.current_hint.id)
        slide = Slide.objects.get(id=current_hint.slide.id)
        slide_image_final = SlideImage.objects.get(
            Q(slide=slide) & Q(hint_index=slide.hints_amount)
        )

        current_slide_run = SlideRun.objects.get(
            Q(run_id=current_run.id) & Q(has_hit=False) & Q(has_missed=False)
        )

        answer = False
        if slide.prof_discipline.lower() == request.data["answer"].lower():
            slide.total_hits += 1
            user.total_hits += 1
            current_run.slides_left -= 1
            answer = True
            current_slide_run.has_hit = True
            current_slide_run.points += calculate_points_on_win(current_slide_run)
            user.total_points += current_slide_run.points
            current_run.total_points += current_slide_run.points
        else:
            slide.total_misses += 1
            user.total_misses += 1
            current_run.slides_left -= 1
            current_slide_run.has_missed = False

        slide.save()
        user.save()
        current_run.save()
        current_slide_run.save()

        return Response(
            data={
                "answer": answer,
                "slide_image_path": slide_image_final.image.name,
                "slide": slide.prof_discipline,
            },
            status=status.HTTP_200_OK,
        )

    except User.DoesNotExist:
        return Response(
            data={"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST
        )

    except Run.DoesNotExist:
        return Response(
            data={"error": "Invalid run"}, status=status.HTTP_400_BAD_REQUEST
        )

    except SlideImage.DoesNotExist:
        return Response(
            data={"error": "Invalid hint"}, status=status.HTTP_400_BAD_REQUEST
        )

    except Slide.DoesNotExist:
        return Response(
            data={"error": "Invalid slide"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getHistoryRun(request, pk=None):
    try:
        run = Run.objects.get(id=pk)
        slides_run = SlideRun.objects.filter(run_id=run.id)

        slides_reports_list = list()
        slides_hits_count = 0
        total_points = 0

        for slide_run in slides_run:

            final_slide_image = SlideImage.objects\
                .filter(Q(slide=slide_run.original_slide))\
                .order_by('-hint_index').first()

            slides_reports_list.append({
                "has_hit" : slide_run.has_hit,
                "prof_discipline": slide_run.original_slide.prof_discipline,
                "slide_image_path": final_slide_image.image.name,
                "difficulty_level": slide_run.original_slide.difficulty_level,
            })

            total_points+=slide_run.points
            
            if slide_run.has_hit:
                slides_hits_count+=1

        all_users_points = 0
        all_users_runs = Run.objects.all()
        for run in all_users_runs:
            all_users_points+=run.total_points
        
        max_slides_per_run = Config.objects.all().first().max_slides_per_run
        max_points_per_slide_run = Config.objects.all().first().max_points_per_slide_run
        max_points_per_run = (max_slides_per_run * max_points_per_slide_run)

        all_users_average = all_users_points / (max_points_per_run * len(all_users_runs))
        this_user_average = total_points / max_points_per_run
        
        above_average_percentage = False
        below_average_percentage = True

        this_user_percentage = (this_user_average / all_users_average)

        if this_user_percentage > 1:
            above_average_percentage = this_user_percentage-1
        else:
            below_average_percentage = 1/this_user_percentage

        response = {
            "total_points" : total_points,
            "slides_reports_list": slides_reports_list,
            "above_average_percentage": above_average_percentage,
            "below_average_percentage": below_average_percentage,
            "slides_hits_count": slides_hits_count
        }
        

        return Response(data=response, status=status.HTTP_200_OK)

    except Run.DoesNotExist:
        return Response(
            data={"error": "Invalid run"}, status=status.HTTP_400_BAD_REQUEST
        )



