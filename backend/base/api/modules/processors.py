from logging import getLogger

from base.api.serializers import MovieRunSerializer, RunSerializer
from base.models import Frame, Movie, MovieRun, Run, User

logger = getLogger('frameguesser')

class RunProcessor:
    
    def __init__(self, run_id, id_user, max_movies_per_run, max_points_per_movie_run, amount_movie_alternatives):
        self.run_id = run_id
        self.id_user = id_user
        self.max_movies_per_run = max_movies_per_run
        self.max_points_per_movie_run = max_points_per_movie_run
        self.amount_movie_alternatives = amount_movie_alternatives
        
        self.run = self._get_or_create_run()
        
    def _has_unfinished_movie_run(self):
        unfinished_movie_runs = MovieRun.objects.filter(
            run__id=self.run.id,
            has_hit=False,
            has_missed=False,
        )
        
        return unfinished_movie_runs.first() if unfinished_movie_runs.exists() else None
    
    def _get_existing_run_by_user(self):
        self.user = User.objects.filter(id=self.id_user).first()
        if not self.user:
            logger.error(f"[ERROR] User with id {self.id_user} does not exist.")
            raise Exception(f"User with id {self.id_user} does not exist.")  # noqa: TRY002

        user_runs = Run.objects.filter(id=self.run_id, user=self.user, movies_left__gt=0)
        for user_run in user_runs:
            movie_run = MovieRun.objects.filter(
                run__id=user_run.id, has_hit=False, has_missed=False,
            ).first()
            if movie_run:
                self.run = user_run
                return user_run.id
            
        return None
        
    def _get_or_create_run(self):
        
        run_id_by_user = self._get_existing_run_by_user()
        self.run_id = run_id_by_user if run_id_by_user else self.run_id
        
        if not self.run_id or self.run_id == "0":
            new_run = RunSerializer(
                data={
                    "user": self.id_user,
                    "movies_left": self.max_movies_per_run,
                    "total_points": self.max_points_per_movie_run,
                }
            )
            
            if not new_run.is_valid():
                logger.error(f"[ERROR] Error at run creation: {new_run.errors}")
                raise Exception(new_run.errors)  # noqa: TRY002
            
            self.run = new_run.save()
            
        else:
            self.run = Run.objects.filter(id=self.run_id).first()
            if not self.run:
                logger.error(f"[ERROR] Run with id {self.run_id} does not exist.")
                raise Exception(f"Run with id {self.run_id} does not exist.")  # noqa: TRY002
        
        return self.run
        
    def _get_random_movie(self):
        if self.run.movies_left == 0:
            return None
        
        movie_runs_of_current_run = MovieRun.objects.filter(run=self.run).values_list('original_movie', flat=True)
        used_movies = Movie.objects.filter(id__in=movie_runs_of_current_run).values_list('id', flat=True)
        
        return Movie.objects.exclude(id__in=used_movies).order_by("?").first()
    
    def _get_movie_alternatives(self, current_movie):
        all_movies_random = Movie.objects.exclude(id=current_movie.id).order_by("?")[:self.amount_movie_alternatives - 1]
        movie_alternatives = [current_movie] + [movie for movie in all_movies_random]
        return movie_alternatives
    
    def _get_first_hint(self, current_movie):
        hints_from_movie = Frame.objects.filter(
            movie__id=current_movie.id
        ).order_by('hint_index')
        
        if not hints_from_movie.exists():
            logger.error(f"[ERROR] No hints found for movie {current_movie.id}")
            return None
        
        return hints_from_movie.first()
    
    def _get_current_hint(self):
        current_hint = Frame.objects.filter(
            movie__id=self.movie_run.original_movie.id
        ).order_by('hint_index')[self.movie_run.hints_used]
        
        return current_hint
    
    def _create_new_movie_run(self, current_movie):
        new_movie_run = MovieRunSerializer(
            data={
                "original_movie": current_movie.id,
                "run": self.run.id,
                "has_hit": 0,
                "has_missed": 0,
                "hints_used": 0,
                "points": 0,
                "movie_alternatives": [movie.id for movie in self._get_movie_alternatives(current_movie)],
            }
        )

        if not new_movie_run.is_valid():
            raise Exception(new_movie_run.errors)  # noqa: TRY002
        
        self.run.current_hint = self.movie_run_current_hint
        self.run.save()
        
        self.movie_run = new_movie_run.save()
        return self.movie_run
        
    def is_valid_run(self):
        return bool(self.run)
    
    def is_finished_run(self):
        return self.run.movies_left == 0
    
    def get_or_create_movie_run(self):
        self.movie_run = self._has_unfinished_movie_run()
        if self.movie_run:
            self.movie_run_current_hint = self._get_current_hint()
            return self.movie_run
        
        self.random_movie = self._get_random_movie()
        if not self.random_movie:
            return None
    
        self.movie_run_current_hint = self._get_first_hint(self.random_movie)
        if not self.movie_run_current_hint:
            return None
        
        new_movie_run = self._create_new_movie_run(self.random_movie)
        return new_movie_run
    
    def generate_response(self):
        
        return {
            "run_id": self.run.id,
            "movies_left_amount": self.run.movies_left,
            "frame_path": self.movie_run_current_hint.image.name,
            "hints_used": self.movie_run.hints_used,
            "hints_total": self.movie_run.original_movie.hints_amount,
            "difficulty_level": self.movie_run.original_movie.difficulty_level,
            "movie_alternatives": [f"{alternative.name} ({alternative.year}) | {alternative.director}" for alternative in self.movie_run.movie_alternatives.all()],
            "movie_run_id": self.movie_run.id,
        }