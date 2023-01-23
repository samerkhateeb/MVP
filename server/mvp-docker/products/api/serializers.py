from rest_framework import serializers
from products.models import ProductsModel
from django.conf import settings
from django.contrib.sites.models import Site


class ProductsSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField('image_field')
    seller = serializers.SerializerMethodField('seller_field')

    # thumbnail = serializers.SerializerMethodField('thumbnail_field')

    @staticmethod
    def image_field(self,):
        if self.image:
            return settings.CURRENT_SITE + self.image.url

    @staticmethod
    def seller_field(self,):
        if self.seller:
            return {'name': '{0}-{1}'.format(self.seller.first_name, self.seller.last_name), 'username': self.seller.username}


    class Meta:
        model = ProductsModel
        fields = ['id', 'title', 'description', 'image', 'amount', 'seller',
                  'cost', 'category', 'external_link_name', 'external_link', 'target']
