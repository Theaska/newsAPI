from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('api_auth.urls')),
    path('news/', include('news.urls')),
    path('comments/', include('comments.urls')),
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
