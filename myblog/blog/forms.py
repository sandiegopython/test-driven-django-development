from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.post = kwargs.pop('post')   # the blog post instance
        super(CommentForm, self).__init__(*args, **kwargs)

    def save(self):
        comment = super(CommentForm, self).save(commit=False)
        comment.post = self.post
        comment.save()
        return comment

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
