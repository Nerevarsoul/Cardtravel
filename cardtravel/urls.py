from django.conf.urls import patterns, include, url
#import cardtravel.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^index/$', 'cardtravel.views.index', name = 'index'),

    url(r'^login/$', 'cardtravel.views.login', name = 'login'),
    url(r'^register/$', 'cardtravel.views.register', name = 'register'),
    url(r'^logout/$', 'cardtravel.views.logout', name = 'logout'),

    url(r'^profile/(?P<user_id>\d+)/$', 'cardtravel.views.view_profile', name = 'profile'),
    url(r'^profile/$', 'cardtravel.views.view_users', name = 'users'),

    url(r'^cards/$', 'cardtravel.views.view_cards', name = 'cards'),
    url(r'^cards/(?P<card_id>\d+)/$', 'cardtravel.views.view_card', name = 'card'),
    url(r'^cards/(?P<category>\w+)/(?P<category_url>\w+)/$', 'cardtravel.views.view_categories', name = 'categories'),
)