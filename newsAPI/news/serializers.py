from rest_framework import serializers

from comments.serializers import CommentSerializer
from .models import NewsPost


class NewsSerializer(serializers.ModelSerializer):
    post_author = serializers.SerializerMethodField()
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    root_comments = CommentSerializer(many=True, source='comments', read_only=True)

    @staticmethod
    def get_post_author(obj):
        return str(obj.author)

    class Meta:
        model = NewsPost
        fields = '__all__'


