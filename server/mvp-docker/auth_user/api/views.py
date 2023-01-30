
from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.models import User

# Create your views here.
from rest_framework import permissions, authentication, status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token as csrfToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

import re
from rest_framework.authtoken.models import Token

# file upload
from .serializers import TempFilesSerializer, UserProfileSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings
from auth_user.models import UserProfile
from django.db.models import Q
import random
from backend.templatetags.common_tags import check_google_verify, allowed_file, uploadimage, vcode_Forget_generator, check_apple_verify
from backend.templatetags.exception import ExceptionMessage

from ..models import DEPOSITES

from backend.templatetags.common_tags import sum_method

USERNAME_REGEX = re.compile('[^0-9a-zA-Z_]+')
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

UserModel = get_user_model()

rows_default = int(settings.ROWS_DEFAULT)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def vLogin(request):  # update the cart
    # find address by pk (id)
    error = "1"
    _status = status.HTTP_401_UNAUTHORIZED
    data = {}
    res = ""
    try:
        # ExceptionMessage('request: {0}'.format(request.data))
        if request.method == 'POST':
            username = request.data.get('username')
            password = request.data.get('password')

            # ExceptionMessage('username: {0}'.format(username))
            # ExceptionMessage('password: {0}'.format(password))

            is_authenticated = False
            user = ''

            if username:
                user = authenticate(username=username, password=password)
            else:
                error = "wrong credentials - unable to login"
                _status = status.HTTP_404_NOT_FOUND

            if user:
                data_user = {"userprofile": user.userprofile.toJSON_Full(
                ), "token": get_tokens_for_user(user)}
                data['context'] = data_user
                _status = status.HTTP_200_OK
                error = "0"

    except Exception as e:
        ExceptionMessage('vLogin Error: {0}'.format(e))
        _status = status.HTTP_400_BAD_REQUEST
        if settings.DEBUG:
            error = str(e)

    data['error'] = error

    return Response(data, status=_status)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def vUserProfile(request):  # update the cart
    # find address by pk (id)
    error = "1"
    _status = status.HTTP_404_NOT_FOUND
    data = {}
    try:
        if request.method == 'GET':
            data['context'] = request.user.userprofile.toJSON_Full()
            _status = status.HTTP_200_OK

        elif request.method == 'DELETE':
            obj = UserProfile.objects.filter(user=request.user).first()
            if obj:
                obj.delete()
                _status = status.HTTP_200_OK

        elif request.method == 'PUT':
            user_data = request.data
            user_data._mutable = True
            user_data['user'] = request.user.pk
            user_data._mutable = False

            obj = UserProfile.objects.filter(user=request.user).first()
            _serializer = UserProfileSerializer(obj, data=user_data)
            image = ''
            if _serializer.is_valid():
                user = request.user
                file = request.FILES.getlist('images')[0]
                badge_identity_types = False
                # if len(file) != 0:
                if file and allowed_file(file.name):
                    # if not obj.image or obj.image.original_filename != request.FILES['file'].name:
                    image = uploadimage(image=file, user=request.user)
                    badge_identity_types = True
                else:
                    image = obj.image

                _serializer.save(user=user, image=image,
                                 badge_identity_types=badge_identity_types)
                save_user = False
                if request.data.get('first_name'):
                    user.first_name = request.data.get('first_name')
                    save_user = True
                if request.data.get('last_name'):
                    user.last_name = request.data.get('last_name')
                    save_user = True

                if request.data.get('password') and request.data.get('password') == request.data.get('cpassword'):
                    user.set_password(request.data.get('password'))
                    save_user = True

                if request.data.get('email'):
                    user.email = request.data.get('email')
                    save_user = True

                user.legal_business_name = request.data.get(
                    'legal_business_name')

                if save_user == True:
                    user.save()

                data['context'] = obj.toJSON_Full()

                _status = status.HTTP_205_RESET_CONTENT

                error = "0"
            else:
                error = _serializer.errors

    except Exception as e:
        ExceptionMessage('vUserProfile Error: {0}'.format(e))
        _status = status.HTTP_400_BAD_REQUEST
        if settings.DEBUG:
            error = str(e)

    data['error'] = error

    return Response(data, status=_status)


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def vUserProfile_deposite(request):
    # find address by pk (id)
    error = "1"
    _status = status.HTTP_404_NOT_FOUND
    data = {}
    try:
        if request.method == 'PUT':
            _data = request.data

            request.POST._mutable = True
            _data['user'] = request.user.pk
            _deposite = 0

            obj = UserProfile.objects.filter(
                user=request.user, user_type='1').first()

            if not obj:
                error = "only users with 'Buyer' Role need is allowed to deposite on the account"
            else:

                for x in DEPOSITES:

                    if x[0] == str(_data['deposite']):
                        _deposite = sum_method(
                            _data['deposite'], obj.deposite)
                        break

                if _deposite == 0:
                    error = "{0} is not a valid choice".format(
                        _data['deposite'])
                else:
                    _data['deposite'] = _deposite

                    request.POST._mutable = False
                    _serializer = UserProfileSerializer(obj, data=_data)

                    if _serializer.is_valid():
                        user = request.user

                        _serializer.save(user=user)

                        data['context'] = obj.toJSON_Full()

                        _status = status.HTTP_205_RESET_CONTENT

                        error = "0"

                    else:
                        error = _serializer.errors

    except Exception as e:
        ExceptionMessage('vUserProfile Error: {0}'.format(e))
        _status = status.HTTP_400_BAD_REQUEST
        if settings.DEBUG:
            error = str(e)

    data['error'] = error

    return Response(data, status=_status)


