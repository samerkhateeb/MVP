
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import ProductsSerializer as serializer
from products.models import ProductsModel as ThisModel
import logging
from django.conf import settings
from auth_user.models import UserProfile
from ..models import TransactionModel
from django.views.decorators.csrf import csrf_exempt
from backend.templatetags.common_tags import multiply_method, process_images
from cms.models import Page, Title


@api_view(['POST',])
@permission_classes((permissions.IsAuthenticated,))
def vProduct_new(request):
    error = "1"
    _status = status.HTTP_404_NOT_FOUND
    data = {}
    try:
        if request.method == 'POST':
            user_type = request.user.userprofile.user_type
            if user_type == '1':
                error = "Users with Sellers only can add products to the Market"
            else:
                img_arr = []
                if len(request.FILES) != 0:
                    images = request.FILES.getlist('images')
                    img_arr = process_images(images, request.user, 1)

                _serializer = serializer(data=request.data)
                if _serializer.is_valid():
                    _serializer.save(
                        image=img_arr['image'] if len(img_arr) > 0 else None,
                        seller=request.user)
                    _status = status.HTTP_201_CREATED
                    # data = _address_data
                    error = "0"
                else:
                    logging.exception('vProduct_new Validation Error: {0} | {1}'.format(
                        _serializer.errors, _status))

    except Exception as e:
        logging.exception('vProduct_new Error: {0}'.format(e))
        _status = status.HTTP_400_BAD_REQUEST
        if settings.DEBUG:
            error = str(e)

    data['error'] = error

    return Response(data, status=_status)


@api_view(['DELETE', 'PUT'])
@permission_classes((permissions.IsAuthenticated,))
def vProducts_manage(request, id):
    # find address by pk (id)
    error = "1"
    _status = status.HTTP_404_NOT_FOUND
    data = {}
    try:
        if request.method == 'PUT':
            obj = ThisModel.objects.get(pk=id, seller=request.user)
            _serializer = serializer(obj, data=request.data)
            if _serializer.is_valid():
                data['context'] = _serializer.validated_data
                _serializer.save()
                _status = status.HTTP_205_RESET_CONTENT
                # data = _address_data
                error = "0"
            else:
                logging.exception('vProducts_manage PUT Validation Error: {0} | {1}'.format(
                    _serializer.errors, _status))

        elif request.method == 'DELETE':
            obj = ThisModel.objects.filter(seller=request.user, pk=id).first()
            if obj:
                obj.delete()
                _status = status.HTTP_205_RESET_CONTENT
            else:
                logging.exception('vProducts_manage Unable to Delete Error: {0} | {1}'.format(
                    _serializer.errors, _status))

        error = "0"

    except Exception as e:
        logging.exception('vProducts_manage Error: {0}'.format(e))
        _status = status.HTTP_400_BAD_REQUEST
        if settings.DEBUG:
            error = str(e)

    data['error'] = error

    return Response(data, status=_status)


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def vProduct_buy(request, id, amount):
    error = "1"
    _status = status.HTTP_404_NOT_FOUND
    data = {}
    try:
        if request.method == 'PUT':
            amount = int(amount)
            product = ThisModel.objects.filter(
                pk=id, amount__gte=amount).first()
            if not product:
                error = "the product is out of stock right now!!, please try less amount"
            else:
                total_cost = multiply_method(product.cost, amount)

                buyer = UserProfile.objects.filter(user=request.user).first()

                deposite = int(buyer.deposite)

                if deposite < total_cost:
                    error = "insufficient fund!! please deposite more money to buy this product"

                else:

                    buyer.deposite = deposite - total_cost
                    buyer.save()

                    product.amount = int(product.amount) - amount
                    product.save()

                    txn = TransactionModel(
                        amount=amount, buyer=buyer.user, product=product)
                    txn.save()
                    _status = status.HTTP_205_RESET_CONTENT
                    data['context'] = txn.json()
                    error = "0"

    except Exception as e:
        logging.exception('vProduct_buy Error: {0}'.format(e))
        _status = status.HTTP_400_BAD_REQUEST
        if settings.DEBUG:
            error = str(e)

    data['error'] = error

    return Response(data, status=_status)


@api_view(['GET',])
@permission_classes((permissions.AllowAny,))
def vProduct_detail(request, id):
    # find address by pk (id)
    error = "1"
    _status = status.HTTP_404_NOT_FOUND
    data = {}
    try:
        if request.method == 'GET':
            obj = ThisModel.objects.filter(pk=id, publish=True).first()
            if obj:
                _serializer = serializer(obj)
                data['context'] = _serializer.data
                _status = status.HTTP_200_OK

            error = "0"

    except Exception as e:
        logging.exception('Products Error: {0}'.format(e))
        _status = status.HTTP_400_BAD_REQUEST
        if settings.DEBUG:
            error = str(e)

    data['error'] = error

    return Response(data, status=_status)


@api_view(['GET',])
@permission_classes((permissions.AllowAny,))
def vProducts(request):
    error = "1"
    _status = status.HTTP_404_NOT_FOUND
    data = {}
    try:

        if request.method == 'GET':

            obj = ThisModel.objects.filter(publish=True, amount__gt=0)
            _serializer = serializer(obj, many=True)

            data['context'] = _serializer.data
            _status = status.HTTP_200_OK
            error = "0"

    except Exception as e:
        logging.exception('Products Error: {0}'.format(e))
        _status = status.HTTP_400_BAD_REQUEST
        if settings.DEBUG:
            error = str(e)

    data['error'] = error

    return Response(data, status=_status)
