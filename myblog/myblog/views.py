from django.views.generic import ListView

from blog.models import Post


class HomeView(ListView):
    template_name = 'index.html'
    queryset = Post.objects.order_by('-created_at')

home = HomeView.as_view()
