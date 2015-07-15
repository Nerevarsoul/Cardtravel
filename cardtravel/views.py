# -*- coding: UTF-8  -*-
from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator


from .forms import UserForm, UserProfileForm, CardForm, EditProfileForm, TradeForm
from .models import UserProfile, Card, WishList, Collection, Trade


def decode_url(cooked_url):
    return cooked_url.replace('_', ' ')

def gain_userlist(user):
    args = {}
    if user.is_authenticated():
        user_profile = UserProfile.objects.get(user=user)
        args['user_wishlist'] = user_profile.get_wishlist()
        args['user_collection'] = user_profile.get_collection()
    return args


class IndexPageView(TemplateView):
    template_name = "cardtravel/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data(**kwargs)
        context['profiles'] = UserProfile.objects.order_by('-id')[:3]
        context['trades'] = Trade.objects.order_by('-date')[:3]
        cards = Card.objects.order_by('-id')[:3]
        context['cards'] = cards
        context.update(gain_userlist(self.request.user))
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
            return redirect('view_profile', user.id)
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
    wishlist = user_profile.get_wishlist()
    collection = user_profile.get_collection()
    if request.user.id != user_id:
        args.update(gain_userlist(request.user))
    else:
        args['user_wishlist'] = args['wishlist']
        args['user_collection'] = args['collection']

    args['wishlist'] = wishlist[0:3]
    args['collection'] = collection[0:3]
    args['trades'] = Trade.objects.filter(user=user_id)[0:3]

    return render_to_response('cardtravel/profile.html', args, context)

def view_users(request):
    context = RequestContext(request)
    args = {}
    args['profiles'] = UserProfile.objects.all()
    return render_to_response('cardtravel/users.html', args, context)


class CardMixin(ListView):

    model = Card
    queryset = Card.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(CardMixin, self).get_context_data(**kwargs)
        cards = Card.objects.all()
        countries = []
        series = []
        years = []
        for card in cards:
            if card.country not in countries:
                countries.append(card.country)
            if card.series not in series:
                series.append(card.series)
            if card.issued_on not in years:
                years.append(card.issued_on)
        countries.sort()
        series.sort()
        years.sort()
        context["countries"] = countries
        context["series"] = series
        context["years"] = years
        context['cards'] = self.queryset
        context.update(gain_userlist(self.request.user))
        return context

class CardsView(CardMixin, ListView):
    template_name = 'cardtravel/cards.html'


class CardCategoryView(CardMixin, ListView):
    template_name = 'cardtravel/cards.html'

    def get_context_data(self, **kwargs):
        context = super(CardCategoryView, self).get_context_data(**kwargs)
        context.update({"category": self.kwargs['category'], 
            "cur_category": decode_url(self.kwargs['category_url'])})
        return context

    def get_queryset(self):
        category = self.kwargs['category']
        cur_category = decode_url(self.kwargs['category_url'])
        if category == 'country':
            self.queryset = Card.objects.filter(country=cur_category)
        elif category == 'series': 
            self.queryset = Card.objects.filter(series=cur_category)
        elif category == 'year':
            self.queryset = Card.objects.filter(issued_on=int(cur_category))
        return self.queryset

def view_card(request, card_id):
    context = RequestContext(request)
    args = {}
    card = Card.objects.get(id=card_id)
    args["card"] = card
    args.update(gain_userlist(request.user))
    return render_to_response('cardtravel/cardview.html', args, context)


class CardView(ListView):

    template_name = 'cardtravel/cardview.html'

    def get_context_data(self, **kwargs):
        context = super(CardView, self).get_context_data(**kwargs)
        context.update(gain_userlist(self.request.user))
        context["card"] = self.queryset
        return context

    def get_queryset(self):
        self.queryset = Card.objects.get(id=self.kwargs['card_id'])
        return self.queryset


class CardListView(ListView):
    template_name = 'cardtravel/cardlist.html'

    def get_context_data(self, **kwargs):
        context = super(CardListView, self).get_context_data(**kwargs)
        context.update({'users': User.objects.get(id=self.kwargs['user_id']),
            'list_category': self.kwargs['list_category']})
        if self.request.user.id != self.kwargs['user_id']:
            context.update(gain_userlist(self.request.user))
        context['cards'] = self.queryset
        return context

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.kwargs['user_id'])
        list_category = self.kwargs['list_category']
        if list_category == 'wishlist':
            self.queryset = user_profile.get_wishlist()
        elif list_category == 'collection':
            self.queryset = user_profile.get_collection()
        return self.queryset


def add_card(request, list_category):
    context = RequestContext(request)
    if request.method == "POST":
        card_id = int(request.POST['card_id'])
        card = Card.objects.get(id=card_id)
        if list_category == 'wishlist':
            cards = WishList.objects.get(user=request.user).wishlist
            cards.add(card)
        elif list_category == 'collection':
            cards = Collection.objects.get(user=request.user).collectionlist
            cards.add(card)
        messages.add_message(request, messages.SUCCESS, 'You add card')
    return redirect(request.META.get('HTTP_REFERER'))

