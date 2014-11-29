from django.conf.urls import url

from media import views

urlpatterns = [

    url(r'^video/$', views.video_index, name='video_index'),

    url(r'^audio/$', views.audio_index, name='audio_index'),

    url(r'^cartoon/$', views.cartoon_index, name='cartoon_index'),

    url(r'^video/(?P<video_id>[0-9]+)/$', views.video_detail, name='video_detail'),

    url(r'^audio/(?P<audio_id>[0-9]+)/$', views.audio_detail, name='audio_detail'),

    url(r'^cartoon/(?P<cartoon_id>[0-9]+)/$', views.cartoon_detail, name='cartoon_detail'),

    url(r'^video/search', views.video_search, name='video_search'),

    url(r'^audio/search', views.audio_search, name='audio_search'),

    url(r'^cartoon/search', views.cartoon_search, name='cartoon_search'),

    url(r'^updates/$', views.update_media, name='media_update'),
]