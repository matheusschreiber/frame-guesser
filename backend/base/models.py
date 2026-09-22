import uuid

from django.contrib.auth.models import AbstractUser  # type: ignore
from django.db import models  # type: ignore
from django.utils.deconstruct import deconstructible  # type: ignore


@deconstructible
class HashedDirectory:
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
        ordering = ['-total_points']  # noqa: RUF012

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # noqa: RUF012


class Message(models.Model):
    text = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (str(self.user) + " | " + self.text[:20])


class Movie(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    director = models.CharField(max_length=200)
    hints_amount = models.IntegerField()
    total_hits = models.IntegerField(default=0)
    total_misses = models.IntegerField(default=0)
    total_hints_used = models.IntegerField(default=0)
    difficulty_level = models.IntegerField()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " | " + f"{self.name} ({self.year}) | {self.director}"
    

class Frame(models.Model):
    hint_index = models.IntegerField(help_text="Index of the hint, starting from 0")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    image = models.ImageField(default="default_frame.jpg", upload_to=HashedDirectory('static/'))
    times_skipped = models.IntegerField(default=0, help_text="Number of times this hint was skipped")
    times_guessed_right = models.IntegerField(default=0, help_text="Number of times this hint was the one shown when the user guessed correctly")
    times_guessed_wrong = models.IntegerField(default=0, help_text="Number of times this hint was the one shown when the user guessed incorrectly")

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.hint_index) + " | " + self.movie.name


class Run(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_hint = models.ForeignKey(Frame, on_delete=models.CASCADE, null=True, blank=True)
    movies_left = models.IntegerField()
    total_points = models.FloatField(default=0.0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " | " + str(self.user)

class MovieRun(models.Model):
    original_movie = models.ForeignKey(Movie, null=True, on_delete=models.CASCADE)
    run = models.ForeignKey(Run, null=True, on_delete=models.CASCADE)
    has_hit = models.BooleanField(default=False)
    has_missed = models.BooleanField(default=False)
    hints_used = models.IntegerField(default=0)
    points = models.FloatField(default=0.0)
    movie_alternatives = models.ManyToManyField(Movie, related_name='alternatives')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " | " + str(self.run.id) + " | " + self.original_movie.name
    
class Config(models.Model):
    name = models.CharField(max_length=200, unique=True)
    value = models.CharField(max_length=200)
