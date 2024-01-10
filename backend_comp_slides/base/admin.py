from django.contrib import admin

from .models import User, Slide, SlideImage, Run, SlideRun

class SlidedRunCustomAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'original_slide',
        'has_hit',
        'has_missed',
    ]

    @admin.display()
    def user(self, obj):
        return obj.run_id.id_user

admin.site.register(Slide)
admin.site.register(User)
admin.site.register(SlideImage)
admin.site.register(Run)
admin.site.register(SlideRun, SlidedRunCustomAdmin)
