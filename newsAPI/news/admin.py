from django.contrib import admin
from .models import NewsPost
from comments.admin import CommentsAdminInline


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    inlines = (CommentsAdminInline, )

