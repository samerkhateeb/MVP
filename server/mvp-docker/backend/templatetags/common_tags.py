
import re
import random
from django.conf import settings
import logging
from django.core.files import File
from filer.models import Image
from backend.templatetags.exception import ExceptionMessage
import requests
from django.template import Library, Node
import random
import string
from django.utils.text import slugify
from  googletrans import Translator as google_translator
from datetime import datetime, timedelta
from os.path import dirname
from time import time 
import jwt
import json

REGEX_PATTERN = r'[#&;`|*?~<>^()\[\]{}$\\]+'
REGEX_PATTERN_FULL = r'[!-#&;`|*?~<>^()\[\]{}$\\]+'

register = Library()
NAME_REGEX = re.compile('[![-]^0-9a-zA-Z+_]+')

def valid_name(name):
    return not NAME_REGEX.search(name)


def senetize(name):
    """Escapes characters you don't want in arguments (preventing shell
    injection)"""
    return re.sub(REGEX_PATTERN, '', name)

def senetize_full(name):
    """Escapes characters you don't want in arguments (preventing shell
    injection)"""
    return re.sub(REGEX_PATTERN_FULL, '', name)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@register.filter
def get_page_id(page):
    try:
        return page.publisher_public_id
    except: pass


@register.filter
def is_business_user(user):
    try:
        return False if user.is_authenticated and user.userprofile.user_type ==  "1" else True
    except: pass
    




def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def trans_title(instance, edit=False):
    
    translator = google_translator()
    # text_lang = translator.detect([instance.name])[0]
   
    if not instance.title_en or edit == True:
        instance.title_en = translator.translate(instance.title, dest="en").text,
        instance.title_en = instance.title_en[0]

    if not instance.title_ar or edit == True:
        instance.title_ar=translator.translate(instance.title, dest="ar").text,
        instance.title_ar = instance.title_ar[0]
    
    # if instance.title_en or instance.title_ar:
    instance.save()

    return instance


def name_desc_trans(instance):
    
    translator = google_translator()
    text_lang = translator.detect([instance.name])[0]
    
    if not instance.name_en or not instance.description_en:
        trans_text = translator.translate([instance.name, instance.description], dest="en"),
        if not instance.name_en:
            instance.name_en = trans_text[0][0].text

        if not instance.description_en:
            instance.description_en = trans_text[0][1].text
    
    if not instance.name_ar or not instance.description_ar:
        trans_text = translator.translate([instance.name, instance.description], dest="ar"),
        if not instance.name_ar:
            instance.name_ar = trans_text[0].text
            instance.name_ar = instance.name_ar[0]
        if not instance.description_ar:
            instance.description_ar = trans_text[1].text
            instance.description_ar = instance.description_ar[0]
    
    if text_lang.lang != "ar" or text_lang.lang != "en":
        instance.save()

    return instance



def trans_title_desc(instance, edit= False):
    
    translator = google_translator()
    # text_lang = translator.detect([instance.title])[0]
    try:
        if not instance.title_en or not instance.description_en or edit:
            trans_text = translator.translate([instance.title, instance.description], dest="en"),
            if not instance.title_en  or edit:
                instance.title_en = trans_text[0][0].text

            if not instance.description_en or edit:
                instance.description_en = trans_text[0][1].text
        
        if not instance.title_ar or not instance.description_ar or edit:
            trans_text = translator.translate([instance.title, instance.description], dest="ar"),
            if not instance.title_ar or edit:
                instance.title_ar = trans_text[0][0].text
            if not instance.description_ar or edit:
                instance.description_ar = trans_text[0][1].text
    except Exception as exc:
        pass
    
    # if text_lang.lang != "ar" or text_lang.lang != "en":
    instance.save()

    return instance



def get_auction_threshold(unit, duration, schedule, status):
        vPass = False
        result = 0
        day = 0
        hour = 0
        minute = 0
        second = 0
        if unit == "1": #  minutes
            threshold =  (schedule.replace(tzinfo=None) + timedelta(minutes=duration)) - datetime.now().replace(tzinfo=None)
            if threshold.days >= 0 and threshold.seconds / 60 > 0:
                vPass = True
                minute = int(threshold.seconds / 60)
                second = int('{:.3f}'.format((round (threshold.seconds /60,3))).split('.')[1]) * 60 /1000
                #result = self.auction_schedule.replace(tzinfo=None).minute 
        elif unit == "2": #  hours
            threshold = (schedule.replace(tzinfo=None) + timedelta(hours=duration)) - datetime.now().replace(tzinfo=None)
            if threshold.days >= 0 and threshold.seconds / (60*60) > 0:
                vPass = True
                hour = int(threshold.seconds / (60*60))
                minute = int(int('{:.3f}'.format((round (threshold.seconds /(60*60),3))).split('.')[1]) * 60 /1000)
                second = int('{:.3f}'.format((round (threshold.seconds /60,3))).split('.')[1]) * 60 /1000
                
        else:   #   days 3
            threshold = (schedule.replace(tzinfo=None) + timedelta(days=duration)) - datetime.now().replace(tzinfo=None)
            if threshold.days > 0:
                vPass = True
                day = threshold.days
                hour = int(threshold.seconds / (60*60))
                minute = int(int('{:.3f}'.format((round (threshold.seconds /(60*60),3))).split('.')[1]) * 60 /1000)
                second = int('{:.3f}'.format((round (threshold.seconds /60,3))).split('.')[1]) * 60 /1000

        if status and vPass:
              return day, hour, minute, second
        return 0

def unique_slug(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title_en)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug(instance, new_slug=new_slug)
    return slug



