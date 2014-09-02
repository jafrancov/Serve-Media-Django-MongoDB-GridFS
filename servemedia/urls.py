from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^blog/', include('blog.urls')),
                       )
