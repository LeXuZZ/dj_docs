import random
import string
from django.contrib.auth import login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import View
from poll_auth.models import *
from dj_docs.settings import redis_instance, REGISTRATION_EXPIRATION_TIME
from poll_auth.util import constant
from poll_auth.util.credentials import LoginCredentials, RegistrationCredentials
from util.response import response_message


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        try:
            user = LoginCredentials(**{str(k): request.POST.get(k) for k in request.POST}).user
        except Exception as error_message:
            return render(request, 'login.html', context={'error_message': error_message})
        login(request, user)
        return redirect("/")


class RegisterView(View):
    def post(self, request):
        try:
            credentials = RegistrationCredentials(**{str(k): request.POST.get(k) for k in request.POST})
        except Exception as error_message:
            return render(request, 'register.html', {'error_message': error_message})

        registration_hash = ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits + string.ascii_lowercase
            ) for _ in range(50))

        redis_instance.setex(registration_hash, REGISTRATION_EXPIRATION_TIME, json.dumps(request.POST))
        redis_instance.publish('registration_email_channel', json.dumps(credentials.redis_data(registration_hash)))
        return render(request, 'login.html', context={
            'success_message': constant.SuccessMessage.REGISTRATION_MAIL_SEND
        })

    def get(self, request, registration_hash=None):
        if not registration_hash:
            return render(request, 'register.html')
        try:
            credentials = RegistrationCredentials(**json.loads(redis_instance.get(registration_hash).decode()))
        except AttributeError:
            return render(request, 'register.html', context={
                'error_message': constant.ErrorMessage.REGISTRATION_INVALID_HASH
            })

        user = PollUser(**credentials.poll_user_data())
        try:
            user.set_password(credentials.password)
            user.save()
            redis_instance.delete(registration_hash)
            return render(request, 'login.html', context={
                'success_message': constant.SuccessMessage.REGISTRATION_SUCCESS
            })
        except IntegrityError:
            return render(request, 'register.html', context={
                'error_message': constant.ErrorMessage.REGISTRATION_USER_EXISTS
            })


class PasswordRecoveryView(View):
    def get(self, request, recovery_hash=None):
        if not recovery_hash:
            return render(request, 'password-recovery.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return response_message(success=True)
