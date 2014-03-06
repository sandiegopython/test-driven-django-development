from django import template

from ..models import Post

register = template.Library()

@register.inclusion_tag('blog/templatetags/entry_history.html')
def entry_history():
    posts = Post.objects.all()[:10]
    return {'posts': posts}