def vcode_Forget_generator(instance):
    code            =   random.randint(10000,99999)
    Klass       =   instance.__class__
    qs_exists       =   Klass.objects.filter(forget_code = code).exists()
    if qs_exists:
        return vcode_Forget_generator()
    return code


def unique_file_name(name):
    _rand = ""
    name = name.replace(' ','')
    if valid_name(name):
        _rand = random.randint(1,9999)
        return True, "{0}_{1}".format(name, _rand)
    else:
        return False

def unique_id(instance):
    order_new_id        =   random_string_generator()

    Klass       =   instance.__class__
    qs_exists       =   Klass.objects.filter(order_id = order_new_id).exists()

    if qs_exists:
        return unique_id(instance)

    return order_new_id
    

def unique_room_name(instance):

    rand_unique_id        =   random_string_generator()
    Klass                 =   instance.__class__
    qs_exists             =   Klass.objects.filter(room = rand_unique_id).exists()

    if qs_exists:
        return unique_room_name(instance)

    return rand_unique_id
    

def track_id(instance):
    code            =   random.randint(1000,2147483647)
    Klass       =   instance.__class__
    qs_exists       =   Klass.objects.filter(TrackID = code).exists()

    if qs_exists:
        return track_id (instance)

    return code



def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False

def floatTryParse(value):
    try:
        return float(value), True
    except ValueError:
        return value, False


def process_images(images, user_, range_):
        img_arr={}
        for i in range(1, range_+1):
            index = '{0}'.format(i) if i> 1 else ''
            if i <= len(images):
                file = images[i-1]
                if file and allowed_file(file.name):
                    img = uploadimage (image = file, user=user_)
                    # if i == 1:
                    img_arr['image' + index ] = img if img else ''
            else:
                img_arr['image' + index ] = None
        
        return img_arr

def uploadimage(**kwargs):
    try:
        result = ""
        image = kwargs['image']
        error = ""
        data_image = {"file":image,}
        temp_id = None
        from auth_user.api.serializers import TempFilesSerializer
        file_serializer = TempFilesSerializer(data=data_image)
        if file_serializer.is_valid():
        
            image_temp = file_serializer.save()
            filename = image.name
            filename_full = settings.MEDIA_ROOT  + "/" + image_temp.file.name

            with open(filename_full, "rb") as f:
                file_obj = File(f, name=filename)
                image = Image.objects.create(owner=kwargs['user'],
                                            original_filename=filename,
                                            file=file_obj)
            result = image
        
        #delete temp image
            image_temp.delete()
        return result

    except Exception as e:
        ExceptionMessage('vRegister Error: {0}'.format(e))
        # raise e
    
    return error



def check_google_verify(token):
    verified = False
    endpoint = settings.GOOGLE_API.format(token)
    requests.ssl_verify = False
    email = ""
    re = requests.get(endpoint)
    re = json.loads(re.content)
    if 'error' in re:
        return verified,  email
    elif re['email_verified'] == "true":
            verified = True
            email = re['email']
    
    return verified,  email

def check_apple_verify(code):
    client_secret = generate_apple_token()
    key_id = settings.APPLE_KEY_ID
    verified = False
    requests.ssl_verify = False
    email = ''
    public_key =""
    payload ={'client_id':settings.APPLE_CLIENT_ID,
                'client_secret': client_secret,
                'code': code,
                'grant_type':'authorization_code',
                }
    headers = {
                'content-type':'application/x-www-form-urlencoded',
                }

    result = requests.post(settings.APPLE_API, headers=headers, data=payload, )
    # JSON.stringify(result)

    result_data = json.loads(result.text)
    
    # r = requests.get(, params=request.GET, auth='Bearer {0}'.format(request.user))
    if "error" in result_data:
        raise Exception ('Error Apple ID - ' + result_data['error']  + " - " + result_data['error_description']) 
    else:
        token_id = result_data['id_token']

        with open(settings.APPLE_PUBLIC_KEY.format(dirname(settings.DATA_DIR)), "r") as f:
            public_key = f.read()

        r = jwt.decode(token_id, key=public_key, verify=False)
            # jwt.decode(id_token, '', verify=False)

        email = r['email']
        verified = True

    return verified, email



def generate_apple_token():
        print(settings.DJANGO_ROOT)
        
        with open(settings.APPLE_PRIVATE_KEY.format(dirname(settings.DATA_DIR)), "r") as f:
            private_key = f.read()
        team_id = settings.APPLE_TEAM_ID
        key_id = settings.APPLE_KEY_ID
        client_id = settings.APPLE_CLIENT_ID
        # time_utc = datetime.utcnow()
        # validity_minutes = 20
        # timestamp_now = int(time_utc.strftime("%Y%m%d%H%M%S"))
        # timestamp_exp = timestamp_now + (60 * validity_minutes)
        timestamp_now = time()
        timestamp_exp = timestamp_now + (86400*180)
        # cls.last_token_expiration = timestamp_exp
        data = {
                "iss": team_id,
                "iat": timestamp_now,
                "exp": timestamp_exp,
                "aud": settings.APPLE_DEV_API,
                "sub": client_id
            }
        # data = {
        #         "iss":  "https://appleid.apple.com",
        #         "sub": "12222",
        #         "iat": timestamp_now,
        #         "exp": timestamp_exp,
        #         "aud":client_id,
        #         'nonce': "Hr0bkzpXJd8xiPxXeZlvK8EiCLniyPx6"
        #     }
        token = jwt.encode(payload=data, key=private_key, algorithm="ES256", headers={"kid": key_id}).decode()
        return token
    
    
    
def sum_method(first, second):
    return int(first) + int(second)

def multiply_method(first, second):
    return int(first) * int(second)
