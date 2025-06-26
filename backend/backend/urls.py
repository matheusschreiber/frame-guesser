from django.contrib import admin
from django.urls import path, include
from base.api.admin_views import add_slides_view, add_zip_view

urlpatterns = [
    path('admin/base/multipleslides/', add_slides_view, name='add_slides_view'),
    path('admin/base/zipslides/', add_zip_view, name='add_zip_view'),
    path("admin/", admin.site.urls),
    path("api/", include("base.api.urls")),
]
