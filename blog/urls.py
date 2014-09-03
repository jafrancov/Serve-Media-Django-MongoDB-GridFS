from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog.views',
                       url(r'^$', 'blog_index'),
                       url(r'^post/add/$', 'add_post'),
                       url(r'^post/(?P<id>\w+)/$', 'view_post'),
                       url(r'^post2/(?P<id>\w+)/$', 'view_post_th'),
                       url(r'^media/(?P<id>\w+)$', 'display_image'),
                       url(r'^media2/(?P<id>\w+)$', 'display_image_m2'),
                       )
