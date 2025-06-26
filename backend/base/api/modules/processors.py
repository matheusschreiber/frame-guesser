from base.models import Run, Slide, SlideRun, SlideImage, User
from base.api.serializers import RunSerializer, SlideRunSerializer

from logging import getLogger
logger = getLogger('compslides')

class RunProcessor():
    
    def __init__(self, run_id, id_user, max_slides_per_run, max_points_per_slide_run, amount_slide_alternatives):
        self.run_id = run_id
        self.id_user = id_user
        self.max_slides_per_run = max_slides_per_run
        self.max_points_per_slide_run = max_points_per_slide_run
        self.amount_slide_alternatives = amount_slide_alternatives
        
        self.run = self._get_or_create_run()
        
    def _has_unfinished_slide_run(self):
        unfinished_slide_runs = SlideRun.objects.filter(
            run_id=self.run.id,
            has_hit=False,
            has_missed=False,
        )
        
        return unfinished_slide_runs.first() if unfinished_slide_runs.exists() else None
    
    def _get_existing_run_by_user(self):
        self.user = User.objects.filter(id=self.id_user).first()
        if not self.user:
            logger.error(f"[ERROR] User with id {self.id_user} does not exist.")
            raise Exception(f"User with id {self.id_user} does not exist.")

        user_runs = Run.objects.filter(id=self.run_id, user=self.user, slides_left__gt=0)
        for user_run in user_runs:
            slide_run = SlideRun.objects.filter(
                run_id=user_run.id, has_hit=False, has_missed=False,
            ).first()
            if slide_run:
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
                    "slides_left": self.max_slides_per_run,
                    "total_points": self.max_points_per_slide_run,
                }
            )
            
            if not new_run.is_valid():
                logger.error(f"[ERROR] Error at run creation: {new_run.errors}")
                raise Exception(new_run.errors)
            
            self.run = new_run.save()
            
        else:
            self.run = Run.objects.filter(id=self.run_id).first()
            if not self.run:
                logger.error(f"[ERROR] Run with id {self.run_id} does not exist.")
                raise Exception(f"Run with id {self.run_id} does not exist.")
        
        return self.run
        
    def _get_random_slide(self):
        if self.run.slides_left == 0:
            return None
        
        slide_runs_of_current_run = SlideRun.objects.filter(run_id=self.run.id).values_list('original_slide', flat=True)
        used_slides = Slide.objects.filter(id__in=slide_runs_of_current_run).values_list('id', flat=True)
        
        return Slide.objects.exclude(id__in=used_slides).order_by("?").first()
    
    def _get_slide_alternatives(self, current_slide):
        all_slides_random = Slide.objects.exclude(id=current_slide.id).order_by("?")[:self.amount_slide_alternatives - 1]
        slide_alternatives = [current_slide] + [slide for slide in all_slides_random]
        return slide_alternatives
    
    def _get_first_hint(self, current_slide):
        hints_from_slide = SlideImage.objects.filter(
            slide__id=current_slide.id
        ).order_by('hint_index')
        
        if not hints_from_slide.exists():
            logger.error(f"[ERROR] No hints found for slide {current_slide.id}")
            return None
        
        return hints_from_slide.first()
    
    def _get_current_hint(self):
        current_hint = SlideImage.objects.filter(
            slide__id=self.slide_run.original_slide.id
        ).order_by('hint_index')[self.slide_run.hints_used]
        
        return current_hint
    
    def _create_new_slide_run(self, current_slide):
        new_slide_run = SlideRunSerializer(
            data={
                "original_slide": current_slide.id,
                "run_id": self.run.id,
                "has_hit": 0,
                "has_missed": 0,
                "hints_used": 0,
                "points": 0,
                "slide_alternatives": [slide.id for slide in self._get_slide_alternatives(current_slide)],
            }
        )

        if not new_slide_run.is_valid():
            raise Exception(new_slide_run.errors)
        
        self.run.current_hint = self.slide_run_current_hint
        self.run.save()
        
        self.slide_run = new_slide_run.save()
        return self.slide_run
        
    def is_valid_run(self):
        if not self.run:
            return False
        
        return True
    
    def is_finished_run(self):
        return self.run.slides_left == 0
    
    def get_or_create_slide_run(self):
        self.slide_run = self._has_unfinished_slide_run()
        if self.slide_run:
            self.slide_run_current_hint = self._get_current_hint()
            return self.slide_run
        
        self.random_slide = self._get_random_slide()
        if not self.random_slide:
            return None
    
        self.slide_run_current_hint = self._get_first_hint(self.random_slide)
        if not self.slide_run_current_hint:
            return None
        
        new_slide_run = self._create_new_slide_run(self.random_slide)
        return new_slide_run
    
    def generate_response(self):
        
        return {
            "run_id": self.run.id,
            "slides_left_amount": self.run.slides_left,
            "slide_image_path": self.slide_run_current_hint.image.name,
            "hints_used": self.slide_run.hints_used,
            "hints_total": self.slide_run.original_slide.hints_amount,
            "difficulty_level": self.slide_run.original_slide.difficulty_level,
            "slide_alternatives": [alternative.prof_discipline for alternative in self.slide_run.slide_alternatives.all()],
            "slide_run_id": self.slide_run.id,
        }