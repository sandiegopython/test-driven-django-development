from django.conf.urls import patterns, url


urlpatterns = patterns('blog.views',
    url(r'^(?P<pk>\d+)/$', 'entry_detail'),
)
