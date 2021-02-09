from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions, mixins

from .serializers import NewsSerializer
from .models import NewsPost


class NewsPostListCreate(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    serializer_class = NewsSerializer
    
    def get_queryset(self):
        return NewsPost.objects.all()

    def get_permissions(self):
        permission_lst = []
        if self.action == 'create':
            permission_lst = [permissions.IsAdminUser, ]
        return [permission() for permission in permission_lst] + super().get_permissions()


class NewsPostListGetDeleteUpdate(mixins.UpdateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.DestroyModelMixin,
                                  GenericViewSet):
    serializer_class = NewsSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_queryset(self):
        return NewsPost.objects.all()

    def get_permissions(self):
        permission_lst = []
        if self.action in ('destroy', 'partial_update'):
            permission_lst = [permissions.IsAdminUser, ]
        return [permission() for permission in permission_lst] + super().get_permissions()
