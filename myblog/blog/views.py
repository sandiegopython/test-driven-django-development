from django.views.generic import DetailView, CreateView
from django.shortcuts import get_object_or_404
from .models import Post
from .forms import CommentForm



class PostDetails(DetailView):
    model = Post

post_details = PostDetails.as_view()

class CreateComment(CreateView):
    template_name = 'blog/create_comment.html'
    form_class = CommentForm
    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs['blog_pk'])

    def get_form_kwargs(self):
        kwargs = super(CreateComment, self).get_form_kwargs()
        kwargs['post'] = self.get_post()
        return kwargs
    def get_success_url(self):
        return self.get_post().get_absolute_url()

create_comment = CreateComment.as_view()

