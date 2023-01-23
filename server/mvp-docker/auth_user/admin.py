from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'
    fieldsets = (
                (None, {'fields': ('user', ('user_type',), ('bio', 'image'), 'deposite'
                                   )}),
    )



class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

    list_display = ('id', 'userprofile', 'email',
                    'get_usertype', 'get_userDeposite')
    list_filter = ('userprofile__user_type',)

    ordering = ('-id',)

    def get_updated(self, obj):
        return obj.userprofile.updated
    get_updated.short_description = 'Update'
    get_updated.admin_order_field = 'userprofile__updated'

    def get_usertype(self, obj):
        if obj.userprofile.user_type == "1":
            return "Buyer"
        else:
            return "Seller"

    get_usertype.short_description = 'user_type'
    get_usertype.admin_order_field = 'userprofile__user_type'

    def get_userDeposite(self, obj):
        if obj.userprofile.deposite:
            return obj.userprofile.deposite

    get_userDeposite.short_description = 'deposite'
    get_userDeposite.admin_order_field = 'userprofile__deposite'



admin.site.unregister(User)
admin.site.register(User, UserAdmin)
