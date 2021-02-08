from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status

from .models import Comment
from .serializers import CommentSerializer, AnswerSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    answer_serializer_class = AnswerSerializer

    def get_serializer_class(self):
        if self.action != 'answer':
            return self.serializer_class
        else:
            return self.answer_serializer_class

    def get_queryset(self):
        return Comment.objects.all()

    def answer(self, request, *args, **kwargs):
        data = request.data
        comment = self.get_object()
        data['post'] = comment.post
        data['parent'] = comment
        return self.create_answer(data)

    def create_answer(self, data):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        permissions_lst = []
        if self.action in ('create', 'answer'):
            permissions_lst.append(permissions.IsAuthenticated)
        return [permission() for permission in permissions_lst] + super().get_permissions()
