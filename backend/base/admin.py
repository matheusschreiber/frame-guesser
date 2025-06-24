from django.contrib import admin
from base.models import *
from django.db import models

class RunCustomAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'current_hint',
        'slides_left',
        'total_points',
    ]

    search_fields = [
        'user__username',
        'user__email',
    ]

class SlidedRunCustomAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'run_id',
        'user',
        'original_slide',
        'has_hit',
        'has_missed',
        'points',
        'difficulty'
    ]

    @admin.display()
    def user(self, obj):
        return obj.run_id.user

    @admin.display()
    def difficulty(self, obj):
        return obj.original_slide.difficulty_level
    
    search_fields = [
        'run_id__user__username',
        'original_slide__prof_discipline',
        'original_slide__difficulty_level'
    ]
    
class ConfigCustomAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'value'
    ]

class UserCustomAdmin(admin.ModelAdmin):
    search_fields = [
        'username',
        'email'
    ]

class MessagesCustomAdmin(admin.ModelAdmin):
    search_fields = [
        'user__username',
        'text'
    ]
    
class MultipleSlides(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name or "MultipleSlides"
    
    class Meta:
        verbose_name_plural = "Add Multiple Slides at once"

@admin.register(MultipleSlides)
class MultipleSlidesAdmin(admin.ModelAdmin):
    list_display = ['name']
    def has_add_permission(self, request):
        return False

admin.site.register(Slide)
admin.site.register(User, UserCustomAdmin)
admin.site.register(SlideImage)
admin.site.register(Run, RunCustomAdmin)
admin.site.register(Message, MessagesCustomAdmin)
admin.site.register(Config, ConfigCustomAdmin)
admin.site.register(SlideRun, SlidedRunCustomAdmin)