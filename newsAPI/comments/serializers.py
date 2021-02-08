from django.core.exceptions import ValidationError as djangoValidationError
from rest_framework import serializers, exceptions

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    comment_author = serializers.SerializerMethodField()
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    @staticmethod
    def get_comment_author(obj):
        return str(obj.author)

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except djangoValidationError as exc:
            raise exceptions.ValidationError(exc.message)

    class Meta:
        model = Comment
        fields = "__all__"


CommentSerializer._declared_fields['children'] = CommentSerializer(
    many=True,
    source='get_children',
)


class AnswerSerializer(serializers.ModelSerializer):
    comment_author = serializers.SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    parent = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def __init__(self, *args, **kwargs):
        self.post = kwargs['data'].get('post')
        self.parent = kwargs['data'].get('parent')
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_comment_author(obj):
        return str(obj.author)

    def create(self, validated_data):
        validated_data['post'] = self.post
        validated_data['parent'] = self.parent
        return super(AnswerSerializer, self).create(validated_data)

    class Meta:
        model = Comment
        fields = ('comment_author', 'author', 'post', 'parent', 'text', 'date')





