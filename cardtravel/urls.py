from django.conf.urls import patterns, include, url

from cardtravel import views
from .views import IndexPageView
from .views import TradesView, TradeView, TradeListView
from .views import CardListView

urlpatterns = patterns('',

    url(r'^index/$', IndexPageView.as_view(), name = 'index'),

    url(r'^login/$', 'cardtravel.views.login', name = 'login'),
    url(r'^register/$', 'cardtravel.views.register', name = 'register'),
    url(r'^logout/$', 'cardtravel.views.logout', name = 'logout'),
    url(r'^edit/$', 'cardtravel.views.edit_profile', name = 'edit_profile'),

    url(r'^profile/(?P<user_id>\d+)/$', 'cardtravel.views.view_profile', 
        name = 'view_profile'),
    url(r'^profile/$', 'cardtravel.views.view_users', name = 'users'),
    url(r'^profile/(?P<user_id>\d+)/(?P<list_category>\w+)/$', 
        'cardtravel.views.view_cardlist', name = 'view_cardlist'),
    
    url(r'^cards/$', CardListView.as_view(), name = 'cards'),
    url(r'^cards/(?P<card_id>\d+)/$', 'cardtravel.views.view_card', 
        name = 'view_card'),
    url(r'^cards/(?P<category>\w+)/(?P<category_url>\w+)/$', 
        'cardtravel.views.view_categories', name = 'view_category'),
    url(r'^add_card/(?P<list_category>\w+)/(?P<card_id>\d+)/$', 
        'cardtravel.views.add_card', name = 'add_card'),
    url(r'^remove_card/(?P<list_category>\w+)/(?P<card_id>\d+)/$', 
        'cardtravel.views.remove_card', name = 'remove_card'),

    url(r'^trades/$', TradesView.as_view(), name = 'trades'),
    url(r'^trades/(?P<trade_id>\d+)/$', TradeView.as_view(), name = 'view_trade'),
    url(r'^trades/add/$', 'cardtravel.views.add_trade', name = 'add_trade'),
    url(r'^tradelist/(?P<user_id>\d+)/$', TradeListView.as_view(), 
        name = 'view_tradelist'),
    url(r'^trades/edit/(?P<trade_id>\d+)/$', 'cardtravel.views.edit_trade', 
        name = 'edit_trade'),
    url(r'^trades/response/(?P<trade_id>\d+)/$', 
        'cardtravel.views.response_trade', name = 'response_trade'),
)

handler404 = views.page404
handler403 = views.page403
handler500 = views.page500