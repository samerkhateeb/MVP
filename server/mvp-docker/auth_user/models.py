from django.db import models

# Create your models here.

from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from filer.fields.image import FilerImageField
from filer.models import Image
from django.core.files import File
import logging
from django.db.models import Avg
from cms.models import Page, Title
from django.conf import settings
import easy_thumbnails
from cms.models.fields import PageField
from datetime import datetime, timedelta
from django.utils.translation import ugettext, ugettext_lazy as _

user_auth_setting = settings.AUTH_USER_MODEL

CUSTOMER_TYPE = [
    ('1', _('Buyer')),
    ('2', _('Seller')),
]


DEPOSITES = [
    ('5', '5'),
    ('10', '10'),
    ('20', '20'),
    ('50', '50'),
    ('100', '100'),
]


CONDITIONS = [
    ('1', _('New')),
    ('2', _('Used')),
]


class TempFiles(models.Model):
    file = models.FileField(blank=False, null=False, default="1.jpg")

    def __str__(self):
        return self.file.name

# extend user model


class UserProfile(models.Model):
    user = models.OneToOneField(
        user_auth_setting, null=False, on_delete=models.CASCADE, verbose_name=_("user"))
    user_type = models.CharField(
        _("user_type"), null=True, blank=True, max_length=10, choices=CUSTOMER_TYPE, default='1',)
    deposite = models.IntegerField(
        _("deposite"), null=True, blank=True, default=5)
    bio = models.TextField(_("bio"), null=True, blank=True)
    image = FilerImageField(null=True, blank=True,
                            on_delete=models.SET_NULL, verbose_name=_("image"),)
    updated = models.DateTimeField(_("updated"), auto_now=True)
    created = models.DateTimeField(_("created"), auto_now_add=True)
    sorting = models.BigIntegerField(
        _("sorting"), null=True, blank=True, default=0)

    def __str__(self):
        return '{0}'.format(self.user.username)

    def get_business_valid_till(self):
        if self.business_valid_till:
            return self.business_valid_till.date()
        else:
            return ""

    def upgrade(self, duration):
        self.user_type = "2"
        if self.business_valid_till and self.business_valid_till > datetime.now():  # check if user already have credit
            self.business_valid_till += + timedelta(days=duration)
        else:
            self.business_valid_till = (datetime.now(
                tzinfo=None) + timedelta(days=duration))
        self.save()

    def get_thumbnail(self):
        if self.image:
            return settings.CURRENT_SITE + easy_thumbnails.templatetags.thumbnail.thumbnail_url(self.image, 'large')

    def toJSON_Full(self, request=""):

        return {
            'id': self.user.id,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'image': self.get_thumbnail(),
            'bio': self.bio,
            'user_type': self.user_type,
            'deposite': self.deposite,

        }


# create Signal
def userprofile_creating_receiver(sender, instance, created, *args, **kwargs):
    if created:
        if all(hasattr(instance, attr) for attr in ['_userprofile']) and all(hasattr(instance, attr) for attr in ['email']):
            image = None
            new_userprofile = instance._userprofile
            if instance._tempfileid:

                # if true, then copy the image to the profile
                filename = instance._image.name
                filepath = settings.MEDIA_ROOT + "/" + instance._image.name

                with open(filepath, "rb") as f:
                    file_obj = File(f, name=filename)
                    image = Image.objects.create(owner=instance,
                                                 original_filename=filename,
                                                 file=file_obj)

                # delete temp image
                instance._tempfileid.delete()
                new_userprofile.image = image
                new_userprofile.badge_identity_types = True

            new_userprofile.user = instance
            new_userprofile.save()


post_save.connect(userprofile_creating_receiver,
                  sender=user_auth_setting, weak=False)
