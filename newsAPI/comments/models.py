from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

UserModel = get_user_model()
MAX_DEPTH = 5


class Comment(MPTTModel):
    """
        Model of comments.
        parent:     parent comment, if current comment is answer of another comment.
        post:       post on which comment was left.
        author:     author of post
        text:       post's text 
        date:       date created
    """
    parent = TreeForeignKey('self',
                            related_name='child_comments',
                            on_delete=models.CASCADE,
                            blank=True,
                            null=True)
    post = models.ForeignKey('news.NewsPost', verbose_name=_('post'), related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, related_name='comments', on_delete=models.CASCADE, null=True)
    text = RichTextField(config_name='simple')
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('News Comment')
        verbose_name_plural = _('News Comments')

    def clean(self):
        # check level 
        if self.parent and self.parent.get_level() >= MAX_DEPTH:
            raise ValidationError(_('Can not add more nodes'))
        
        # post of parent comment have to be post of current comment
        if self.parent and self.parent.post != self.post:
            raise ValidationError(_('Comment must be connected with {} post'.format(self.parent.post)))

    def __str__(self):
        return f'Comment # {self.pk}'
