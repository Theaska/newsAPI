from django.core.exceptions import ValidationError as djangoValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

from .models import Comment, MAX_DEPTH


class CommentSerializer(serializers.ModelSerializer):
    comment_author = serializers.SerializerMethodField()
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    children = serializers.SerializerMethodField()

    @staticmethod
    def get_comment_author(obj):
        return str(obj.author)

    def get_children(self, obj):
        return type(self)(obj.get_children(), many=True).data

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except djangoValidationError as exc:
            raise exceptions.ValidationError(exc.message)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'parent', 'author', 'comment_author', 'text', 'date', 'children')


class AnswerSerializer(serializers.ModelSerializer):
    comment_author = serializers.SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    parent = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._post = kwargs['data'].get('post')
        self._parent = kwargs['data'].get('parent')

    @staticmethod
    def get_comment_author(obj):
        return str(obj.author)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if self._parent and self._parent.get_level() >= MAX_DEPTH:
            raise ValidationError(_('Can not add more answer to this comment'))
        attrs['parent'] = self._parent
        attrs['post'] = self._post
        return attrs

    class Meta:
        model = Comment
        fields = ('id', 'comment_author', 'author', 'post', 'parent', 'text', 'date')





