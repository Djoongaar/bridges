from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden
import requests

from authapp.models import Users


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        api_url = urlunparse(('https',
                              'api.vk.com',
                              '/method/users.get',
                              None,
                              urlencode(OrderedDict(
                                  fields=','.join(
                                      ('bdate', 'sex', 'about', 'photo_200')),
                                  access_token=response['access_token'],
                                  v='5.92')), None
                              ))
        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]
        if data['about'] and not user.description:
            user.description = data['about']
        if data['bdate'] and not user.birthday:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
            user.birthday = bdate
        if data['sex'] and not user.gender:
            user.gender = 'муж' if data['sex'] == 2 else 'жен'
        if data['photo_200'] and not user.avatar:
            user.avatar = data['photo_200']
        user.save()
    return
