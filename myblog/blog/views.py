import datetime
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404

from .models import Entry
from .forms import CommentForm


class EntryDetail(CreateView):
    template_name = 'blog/entry_detail.html'
    form_class = CommentForm

    def get_entry(self):
        attrs = self.kwargs
        entry_date = datetime.date(
            int(attrs['year']),
            int(attrs['month']),
            int(attrs['day'])
        )
        return get_object_or_404(Entry, created_at__contains=entry_date,
                                 slug=attrs['slug'])

    def dispatch(self, *args, **kwargs):
        self.entry = self.get_entry()
        return super(EntryDetail, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EntryDetail, self).get_form_kwargs()
        kwargs['entry'] = self.entry
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs['entry'] = self.entry
        return super(EntryDetail, self).get_context_data(**kwargs)

    def get_success_url(self):
        return self.get_entry().get_absolute_url()

entry_detail = EntryDetail.as_view()
