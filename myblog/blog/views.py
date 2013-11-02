from django.views.generic import CreateView
from django.shortcuts import get_object_or_404
from .models import Post
from .forms import CommentForm


class PostDetails(CreateView):
    template_name = 'blog/post_detail.html'
    form_class = CommentForm

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def dispatch(self, *args, **kwargs):
        self.blog_post = self.get_post()
        return super(PostDetails, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PostDetails, self).get_form_kwargs()
        kwargs['post'] = self.blog_post
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs['post'] = self.blog_post
        return super(PostDetails, self).get_context_data(**kwargs)

    def get_success_url(self):
        return self.get_post().get_absolute_url()

post_details = PostDetails.as_view()
