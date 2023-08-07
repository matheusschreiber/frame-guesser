from django.contrib import admin

# Register your models here.

from .models import User, Slide, SlideImages

admin.site.register(Slide)
admin.site.register(User)
admin.site.register(SlideImages)
