import json
import random
import string

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.generic import View
from poll.models import *
from dj_docs.settings import redis_instance, REGISTRATION_EXPIRATION_TIME


def response_message(success=False, data=None, **kwargs):
    allowed_keys = ('text', 'info', 'warning', 'error')
    return HttpResponse(json.dumps({'success': success,
                                    'data': data,
                                    'message': {
                                        k: v for k, v in kwargs.items() if k in allowed_keys
                                        }}), content_type="application/json")


@ensure_csrf_cookie
def get_csrf(request):
    return HttpResponse("")


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class PollView(View):
    def get(self, request, id=None):
        if id:
            try:
                poll = Poll.objects.get(pk=id)
                return response_message(success=True, data=poll.json_serialize())
            except Poll.DoesNotExist:
                return response_message(success=False, error=True, text='no such poll')

        return response_message(success=True, data=[poll.json_serialize() for poll in Poll.objects.all()])

    def post(self, request):
        name, json = request.POST.get("name"), request.POST.get("json")
        try:
            Poll.objects.create(name=name, json=json).save()
            return response_message(success=True)
        except Exception:
            return response_message(success=False, error=True, text='cannot save poll to db')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/")
        return response_message(success=False,
                                text='Невірно вказана пара логін\пароль',
                                error=True)


class RegisterView(View):

    def post(self, request):

        registration_hash = ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits + string.ascii_lowercase
            ) for _ in range(50))

        registration_data = json.dumps({
            'email': request.POST.get('email'),
            'password': request.POST.get('password')
        })
        redis_instance.setex(registration_hash, REGISTRATION_EXPIRATION_TIME, registration_data)
        redis_instance.publish('registration_email_channel', registration_data)
        return response_message(success=True,
                                text='email with registration link was send')

    def get(self, request, registration_hash):
        if not registration_hash:
            return render(request, 'register.html')

        try:
            registration_data = json.loads(redis_instance.get(registration_hash).decode())
        except AttributeError:
            return response_message(success=False,
                                    text='such registration key was not found',
                                    error=True)

        user = PollUser(email=registration_data.get('email'))
        user.set_password(registration_data.get('password'))
        try:
            user.is_active = True
            user.save()
            return response_message(success=True,
                                    text='u have registered',
                                    info=True)
        except IntegrityError:
            return response_message(success=False,
                                    error=True,
                                    text='such user already exists')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return response_message(success=True)
