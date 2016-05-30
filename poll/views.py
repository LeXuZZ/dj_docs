import json
import random
import string

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from poll.models import PollUser
from dj_docs.settings import redis_instance, REGISTRATION_EXPIRATION_TIME


def response_message(success=False, data=None, **kwargs):
    allowed_keys = ('text', 'info', 'warning', 'error')
    return json.dumps({'success': success,
                       'data': data,
                       'message': {
                           k: v for k, v in kwargs.items() if k in allowed_keys
                           }})


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class LoginView(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(response_message(success=True))
        return HttpResponse(response_message(success=False,
                                             text='Невірно вказана пара логін\пароль',
                                             error=True))


class RegisterView(View):
    def post(self, request):

        registration_hash = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))
        redis_instance.setex(registration_hash,
                             json.dumps({'email': request.POST.get('email'), 'password': request.POST.get('password')}),
                             REGISTRATION_EXPIRATION_TIME)
        return HttpResponse(response_message(success=True,
                                             text='email with registration link was send'))

    def get(self, request, registration_hash):
        raw_registration_data = redis_instance.get(registration_hash)
        if raw_registration_data:
            registration_data = json.loads(raw_registration_data, encoding='utf-8')
            user = PollUser(email=registration_data.get('email'))
            user.set_password(registration_data.get('password'))
            try:
                user.is_active = True
                user.save()
                return HttpResponse(response_message(success=True,
                                                     text='u have registered',
                                                     info=True))
            except IntegrityError:
                return HttpResponse(response_message(success=False,
                                                     error=True,
                                                     text='such user already exists'))
        return HttpResponse(response_message(success=False,
                                             text='such registrationkey was not found',
                                             error=True))


class LogoutView(View):
    def post(self, request):
        logout(request)
        return HttpResponse(response_message(success=True))
