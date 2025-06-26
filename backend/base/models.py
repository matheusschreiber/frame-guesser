from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid

@deconstructible
class HashedDirectory():
    def __init__(self, diretorio):
        self.diretorio = f"{diretorio}/"

    def __call__(self, instance, filename):
        extension = filename.split('.')[-1]
        new_filename = f"{uuid.uuid4()}.{extension}"
        return f"{self.diretorio}/{new_filename}"

class User(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    total_hits = models.IntegerField(default=0)
    total_misses = models.IntegerField(default=0)
    total_hints_used = models.IntegerField(default=0)
    total_points = models.FloatField(default=0.0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-total_points']

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Message(models.Model):
    text = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (str(self.user) + " | " + self.text[:20])


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
    hint_index = models.IntegerField(help_text="Index of the hint, starting from 0")
    slide = models.ForeignKey(Slide, on_delete=models.CASCADE)
    image = models.ImageField(default="default_slide.jpg", upload_to=HashedDirectory('static/'))

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.hint_index) + " | " + self.slide.prof_discipline


class Run(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_hint = models.ForeignKey(SlideImage, on_delete=models.CASCADE, null=True, blank=True)
    slides_left = models.IntegerField()
    total_points = models.FloatField(default=0.0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " | " + str(self.user)

class SlideRun(models.Model):
    original_slide = models.ForeignKey(Slide, null=True, on_delete=models.CASCADE)
    run_id = models.ForeignKey(Run, null=True,  on_delete=models.CASCADE)
    has_hit = models.BooleanField(default=False)
    has_missed = models.BooleanField(default=False)
    hints_used = models.IntegerField(default=0)
    points = models.FloatField(default=0.0)
    slide_alternatives = models.ManyToManyField(Slide, related_name='alternatives')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " | " + str(self.run_id.id) + " | " + self.original_slide.prof_discipline
    
class Config(models.Model):
    name = models.CharField(max_length=200, unique=True)
    value = models.CharField(max_length=200)
