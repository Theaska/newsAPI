from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status

from helpers.send_notification import send_notification
from .models import Comment
from .serializers import CommentSerializer, AnswerSerializer
from api_auth.permissions import IsNotBanned


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    answer_serializer_class = AnswerSerializer

    def get_serializer_class(self):
        if self.action != 'answer':
            return self.serializer_class
        else:
            return self.answer_serializer_class

    def get_queryset(self):
        if self.action == 'list':
            # show in list only root comments with included children
            return Comment.objects.filter(parent=None)
        else:
            return Comment.objects.all()

    def answer(self, request, *args, **kwargs):
        """ Create answer to current comment """
        data = request.data
        comment = self.get_object()
        data['post'] = comment.post
        data['parent'] = comment
        return self.create_answer(data)

    def create_answer(self, data):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        main_comment = self.get_object()
        new_comment = serializer.save()
        receiver_email = main_comment.author.email if main_comment.author else None
        if receiver_email and new_comment.author != main_comment.author:
            send_notification(template_name='comments/new_answer_to_comment.html',
                              subject='New answer to your comment',
                              receivers=[receiver_email, ],
                              context={'comment': new_comment})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        permissions_lst = []
        if self.action in ('create', 'answer'):
            permissions_lst = [permissions.IsAuthenticated, IsNotBanned]
        if self.action == 'destroy':
            permissions_lst.append(permissions.IsAdminUser)
        return [permission() for permission in permissions_lst] + super().get_permissions()

