from django.conf.urls import url

from feeds import views  
     # (?P<id>\d+)/ 
urlpatterns = [    
    url(r'^$', views.feeds, name='feeds'),
    url(r'^(?P<id>\d+)/$', views.feed, name='feeds'),
    url(r'^challenge/(?P<id>\d+)/$', views.specialfeeds, name='special_feeds'),
    url(r'^people/$', views.profilefeeds, name='profilefeeds'),    
    url(r'^products/$', views.product_profilefeeds, name='product_profilefeeds'),    
    # url(r'^challenge/(?P<id>\d+)/$', views.specific_challenge_feeds, name='specific_challenge_feeds'),    
    url(r'^challenge/$', views.challengefeeds, name='challenge_feeds'),
    url(r'^new_post/$', views.new_post, name='new_post'),
    url(r'^post/$', views.post, name='post'),
    url(r'^like/$', views.like, name='like'),
    url(r'^profile_like/$', views.profile_like, name='profile_like'),    
    url(r'^comment/$', views.comment, name='comment'),  
    url(r'^load/$', views.load, name='load'), 
    url(r'^check/$', views.check, name='check'), 
    url(r'^load_new/$', views.load_new, name='load_new'),
    url(r'^update/$', views.update, name='update'),
    url(r'^profile_update/$', views.profile_update, name='profile_update'),    
    url(r'^track_comments/$', views.track_comments, name='track_comments'),
    url(r'^remove/$', views.remove, name='remove_feed'),
    url(r'^(\d+)/$', views.feed, name='feed'),
] 
      