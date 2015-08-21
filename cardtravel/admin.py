from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserProfile, Card, Trade


# Register your models here.
class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Information'
    filter_horizontal = ['wishlist', 'collection']


class UserAdmin(UserAdmin):
    inlines = (UserInline,)


class CardAdmin(admin.ModelAdmin):
    model = Card
    list_display = ("name", "country", "series", "issued_on",)


class TradeAdmin(admin.ModelAdmin):
    list_display = ("card", "condition", "user", "status")
    

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Trade, TradeAdmin)
