from django.contrib import admin

from base.fake_models import *
from base.models import *

@admin.register(Run)
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
    
@admin.register(Slide)
class SlideCustomAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'prof_discipline',
        'hints_amount',
        'total_hits',
        'total_misses',
        'total_hints_used',
        'difficulty_level'
    ]

    search_fields = [
        'prof_discipline',
        'difficulty_level'
    ]

@admin.register(SlideImage)
class SlideImageCustomAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'slide',
        'hint_index',
        'image'
    ]

    search_fields = [
        'slide__prof_discipline',
        'slide__difficulty_level',
        'hint_index'
    ]

@admin.register(SlideRun)
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
    
@admin.register(Config)
class ConfigCustomAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'value'
    ]

@admin.register(User)
class UserCustomAdmin(admin.ModelAdmin):
    search_fields = [
        'username',
        'email'
    ]

@admin.register(Message)
class MessagesCustomAdmin(admin.ModelAdmin):
    search_fields = [
        'user__username',
        'text'
    ]