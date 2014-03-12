from . import models


def prev_posts(request):
    return {'prev_posts': models.Post.objects.all()[:20]}
