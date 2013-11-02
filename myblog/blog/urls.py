from django.conf.urls import patterns, url


urlpatterns = patterns('blog.views',
    url(r'^post/(?P<pk>\d+)/$', 'post_details'),
    url(r'^comment/(?P<blog_pk>\d+)/$', 'create_comment'),
)


