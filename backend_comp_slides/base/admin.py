from django.contrib import admin

from .models import *

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
    
class ConfigCustomAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'value'
    ]

admin.site.register(Slide)
admin.site.register(User)
admin.site.register(SlideImage)
admin.site.register(Run)
admin.site.register(Message)
admin.site.register(Config, ConfigCustomAdmin)
admin.site.register(SlideRun, SlidedRunCustomAdmin)