from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from .serializers import NewsSerializer
from .models import NewsPost


class NewsPostViewSet(ModelViewSet):
    serializer_class = NewsSerializer
    
    def get_queryset(self):
        return NewsPost.objects.all()

    def get_permissions(self):
        permission_lst = []
        if self.action in ('destroy', 'create'):
            permission_lst = [permissions.IsAdminUser, ]
        return [permission() for permission in permission_lst] + super().get_permissions()


