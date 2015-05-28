from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from cardtravel.models import UserProfile, Card, WishList, Collection


# Register your models here.
class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Information'


class WishListInline(admin.StackedInline):
    model = WishList
    can_delete = False
    verbose_name_plural = 'Fish List'
    fk_name = 'user'
    filter_horizontal = ['wishlist']

class CollectionInline(admin.StackedInline):
    model = Collection
    can_delete = False
    fk_name = 'user'
    filter_horizontal = ['collectionlist']


class UserAdmin(UserAdmin):
    inlines = (UserInline, WishListInline, CollectionInline)
    

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Card)