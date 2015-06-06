from django.conf.urls import patterns, include, url

from cardtravel.views import IndexPageView, TradesView, TradeView, AddTradeView

urlpatterns = patterns('',

    url(r'^index/$', IndexPageView.as_view(), name = 'index'),

    url(r'^login/$', 'cardtravel.views.login', name = 'login'),
    url(r'^register/$', 'cardtravel.views.register', name = 'register'),
    url(r'^logout/$', 'cardtravel.views.logout', name = 'logout'),
    url(r'^edit/$', 'cardtravel.views.edit_profile', name = 'edit_profile'),

    url(r'^profile/(?P<user_id>\d+)/$', 'cardtravel.views.view_profile'),
    url(r'^profile/$', 'cardtravel.views.view_users', name = 'users'),
    url(r'^profile/page/(\d+)/$', 'cardtravel.views.view_users', name = 'users'),
    url(r'^profile/(?P<user_id>\d+)/(?P<list_category>\w+)/$', 
        'cardtravel.views.view_cardlist'),

    url(r'^cards/$', 'cardtravel.views.view_cards', name = 'cards'),
    url(r'^cards/page/(\d+)/$', 'cardtravel.views.view_cards', name = 'cards'),
    url(r'^cards/(?P<card_id>\d+)/$', 'cardtravel.views.view_card'),
    url(r'^cards/(?P<category>\w+)/(?P<category_url>\w+)/$', 
        'cardtravel.views.view_categories'),
    url(r'^add_card/(?P<list_category>\w+)/(?P<card_id>\d+)/$', 
        'cardtravel.views.add_card'),
    url(r'^remove_card/(?P<list_category>\w+)/(?P<card_id>\d+)/$', 
        'cardtravel.views.remove_card'),

    url(r'^trades/$', TradesView.as_view(), name = 'trades'),
    url(r'^trades/page/(?P<page_number>\d+)/$', TradesView.as_view(), name = 'trades'),
    url(r'^trades/(?P<trade_id>\d+)/$', TradeView.as_view()),
    url(r'^trades/add/$', AddTradeView.as_view(), name = 'add_trade'),
)