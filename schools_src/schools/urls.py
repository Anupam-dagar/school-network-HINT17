from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static  
from django.contrib import admin   
from django.contrib.auth import views as auth_views

from activities import views as activities_views
from authentication import views as schools_auth_views
from core import views as core_views
from search import views as search_views
from newsletter.views import (
    about, contact, home_out,
    )  
from django.contrib.auth.views import (
    password_reset,
    password_reset_done,
    password_reset_confirm, 
    password_reset_complete,  
    )
  
 
urlpatterns = [      
  
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', core_views.home , name='home'),
    url(r'^mission_ajax/', include('mission_ajax.urls', namespace='ajax')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^login', auth_views.login, {'template_name': 'core/cover.html'},
        name='login'), 
    url(r'^logout', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^signup/teachers$', schools_auth_views.signup_teachers, name='signup_teachers'),
    url(r'^signup/students$', schools_auth_views.signup_human, name='signup_human'),
    url(r'^signup/colleges$', schools_auth_views.signup_products, name='signup_products'),    
    
    url(r'^password_reset/$', password_reset, name='password_reset'),
    url(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', password_reset_complete, name='password_reset_complete'),


    url(r'^contact/$', contact, name='contact'),
    url(r'^about/$', about, name='about'),
    url(r'^introho/$', core_views.introho, name='introho'),
    url(r'^settings/human/$', core_views.settings_human, name='settings_human'),
    url(r'^settings/products/$', core_views.settings_products, name='settings_products'),
    url(r'^settings/picture/$', core_views.picture, name='picture'),
    # url(r'^settings/upload_picture/$', core_views.upload_picture,
    #     name='upload_picture'), 
    # url(r'^settings/save_uploaded_picture/$', core_views.save_uploaded_picture,
    #     name='save_uploaded_picture'),
    url(r'^settings/profile_pic_upload/$', core_views.profile_pic_upload, name='profile_pic_upload'),
    url(r'^settings/password/$', core_views.password, name='password'),

    url(r'^network/$', core_views.network, name='network'),
    url(r'^feeds/', include('feeds.urls')),
    url(r'^notifications/$', activities_views.notifications,
        name='notifications'), 
    url(r'^notifications/last/$', activities_views.last_notifications,
        name='last_notifications'),
    url(r'^notifications/check/$', activities_views.check_notifications,
        name='check_notifications'),
    url(r'^search/$', search_views.search, name='search'),
    url(r'^searchusers/$', search_views.searchusers, name='searchusers'),
    url(r'^(?P<username>[^/]+)/$', core_views.profile, name='profile'),
    url(r'^(?P<username>[^/]+)/likers/$', core_views.profile_likers, name='profile_likers'),
    url(r'^(?P<username>[^/]+)/likesto/$', core_views.likes_to, name='likes_to'),
    url(r'^(?P<username>[^/]+)/activities/$', core_views.userfeeds, name='userfeeds'),
    url(r'^like/$', core_views.profile, name='profile_like'),
    url(r'^(?P<username>[^/]+)/$', core_views.profile_unlike, name='profile_unlike'),
    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
