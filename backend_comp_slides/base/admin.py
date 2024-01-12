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
    ]

    @admin.display()
    def user(self, obj):
        return obj.run_id.id_user
    
class ConfigCustomAdmin(admin.ModelAdmin):
    list_display = [
        'max_points_per_slide_run',
        'max_slides_per_run'
    ]

admin.site.register(Slide)
admin.site.register(User)
admin.site.register(SlideImage)
admin.site.register(Run)
admin.site.register(Message)
admin.site.register(Config, ConfigCustomAdmin)
admin.site.register(SlideRun, SlidedRunCustomAdmin)