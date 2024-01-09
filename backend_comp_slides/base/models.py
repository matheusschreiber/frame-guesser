from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    message = models.TextField(null=True)
    hits = models.IntegerField(default=0)
    misses = models.IntegerField(default=0)
    hints_used = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-points']  # decrescent order

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Slide(models.Model):
    prof_discipline = models.CharField(max_length=300)
    hints_amount = models.IntegerField()
    hits = models.IntegerField(default=0)
    misses = models.IntegerField(default=0)
    hints_used = models.IntegerField(default=0)
    difficulty_level = models.IntegerField()
    # wrong_options = models.ForeignKey()

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
    slides_left = models.IntegerField(default=10)
    hits = models.IntegerField(default=0)
    misses = models.IntegerField(default=0)
    hints_used = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " | " + str(self.id_user)

class SlideRun(models.Model):
    original_slide = models.ForeignKey(Slide, null=True, on_delete=models.SET_NULL)
    run_id = models.ForeignKey(Run, null=True,  on_delete=models.SET_NULL)
    has_hit = models.BooleanField(default=False)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " | " + str(self.run_id.id) + " | " + self.original_slide.prof_discipline
