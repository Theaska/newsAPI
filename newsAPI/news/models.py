from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

UserModel = get_user_model()


class NewsPost(models.Model):
    author = models.ForeignKey(UserModel, related_name='news_posts', on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=128)
    slug = models.SlugField(_('slug'), unique=True)
    text = RichTextField(config_name='default')
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('News Post')
        verbose_name_plural = _('News Posts')
        ordering = ('-date', )

    def __str__(self):
        return self.title

