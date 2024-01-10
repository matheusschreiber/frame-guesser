from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    message = models.TextField(null=True)
    total_hits = models.IntegerField(default=0)
    total_misses = models.IntegerField(default=0)
    total_hints_used = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-total_points']  # decrescent order

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Slide(models.Model):
    prof_discipline = models.CharField(max_length=300)
    hints_amount = models.IntegerField()
    total_hits = models.IntegerField(default=0)
    total_misses = models.IntegerField(default=0)
    total_hints_used = models.IntegerField(default=0)
    difficulty_level = models.IntegerField()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " | " + self.prof_discipline


class SlideImage(models.Model):
    hint_index = models.IntegerField()
    slide = models.ForeignKey(Slide, on_delete=models.CASCADE)
    image = models.ImageField(default="default_slide.jpg", upload_to='static/')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.hint_index) + " | " + self.slide.prof_discipline


class Run(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_hint = models.ForeignKey(SlideImage, on_delete=models.CASCADE)
    slides_left = models.IntegerField()
    total_points = models.IntegerField(default=0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " | " + str(self.id_user)

class SlideRun(models.Model):
    original_slide = models.ForeignKey(Slide, null=True, on_delete=models.CASCADE)
    run_id = models.ForeignKey(Run, null=True,  on_delete=models.CASCADE)
    has_hit = models.BooleanField(default=False)
    has_missed = models.BooleanField(default=False)
    hints_used = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    slide_alternatives = models.ManyToManyField(Slide, related_name='alternatives')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " | " + str(self.run_id.id) + " | " + self.original_slide.prof_discipline
    
class Config(models.Model):
    max_points_per_slide_run = models.IntegerField(default=5)
    max_slides_per_run = models.IntegerField(default=10)
