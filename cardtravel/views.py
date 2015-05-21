# -*- coding: UTF-8  -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from cardtravel.forms import UserForm, UserProfileForm, CardForm
from cardtravel.models import UserProfile, Card


def encode(raw_url):
    return raw_url.replace(' ', '_')

def decode(cooked_url):
    return cooked_url.replace('_', ' ')

def index(request):
	context = RequestContext(request)
	return render_to_response('cardtravel/index.html', {}, context)

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
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
    	user_form = UserForm()
        profile_form = UserProfileForm()
    return render_to_response('cardtravel/register.html', {'user_form': user_form, 
    	'profile_form': profile_form, 'registered': registered}, context)

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
    args['profiles'] = UserProfile.objects.get(user=user_id)
    args['users'] = User.objects.get(id=user_id)
    return render_to_response('cardtravel/profile.html', args, context)

def view_users(request):
    context = RequestContext(request)
    args = {}
    args["profiles"] = UserProfile.objects.all()
    return render_to_response('cardtravel/users.html', args, context)

def view_cards(request):
    context = RequestContext(request)
    args = {}
    cards = Card.objects.all()
    for card in cards:
        card.country_url = encode(card.country)
        card.series_url = encode(card.series)
    args["cards"] = cards
    return render_to_response('cardtravel/cards.html', args, context)

def view_card(request, card_id):
    context = RequestContext(request)
    args = {}
    card = Card.objects.get(id=card_id)
    card.country_url = encode(card.country)
    card.series_url = encode(card.series)
    args["card"] = card
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
    return render_to_response('cardtravel/category.html', args, context)
