from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.entry = kwargs.pop('entry')   # the blog entry instance
        super(CommentForm, self).__init__(*args, **kwargs)

    def save(self):
        comment = super(CommentForm, self).save(commit=False)
        comment.entry = self.entry
        comment.save()
        return comment

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
