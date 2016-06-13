import random
import string
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import View
from poll_auth.models import *
from dj_docs.settings import redis_instance, REGISTRATION_EXPIRATION_TIME
from util.response import response_message


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        error_messages = []
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/")
        if not email:
            error_messages.append('Вы не указали почтовый адрес')
        if not password:
            error_messages.append('Вы не указали пароль')
        if not user:
            error_messages.append('Ошибка авторизации')
        return render(request, 'login.html', {'error_messages': error_messages})


class RegisterView(View):

    def post(self, request):
        validation_status = self._validate_registration_data(request.POST)
        if not validation_status.get('status'):
            return render(request, 'register.html', {'error_message': validation_status.get('error_message')})
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
        return render(request, 'login.html', {'success_message': 'На почту отправлена ссылка для подтверждения регистрации'})

    def get(self, request, registration_hash=None):
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

    def _validate_registration_data(self, request_post):
        firstname = request_post.get("firstname")
        lastname = request_post.get("lastname")
        middlename = request_post.get("middlename")
        email = request_post.get("email")
        password = request_post.get("password")
        password_confirmation = request_post.get("password_confirmation")

        if not all([value for value in request_post.values()]):
            return {'status': False, 'error_message': 'Все поля должны быть заполнены'}
        if not password == password_confirmation:
            return {'status': False, 'error_message': 'Пароли не совпадают'}
        return {'status': True}



class PasswordRecoveryView(View):
    def get(self, request):
        return render(request, 'password-recovery.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return response_message(success=True)