@api_view(['PUT'])
@permission_classes((permissions.IsAuthenticated,))
def vUserProfile_reset(request):  # update the cart
    # find address by pk (id)
    error = "1"
    _status = status.HTTP_404_NOT_FOUND
    data = {}
    try:
        if request.method == 'PUT':
            _deposite = 0
            obj = UserProfile.objects.filter(
                user=request.user, user_type='1').first()
            if not obj:
                error = "only users with 'Buyer' Role need is allowed to deposite on the account"
            else:
                obj.deposite = _deposite
                obj.save()
                data['context'] = obj.toJSON_Full()
                _status = status.HTTP_205_RESET_CONTENT
                error = "0"

    except Exception as e:
        ExceptionMessage('vUserProfile Error: {0}'.format(e))
        _status = status.HTTP_400_BAD_REQUEST
        if settings.DEBUG:
            error = str(e)

    data['error'] = error

    return Response(data, status=_status)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def vRegister(request):  # update the cart
    '''
    Register New User API .. it takes sort of parameters, please make sure you put the validation correctly.
    '''

    data = {}
    error = "1"
    token = ""
    _status = status.HTTP_404_NOT_FOUND
    image = ""
    try:
        if request.method == 'POST':
            username = ""
            firstname = request.data.get('firstname')
            lastname = request.data.get('lastname')
            email = request.data.get('email')
            password = request.data.get('password')
            cpassword = request.data.get('cpassword')
            bio = request.data.get('bio')
            user_type = "1"
            concent = request.data.get('concent')
            password_valid = False

            if concent == 'False':
                _status = status.HTTP_417_EXPECTATION_FAILED
            else:
                if len(request.FILES) != 0:
                    image = request.FILES['images']

                email_valid = False
                file_valid = False

                if password == cpassword:
                    password_valid = True
                else:
                    _status = status.HTTP_406_NOT_ACCEPTABLE

                if email:
                    if EMAIL_REGEX.match(email):
                        email_valid = True
                    else:
                        _status = status.HTTP_406_NOT_ACCEPTABLE

                username = '{0}{1}_{2}'.format(
                    firstname, lastname, random.randint(0, 1000))

                if image:
                    data_image = {"file": image, }
                    temp_id = None
                    file_serializer = TempFilesSerializer(data=data_image)
                    if file_serializer.is_valid():
                        file_valid = True
                    else:
                        _status = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

                if email_valid and password_valid:
                    if not USERNAME_REGEX.search(username):

                        user_exists = User.objects.exclude(pk=request.user.pk).filter(
                            Q(username=username) | Q(email=email)).exists()

                        if not user_exists:
                            # get the user object
                            user = get_user_model()

                            # create new user
                            new_user = user(
                                username=username,
                                email=email
                            )
                            # set the password
                            new_user.set_password(password)
                            new_user.first_name = firstname
                            new_user.last_name = lastname

                            temp_id = ""
                            if file_valid:
                                # save the file
                                temp_id = file_serializer.save()

                            new_user._image = image
                            new_user._tempfileid = temp_id
                            # new_user._uniqueid = uniqueid
                            new_user._user_type = user_type

                            # check if userprofile valid
                            new_userprofile = UserProfile(
                                user=new_user,  user_type=new_user._user_type, bio=bio)

                            try:
                                new_userprofile.full_clean()
                            except Exception as exc:  # just if the email was not correct raise the exception, otherwise continue
                                if 'user' not in exc.message_dict and len(exc.message_dict) != 1:
                                    raise exc
                                else:
                                    new_user._userprofile = new_userprofile
                                    new_user.save()

                            # save new user
                            _status = status.HTTP_200_OK

                            # when created successfully, login
                            if new_user:
                                data_user = {"userprofile": new_user.userprofile.toJSON_Full(
                                ), "token": get_tokens_for_user(new_user)}
                                data['context'] = data_user
                                # proceed login to the CMS
                                authenticate(username=username,
                                             password=password)

                            error = "0"

                        else:  # existing user
                            _status = status.HTTP_409_CONFLICT
                    else:  # username including special characters
                        _status = status.HTTP_406_NOT_ACCEPTABLE

                else:  # fields are not provided properly
                    _status = status.HTTP_428_PRECONDITION_REQUIRED

    except Exception as e:
        ExceptionMessage('vRegister Error: {0}'.format(e))
        _status = status.HTTP_400_BAD_REQUEST
        if settings.DEBUG:
            error = str(e)

    data['error'] = error

    return Response(data, status=_status)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    access['name'] = user.username

    csrf_token = csrfToken.objects.filter(user=user).first()

    if csrf_token:
        csrf_token = user.auth_token.key
    else:
        csrf_token = csrfToken.objects.create(user=user).key

    return {
        'refresh': str(refresh),
        'access': str(access),
        'csrf': csrf_token
    }
