from django import template

from ..models import Entry

register = template.Library()


@register.inclusion_tag('blog/_entry_history.html')
def entry_history():
    entries = Entry.objects.all()[:5]
    return {'entries': entries}
