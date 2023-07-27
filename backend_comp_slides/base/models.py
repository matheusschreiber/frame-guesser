from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    message = models.TextField(null=True)
    hits = models.IntegerField(null=True)
    misses = models.IntegerField(null=True)
    tips_used = models.IntegerField(null=True)
    points = models.IntegerField(null=True)

    class Meta:
        ordering = ['-points']  # decrescent order

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Slide(models.Model):
    prof_discipline = models.CharField(max_length=300)
    # images =
    tips_amount = models.IntegerField()
    hits = models.IntegerField(default=0)
    misses = models.IntegerField(default=0)
    tips_used = models.IntegerField(default=0)
    difficulty_level = models.IntegerField()

    def __str__(self):
        return self.prof_discipline
