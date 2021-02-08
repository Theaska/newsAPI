from rest_framework import serializers
from .models import NewsPost


class NewsSerializer(serializers.ModelSerializer):
    post_author = serializers.SerializerMethodField()
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    @staticmethod
    def get_post_author(obj):
        return str(obj.author)

    class Meta:
        model = NewsPost
        fields = '__all__'


