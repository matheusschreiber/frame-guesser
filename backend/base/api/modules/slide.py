from django.db.models import Q

from base.api.serializers import SlideRunSerializer
from base.models import User, Slide, SlideImage, Run, SlideRun, Config
from base.api.modules.processors import RunProcessor

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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
def getNextSlide(request, pk=None):
    
    max_slides_per_run = Config.objects.filter(name="max_slides_per_run").first()
    max_slides_per_run = int(max_slides_per_run.value) if max_slides_per_run else 5
    max_points_per_slide_run = Config.objects.filter(name="max_points_per_slide_run").first()
    max_points_per_slide_run = int(max_points_per_slide_run.value) if max_points_per_slide_run else 10
    amount_slide_alternatives = Config.objects.filter(name="amount_slide_alternatives").first()
    amount_slide_alternatives = int(amount_slide_alternatives.value) if amount_slide_alternatives else 4
    
    run_processor = RunProcessor(
        pk, request.user.id, 
        max_slides_per_run, 
        max_points_per_slide_run, 
        amount_slide_alternatives
    )
    
    if not run_processor.is_valid_run():
        return Response(
            data={"error": "Invalid Run"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
    if run_processor.is_finished_run():
        return Response(
            data={"error": "Run has finished"},
            status=status.HTTP_301_MOVED_PERMANENTLY,
        )
    
    if not run_processor.get_or_create_slide_run():
        return Response(
            data={"error": "Error on SlideRun"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    response = run_processor.generate_response()
    return Response(
        data=response, 
        status=status.HTTP_200_OK
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
            Q(has_hit=False) & Q(has_missed=False) & Q(original_slide=current_slide) & Q(run_id=current_run)
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


def calculate_points_on_win(current_slide_run):
    total_hints_available = current_slide_run.original_slide.hints_amount
    hints_left = total_hints_available - current_slide_run.hints_used
    hints_factor = hints_left / total_hints_available
    config_max_points = Config.objects.filter(
        name="max_points_per_slide_run"
    ).first()
    if not config_max_points:
        raise Config.DoesNotExist("Config not set: max_points_per_slide_run")

    max_points = float(config_max_points.value)
    config_diff_bonus = Config.objects.filter(
        name=f"difficulty_{current_slide_run.original_slide.difficulty_level}_bonus"
    ).first()
    if not config_diff_bonus:
        raise Config.DoesNotExist("Config not set: max_points_per_slide_run")

    difficulty_bonus = float(config_diff_bonus.value)
    final_score = (hints_factor*.3 + difficulty_bonus*.7 ) * max_points
    final_score = (round(final_score * 1000))/1000

    return final_score



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
            Q(slide=slide) & Q(hint_index=slide.hints_amount-1)
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

            current_slide_run.points = calculate_points_on_win(current_slide_run)
            user.total_points += current_slide_run.points
            current_run.total_points += current_slide_run.points
        else:
            slide.total_misses += 1
            user.total_misses += 1
            current_run.slides_left -= 1
            current_slide_run.has_missed = True

        slide.save()
        user.save()
        current_run.save()
        current_slide_run.save()

        return Response(
            data={
                "answer": answer,
                "slide_image_path": slide_image_final.image.name,
                "slide": slide.prof_discipline,
                "points": current_slide_run.points,
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

    # TODO: create the exception for config not setted up


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
            final_slide_image = (
                SlideImage.objects.filter(Q(slide=slide_run.original_slide))
                .order_by("-hint_index")
                .first()
            )

            slides_reports_list.append(
                {
                    "has_hit": slide_run.has_hit,
                    "prof_discipline": slide_run.original_slide.prof_discipline,
                    "slide_image_path": final_slide_image.image.name,
                    "difficulty_level": slide_run.original_slide.difficulty_level,
                    "points": slide_run.points,
                    "hints_used": slide_run.hints_used
                }
            )

            total_points += slide_run.points

            if slide_run.has_hit:
                slides_hits_count += 1

        all_users_points = 0
        all_users_runs = Run.objects.all()
        for run in all_users_runs:
            all_users_points += run.total_points

        try:
            max_slides_per_run = int(
                Config.objects.get(name="max_slides_per_run").value
            )
            max_points_per_slide_run = int(
                Config.objects.get(name="max_points_per_slide_run").value
            )
        except Config.DoesNotExist:
            return Response(
                data={
                    "error": "Config not present: max_slides_per_run, max_points_per_slide_run"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        max_points_per_run = max_slides_per_run * max_points_per_slide_run

        all_users_average = all_users_points / (
            max_points_per_run * len(all_users_runs)
        )
        this_user_average = total_points / max_points_per_run

        above_average_percentage = 0
        below_average_percentage = 0

        this_user_percentage = this_user_average / all_users_average

        if this_user_percentage > 1:
            above_average_percentage = this_user_percentage - 1
        else:
            below_average_percentage =  1 - this_user_percentage

        response = {
            "total_points": f'{total_points:.2f}',
            "slides_reports_list": slides_reports_list,
            "above_average_percentage": above_average_percentage,
            "below_average_percentage": below_average_percentage,
            "slides_hits_count": slides_hits_count,
        }

        return Response(data=response, status=status.HTTP_200_OK)

    except Run.DoesNotExist:
        return Response(
            data={"error": "Invalid run"}, status=status.HTTP_400_BAD_REQUEST
        )
