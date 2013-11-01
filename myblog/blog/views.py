from django.views.generic import DetailView
from .models import Post


class PostDetails(DetailView):
    model = Post

post_details = PostDetails.as_view()