from django.contrib import admin

from .models import ProductsModel, TransactionModel
from django.utils.translation import ugettext, ugettext_lazy as _


@admin.register(TransactionModel)
class TxnsAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'product', 'amount')
    pass


@admin.register(ProductsModel)
class ProductsAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'publish', 'cost', 'amount')
    list_filter = ('publish',)
    ordering = ('-id',)

    fieldsets = ('publish', 'title', 'description', 'image',
                 'external_link_name', 'external_link', 'target', 'sorting')

    fieldsets = (
        (None, {
            'fields': ('publish', 'title', )
        }),

        (None, {
            'fields': ('description', )
        }),

        (None, {'fields': (('cost', 'amount'), ('category', 'seller'), ('image'),
         ('external_link_name', 'target', 'sorting'), 'external_link',)})

    )
