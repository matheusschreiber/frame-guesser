from django.contrib import admin
from django.db import models

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
    
class ZipSlides(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name or "ZipSlides"
    
    class Meta:
        verbose_name_plural = "Add a .zip file with all slides"
    
@admin.register(ZipSlides)
class ZipSlidesAdmin(admin.ModelAdmin):
    list_display = ['name']
    def has_add_permission(self, request):
        return False