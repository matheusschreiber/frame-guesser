import base64

from base.api.modules.hint_gen import generate_hints
from base.api.modules.processors import RunProcessor
from base.api.serializers import MovieRunSerializer
from base.models import Config, Frame, Movie, MovieRun, Run, User
from django.core.files.uploadedfile import UploadedFile  # type: ignore
from django.db.models import Q  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.decorators import (  # type: ignore
    api_view,
    parser_classes,
    permission_classes,
)
from rest_framework.parsers import FormParser, MultiPartParser  # type: ignore
from rest_framework.permissions import (  # type: ignore
    IsAdminUser,
    IsAuthenticated,  # type: ignore
)
from rest_framework.response import Response  # type: ignore

REQUIRED_IMAGE_SIZE = (400, 400)

def create_new_movie_run(movie, run, movie_alternatives):
    new_movie_run = MovieRunSerializer(
        data={
            "original_movie": movie.id,
            "run": run.id,
            "has_hit": 0,
            "has_missed": 0,
            "hints_used": 0,
            "points": 0,
            "movie_alternatives": [movie.id for movie in movie_alternatives],
        }
    )

    if not new_movie_run.is_valid():
        return Response(
            data={"error": "Invalid movie run creation"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        return new_movie_run.save()


def movie_run_has_ended(movie_run):
    return movie_run.hints_used == movie_run.original_movie.hints_amount


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getNextMovie(request, pk=None):
    
    max_movies_per_run = Config.objects.filter(name="max_movies_per_run").first()
    max_movies_per_run = int(max_movies_per_run.value) if max_movies_per_run else 5
    max_points_per_movie_run = Config.objects.filter(name="max_points_per_movie_run").first()
    max_points_per_movie_run = int(max_points_per_movie_run.value) if max_points_per_movie_run else 10
    amount_movie_alternatives = Config.objects.filter(name="amount_movie_alternatives").first()
    amount_movie_alternatives = int(amount_movie_alternatives.value) if amount_movie_alternatives else 4
    
    run_processor = RunProcessor(
        pk, request.user.id, 
        max_movies_per_run, 
        max_points_per_movie_run, 
        amount_movie_alternatives
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
    
    if not run_processor.get_or_create_movie_run():
        return Response(
            data={"error": "Error on MovieRun"},
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

        current_hint = Frame.objects.get(id=current_run.current_hint.id)
        next_hint = Frame.objects.get(
            Q(movie=current_hint.movie) & Q(hint_index=current_hint.hint_index + 1)
        )

        current_hint.times_skipped += 1
        current_hint.save()
        user.total_hints_used += 1
        user.save()

        current_run.current_hint = next_hint
        current_run.save()

        current_movie = Movie.objects.get(id=current_hint.movie.id)
        current_movie_run = MovieRun.objects.filter(
            Q(has_hit=False) & Q(has_missed=False) & Q(original_movie=current_movie) & Q(run=current_run)
        ).first()
        current_movie_run.hints_used += 1
        current_movie_run.save()

        response = {
            "frame_path": next_hint.image.name,
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

    except Frame.DoesNotExist:
        return Response(
            data={"error": "Invalid hint (no more hints for this movie)"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Movie.DoesNotExist:
        return Response(
            data={"error": "Invalid movie"}, status=status.HTTP_400_BAD_REQUEST
        )


def calculate_points_on_win(current_movie_run):
    total_hints_available = current_movie_run.original_movie.hints_amount
    hints_left = total_hints_available - current_movie_run.hints_used
    hints_factor = hints_left / total_hints_available
    config_max_points = Config.objects.filter(
        name="max_points_per_movie_run"
    ).first()
    if not config_max_points:
        raise Config.DoesNotExist("Config not set: max_points_per_movie_run")

    max_points = float(config_max_points.value)
    config_diff_bonus = Config.objects.filter(
        name=f"difficulty_{current_movie_run.original_movie.difficulty_level}_bonus"
    ).first()
    if not config_diff_bonus:
        raise Config.DoesNotExist("Config not set: max_points_per_movie_run")

    difficulty_bonus = float(config_diff_bonus.value)
    final_score = (hints_factor*.3 + difficulty_bonus*.7 ) * max_points
    final_score = (round(final_score * 1000))/1000

    return final_score



@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def getAnswerMovie(request, pk):
    try:
        current_run = Run.objects.get(id=pk)
        user = User.objects.get(username=current_run.user)

        if not user or user.username != request.user.username:
            raise User.DoesNotExist

        current_hint = Frame.objects.get(id=current_run.current_hint.id)
        movie = Movie.objects.get(id=current_hint.movie.id)
        frame_final = Frame.objects.get(
            Q(movie=movie) & Q(hint_index=movie.hints_amount-1)
        )

        current_movie_run = MovieRun.objects.get(
            Q(run=current_run) & Q(has_hit=False) & Q(has_missed=False)
        )

        answer = False
        movie_verbose = f"{movie.name} ({movie.year}) | {movie.director}"
        if movie_verbose.lower() == request.data["answer"].lower():
            current_hint.times_guessed_right += 1
            movie.total_hits += 1
            user.total_hits += 1
            current_run.movies_left -= 1
            answer = True
            current_movie_run.has_hit = True

            current_movie_run.points = calculate_points_on_win(current_movie_run)
            user.total_points += current_movie_run.points
            current_run.total_points += current_movie_run.points
        else:
            current_hint.times_guessed_wrong += 1
            movie.total_misses += 1
            user.total_misses += 1
            current_run.movies_left -= 1
            current_movie_run.has_missed = True

        movie.save()
        user.save()
        current_run.save()
        current_movie_run.save()
        current_hint.save()

        return Response(
            data={
                "answer": answer,
                "frame_path": frame_final.image.name,
                "movie_verbose": f"{movie.name} ({movie.year}) | {movie.director}",
                "points": current_movie_run.points,
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

    except Frame.DoesNotExist:
        return Response(
            data={"error": "Invalid hint"}, status=status.HTTP_400_BAD_REQUEST
        )

    except Movie.DoesNotExist:
        return Response(
            data={"error": "Invalid movie"}, status=status.HTTP_400_BAD_REQUEST
        )

    # TODO: create the exception for config not setted up


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getHistoryRun(request, pk=None):
    try:
        run = Run.objects.get(id=pk)
        movies_run = MovieRun.objects.filter(run=run)

        movies_reports_list = []
        movies_hits_count = 0
        total_points = 0

        for movie_run in movies_run:
            final_frame = (
                Frame.objects.filter(Q(movie=movie_run.original_movie))
                .order_by("-hint_index")
                .first()
            )

            movies_reports_list.append(
                {
                    "has_hit": movie_run.has_hit,
                    "name": movie_run.original_movie.name,
                    "year": movie_run.original_movie.year,
                    "director": movie_run.original_movie.director,
                    "frame_path": final_frame.image.name,
                    "difficulty_level": movie_run.original_movie.difficulty_level,
                    "points": movie_run.points,
                    "hints_used": movie_run.hints_used
                }
            )

            total_points += movie_run.points

            if movie_run.has_hit:
                movies_hits_count += 1

        all_users_points = 0
        all_users_runs = Run.objects.all()
        for run in all_users_runs:
            all_users_points += run.total_points

        try:
            max_movies_per_run = int(
                Config.objects.get(name="max_movies_per_run").value
            )
            max_points_per_movie_run = int(
                Config.objects.get(name="max_points_per_movie_run").value
            )
        except Config.DoesNotExist:
            return Response(
                data={
                    "error": "Config not present: max_movies_per_run, max_points_per_movie_run"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        max_points_per_run = max_movies_per_run * max_points_per_movie_run

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
            "movies_reports_list": movies_reports_list,
            "above_average_percentage": above_average_percentage,
            "below_average_percentage": below_average_percentage,
            "movies_hits_count": movies_hits_count,
        }

        return Response(data=response, status=status.HTTP_200_OK)

    except Run.DoesNotExist:
        return Response(
            data={"error": "Invalid run"}, status=status.HTTP_400_BAD_REQUEST
        )

def _validate_image_dimensions(image_file: UploadedFile) -> bool:
    try:
        from PIL import Image
    except ImportError:
        return True

    try:
        with Image.open(image_file) as img:
            valid = img.size == REQUIRED_IMAGE_SIZE
    finally:
        image_file.seek(0)

    return valid


@api_view(["POST"])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def generateHints(request):
    image = request.FILES.get("image")

    if not image:
        return Response(
            data={"error": "An image is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not _validate_image_dimensions(image):
        return Response(
            data={"error": f"Image must be exactly {REQUIRED_IMAGE_SIZE[0]}x{REQUIRED_IMAGE_SIZE[1]} pixels."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    ext = (image.name or "movie.png").rsplit(".", 1)[-1].lower()
    if ext not in ("png", "jpg", "jpeg"):
        ext = "png"

    try:
        image_bytes = image.read()
        hints = generate_hints(image_bytes, ext)
    except Exception as exc:  # noqa: BLE001
        return Response(
            data={"error": f"Hint generation failed: {exc}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    encoded = [
        "data:image/png;base64," + base64.b64encode(h).decode("ascii")
        for h in hints
    ]

    return Response(
        data={
            "hints": encoded,
            "hints_amount": len(encoded),
            "difficulty_level": min(len(encoded), 5) if encoded else 1,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def addMovie(request):
    name = (request.data.get("name") or "").strip()
    director = (request.data.get("director") or "").strip()
    year_raw = (request.data.get("year") or "").strip()
    images = request.FILES.getlist("images")

    if not name or not director or not year_raw or not images:
        return Response(
            data={"error": "Fields name, year, director and images are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        year = int(year_raw)
    except ValueError:
        return Response(
            data={"error": "Year must be an integer."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    for img in images:
        if not _validate_image_dimensions(img):
            return Response(
                data={"error": f"All images must be exactly {REQUIRED_IMAGE_SIZE[0]}x{REQUIRED_IMAGE_SIZE[1]} pixels."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    hints_amount = len(images)
    difficulty_level = min(hints_amount, 5)

    if Movie.objects.filter(name=name, director=director, year=year).exists():
        return Response(
            data={"error": "A movie with this name, year and director already exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    movie = Movie.objects.create(
        name=name,
        director=director,
        year=year,
        hints_amount=hints_amount,
        difficulty_level=difficulty_level,
    )

    Frame.objects.bulk_create([
        Frame(hint_index=idx, movie=movie, image=img)
        for idx, img in enumerate(images)
    ])

    return Response(
        data={"id": movie.id, "name": movie.name, "year": movie.year, "director": movie.director},
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAdminUser])
def listMoviesAdmin(request):
    q = (request.query_params.get("q") or "").strip()

    movies = Movie.objects.all().order_by("-created")

    if q:
        movies = movies.filter(Q(name__icontains=q) | Q(director__icontains=q) | Q(year__icontains=q))

    final_images: dict[int, str] = {}
    for si in Frame.objects.filter(movie__in=movies).order_by("movie_id", "hint_index"):
        final_images[si.movie_id] = si.image.name

    data = []
    for movie in movies:
        data.append({
            "id": movie.id,
            "name": movie.name,
            "year": movie.year,
            "director": movie.director,
            "hints_amount": movie.hints_amount,
            "difficulty_level": movie.difficulty_level,
            "image_path": final_images.get(movie.id),
        })

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(["GET"])
def listMovies(request):
    movies = Movie.objects.all().order_by("-created")

    data = []
    for movie in movies:
        data.append({
            "id": movie.id,
            "name": movie.name,
            "year": movie.year,
            "director": movie.director,
        })

    return Response(data=data, status=status.HTTP_200_OK)

