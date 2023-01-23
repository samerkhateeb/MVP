from django.db import models
from cms.models import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone
from filer.fields.image import FilerImageField
from .validators import IntranetURLValidator
from cms.models import CMSPlugin, Page
from django.conf import settings
from django.contrib.auth.models import User
from backend.templatetags.common_tags import multiply_method

HOSTNAME = getattr(
    settings,
    'DJANGOCMS_LINK_INTRANET_HOSTNAME_PATTERN',
    None
)

TARGET_CHOICES = (
    ('_blank', _('Open in new window')),
    ('_self', _('Open in same window')),
    ('_parent', _('Delegate to parent')),
    ('_top', _('Delegate to top')),
)


class ProductsModel(CMSPlugin):
    url_validators = [IntranetURLValidator(intranet_host_re=HOSTNAME),]
    title = models.CharField(null=True, max_length=50, verbose_name=_("title"))
    description = models.TextField(
        null=True, blank=True, verbose_name=_("description"))
    amount = models.IntegerField(_("amount"), null=True, blank=True, default=1)
    image = FilerImageField(null=True, blank=True, on_delete=models.SET_NULL,
                            related_name='product_image', verbose_name=_("image"))
    seller = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE,  verbose_name=_('seller'),)
    cost = models.DecimalField(verbose_name=_(
        'cost'), null=True, decimal_places=3, max_digits=8, default=0.00,)

    category = models.ForeignKey(
        Page,
        limit_choices_to={'publisher_is_draft': True},
        verbose_name=_('category'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('If provided, overrides the external link.'),
    )
    external_link_name = models.CharField(
        verbose_name=_('Link Name'),
        blank=True,
        max_length=255,
    )
    external_link = models.URLField(
        verbose_name=_('External link'),
        blank=True,
        max_length=2040,
        validators=url_validators,
        help_text=_('Provide a valid URL to an external website.'),
    )

    target = models.CharField(
        verbose_name=_('Link Target'),
        choices=TARGET_CHOICES,
        blank=True,
        max_length=255,
    )

    sorting = models.BigIntegerField(
        null=True, blank=False, default=0, verbose_name=_("sorting"))
    publish = models.BooleanField(
        blank=True, default=True,  verbose_name=_("publish"))
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ("-sorting", "-id")

    def get_product(self):
        return self.title + ' the description is ' + self.description

    def __str__(self):
        return '{0} - {1}'.format(self.title, self.seller)


class TransactionModel(CMSPlugin):
    amount = models.IntegerField(_("amount"), null=True, blank=True, default=1)
    buyer = models.ForeignKey(User, null=True, blank=True,
                              on_delete=models.CASCADE,  verbose_name=_('buyer'),)
    product = models.ForeignKey(ProductsModel, null=True, blank=True,
                                on_delete=models.CASCADE,  verbose_name=_('product'),)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
        ordering = ["-id"]

    def json(self):

        return {
            'id': self.id,
            'product': {'name': self.product.title, 'description': self.product.description, 'seller': {'id': self.product.seller.id, 'name': '{0} {1}'.format(self.product.seller.first_name, self.product.seller.last_name)}},
            'buyer': {'id': self.buyer.id, 'name': '{0}-{1}'.format(self.buyer.first_name, self.buyer.last_name)},
            'amount': self.amount,
            'total': multiply_method(self.amount, self.product.cost),
            'remaining_change': 'No_change'
        }

    def __str__(self):
        return '{0} - {1}'.format(self.buyer, self.product)
