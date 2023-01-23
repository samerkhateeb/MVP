from django.conf.urls import url
from products.api import views


urlpatterns = [

    url(r'^$', views.vProducts, name='get_all_products'),
    url(r'^new/$', views.vProduct_new,  name='create_new_product'),
    url(r'^(?P<id>[0-9]+)$', views.vProduct_detail, name='get_single_product'),
    url(r'^manage/(?P<id>[0-9]+)$',
        views.vProducts_manage, name='edit_delete_product'),
    url(r'^buy/(?P<id>[0-9]+)/(?P<amount>[0-9]+)/$',
        views.vProduct_buy, name='buy_product'),

]
