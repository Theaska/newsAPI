from django import forms
from django.contrib import admin
from .models import Comment


class CommentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentsForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = self.fields['parent'].queryset.exclude(pk=self.instance.pk)


class CommentsAdminInline(admin.StackedInline):
    model = Comment
    extra = 0
    form = CommentsForm

    def wrap_callback(self, request, obj=None, **kwargs):
        """ Для того, чтобы в поле parent показывались только комментарии к данному посту """
        obj = obj

        def callback(field, **kwargs):
            nf = field.formfield(**kwargs)
            if field.name == 'parent':
                nf.queryset = self.model.objects.filter(post=obj)
            return nf

        return callback

    def get_formset(self, request, obj=None, **kwargs):
        kwargs.update({
            'formfield_callback': self.wrap_callback(request=request, obj=obj)
        })
        return super().get_formset(request, obj, **kwargs)
