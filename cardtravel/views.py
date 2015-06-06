# -*- coding: UTF-8  -*-
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.views.generic.base import TemplateView


from cardtravel.forms import UserForm, UserProfileForm, CardForm, EditProfileForm
from cardtravel.models import UserProfile, Card, WishList, Collection, Trade


def encode(raw_url):
    return raw_url.replace(' ', '_')

def decode(cooked_url):
    return cooked_url.replace('_', ' ')

def gain_userlist(user):
    user_profile = UserProfile.objects.get(user=user)
    args = {}
    args['user_wishlist'] = user_profile.get_wishlist()
    args['user_collection'] = user_profile.get_collection()
    return args


class IndexPageView(TemplateView):
    template_name = "cardtravel/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context['profiles'] = UserProfile.objects.all().order_by('-id')[:3]
        context['trades'] = Trade.objects.all().order_by('-date')[:3]
        context['cards'] = Card.objects.all().order_by('-id')[:3]
        return context


def register(request):
    context = RequestContext(request)
    registered = False
    if request.POST:
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            wishlist = WishList(user=user)
            wishlist.save()
            collection = Collection(user=user)
            collection.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
    	user_form = UserForm()
        profile_form = UserProfileForm()
    return render_to_response('cardtravel/register.html', {'user_form': user_form, 
    	'profile_form': profile_form, 'registered': registered}, context)

@login_required
def edit_profile(request):
    context = RequestContext(request)
    user = request.user
    profile = UserProfile.objects.get(user=user)
    if request.POST:
        editprofile_form = EditProfileForm(data=request.POST)
        if editprofile_form.is_valid() and editprofile_form.has_changed():
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.save()
            profile.adress = request.POST['adress']
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
        else:
            editprofile_form.errors
    else:
        editprofile_form = EditProfileForm(initial={
                                            'username': user.username, 
                                            'email': user.email,
                                            'adress': profile.adress,
                                            'picture': profile.picture})
    return render_to_response('cardtravel/edit_profile.html', 
        {'editprofile_form': editprofile_form}, context)        

def login(request):
    context = RequestContext(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/index/')
        else:
            return HttpResponse("Your Rango account is disabled.")
    else:
        return render_to_response('cardtravel/login.html', {}, context)

def logout(request):
    auth.logout(request)
    return redirect('/index/')

@login_required
def view_profile(request, user_id):
    context = RequestContext(request)
    args = {}
    user_profile = UserProfile.objects.get(user=user_id)
    args['profiles'] = user_profile
    args['users'] = User.objects.get(id=user_id)
    args['wishlist'] = user_profile.get_wishlist()
    args['collection'] = user_profile.get_collection()

    if request.user.id != user_id:
        args.update(gain_userlist(request.user))
    else:
        args['user_wishlist'] = args['wishlist']
        args['user_collection'] = args['collection']

    args['wishlist'] = args['wishlist'][0:3]
    args['collection'] = args['collection'][0:3]

    return render_to_response('cardtravel/profile.html', args, context)

def view_users(request, page_number=1):
    context = RequestContext(request)
    args = {}
    profiles = UserProfile.objects.all()
    current_page = Paginator(profiles, 6)
    return render_to_response('cardtravel/users.html', {"profiles": current_page.page(page_number)}, context)


def view_cards(request, page_number=1):
    context = RequestContext(request)
    args = {}
    cards = Card.objects.all()
    for card in cards:
        card.country_url = encode(card.country)
        card.series_url = encode(card.series)
    args.update(gain_userlist(request.user))
    current_page = Paginator(cards, 6)
    args["cards"] = current_page.page(page_number)
    return render_to_response('cardtravel/cards.html', args, context)

def view_card(request, card_id):
    context = RequestContext(request)
    args = {}
    card = Card.objects.get(id=card_id)
    card.country_url = encode(card.country)
    card.series_url = encode(card.series)
    args["card"] = card
    args.update(gain_userlist(request.user))
    return render_to_response('cardtravel/cardview.html', args, context)

def view_categories(request, category, category_url):
    context = RequestContext(request)
    args = {}
    cur_category = decode(category_url)
    args["category"] = category
    args["category_url"] = category_url
    args["cur_category"] = cur_category
    if category == 'country':
        cards = Card.objects.filter(country=cur_category)
    elif category == 'series': 
        cards = Card.objects.filter(series=cur_category)
    elif category == 'year':
        cards = Card.objects.filter(issued_on=int(cur_category))
    for card in cards:
        card.country_url = encode(card.country)
        card.series_url = encode(card.series)
    args["cards"] = cards
    args.update(gain_userlist(request.user))
    return render_to_response('cardtravel/category.html', args, context)

def view_cardlist(request, user_id, list_category):
    context = RequestContext(request)
    args = {}
    user_profile = UserProfile.objects.get(user=user_id)
    args['users'] = User.objects.get(id=user_id)
    args['list_category'] = list_category
    if list_category == 'wishlist':
        args['cards'] = user_profile.get_wishlist()
    elif list_category == 'collection':
        args['cards'] = user_profile.get_collection()
    if request.user.id != user_id:
        args.update(gain_userlist(request.user))
    return render_to_response('cardtravel/cardlist.html', args, context)

def add_card(request, list_category, card_id):
    context = RequestContext(request)
    card = Card.objects.get(id=card_id)
    if list_category == 'wishlist':
        cards = WishList.objects.get(user=request.user).wishlist
        cards.add(card)
    elif list_category == 'collection':
        cards = Collection.objects.get(user=request.user).collectionlist
        cards.add(card)
    return redirect('/index/')

def remove_card(request, list_category, card_id):
    context = RequestContext(request)
    card = Card.objects.get(id=card_id)
    if list_category == 'wishlist':
        cards = WishList.objects.get(user=request.user).wishlist
        cards.remove(card)
    elif list_category == 'collection':
        cards = Collection.objects.get(user=request.user).collectionlist
        cards.remove(card)
    return redirect('/index/')


class TradesView(TemplateView):
    template_name = "cardtravel/trades.html"

    def get_context_data(self, page_number=1, **kwargs):
        context = super(TradesView, self).get_context_data(**kwargs)
        trades = Trade.objects.all()
        current_page = Paginator(trades, 4)
        context['trades'] = current_page.page(page_number)
        return context

class TradeView(TemplateView):
    template_name = "cardtravel/trade.html"

    def get_context_data(self, trade_id, **kwargs):
        context = super(TradeView, self).get_context_data(**kwargs)
        context['trade'] = Trade.objects.get(id=trade_id)
        return context