def remove_card(request, list_category):
    context = RequestContext(request)
    if request.method == "POST":
        card_id = int(request.POST['card_id'])
        card = Card.objects.get(id=card_id)
        if list_category == 'wishlist':
            cards = WishList.objects.get(user=request.user).wishlist
            cards.remove(card)
        elif list_category == 'collection':
            cards = Collection.objects.get(user=request.user).collectionlist
            cards.remove(card)
        messages.add_message(request, settings.DELETE_MESSAGES, 'You delete card')
    return redirect(request.META.get('HTTP_REFERER'))


class TradesView(TemplateView):
    template_name = "cardtravel/trades.html"

    def get_context_data(self, **kwargs):
        context = super(TradesView, self).get_context_data(**kwargs)
        context['trades'] = Trade.objects.all()
        return context

class TradeListView(TemplateView):
    template_name = "cardtravel/tradelist.html"

    def get_context_data(self, user_id, **kwargs):
        context = super(TradeListView, self).get_context_data(**kwargs)
        context['trades'] = Trade.objects.filter(user=user_id)
        context['current_user'] = User.objects.get(id=user_id)
        return context

class TradeView(TemplateView):
    template_name = "cardtravel/trade.html"

    def get_context_data(self, trade_id, **kwargs):
        context = super(TradeView, self).get_context_data(**kwargs)
        context['trade'] = Trade.objects.get(id=trade_id)
        return context

@login_required
def add_trade(request):
    context = RequestContext(request)
    if request.POST:
        trade_form = TradeForm(request.POST, request.FILES)
        if trade_form.is_valid():
            trade = trade_form
            if 'face_picture' in request.FILES:
                trade.face_picture = request.FILES['face_picture']
            if 'reverse_picture' in request.FILES:
                trade.reverse_picture = request.FILES['reverse_picture']
            if 'addiction_picture1' in request.FILES:
                trade.addiction_picture1 = request.FILES['addiction_picture1']
            if 'addiction_picture2' in request.FILES:
                trade.addiction_picture2 = request.FILES['addiction_picture2']
            if 'addiction_picture3' in request.FILES:
                trade.addiction_picture3 = request.FILES['addiction_picture3']
            trade.save()
        else:
            trade_form.errors
    else:
        trade_form = TradeForm(initial={'user': request.user})
                                             
    return render_to_response('cardtravel/add_trade.html', 
        {'trade_form': trade_form}, context)

@login_required
def edit_trade(request, trade_id):
    context = RequestContext(request)
    trade = Trade.objects.get(id=trade_id)
    context['trade'] = trade
    if request.POST:
        trade_form = TradeForm(request.POST, request.FILES)
        if trade_form.is_valid() and trade_form.has_changed():
            card_id = request.POST['card']
            trade.card = Card.objects.get(id=card_id)
            trade.condition = request.POST['condition']
            trade.description = request.POST['description']
            if 'face_picture' in request.FILES:
                trade.face_picture = request.FILES['face_picture']
            if 'reverse_picture' in request.FILES:
                trade.reverse_picture = request.FILES['reverse_picture']
            if 'addiction_picture1' in request.FILES:
                trade.addiction_picture1 = request.FILES['addiction_picture1']
            if 'addiction_picture2' in request.FILES:
                trade.addiction_picture2 = request.FILES['addiction_picture2']
            if 'addiction_picture3' in request.FILES:
                trade.addiction_picture3 = request.FILES['addiction_picture3']
            trade.save()
        else:
            trade_form.errors
    else:
        trade_form = TradeForm(initial={'user': trade.user,
                                        'card': trade.card,
                                        'condition': trade.condition,
                                        'description': trade.description,
                                        'face_picture': trade.face_picture,
                                        'reverse_picture': trade.reverse_picture, 
                                        'addiction_picture1': trade.addiction_picture1, 
                                        'addiction_picture2': trade.addiction_picture2, 
                                        'addiction_picture3': trade.addiction_picture3})
    return render_to_response('cardtravel/edit_trade.html', 
        {'trade_form': trade_form}, context)

@login_required
def response_trade(request):
    pass

#class AddTradeView(FormView):
    #form_class = TradeForm
    #template_name = "cardtravel/add_trade.html"
    #success_url = '/index/'

    #@method_decorator(login_required)
    #def get_context_data(self, **kwargs):
        #context = super(AddTradeView, self).get_context_data(**kwargs)
        #context.update(csrf(self.request))
        #context['trade_form'] = self.form_class(initial={'user': self.request.user})
        #return context

    #@method_decorator(login_required)
    #def post(self, request, **kwargs):
        #trade_form = self.form_class(request.POST)
        #context = super(AddTradeView, self).get_context_data(**kwargs)
        #context.update(csrf(self.request))
        #context['trade_form'] = trade_form
        #if trade_form.is_valid():
            #return self.form_valid(trade_form)
        #else:
            #return render_to_response(self.template_name, context)
    
    #@method_decorator(login_required)
    #def form_valid(self, trade_form):
        #context = super(AddTradeView, self).get_context_data(**kwargs)
        #trade = trade_form
        #trade.save()
        #return super(AddTradeView, self).form_valid(trade_form)
      
def page403(request):
    return render(request, '403.html', {}, status=403)


def page404(request):
    return render(request, '404.html', {}, status=404)


def page500(request):
    return render(request, '500.html', {}, status=500)