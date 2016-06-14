import random
import string
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import View
from poll_auth.models import *
from dj_docs.settings import redis_instance, REGISTRATION_EXPIRATION_TIME
from poll_auth.util import constant
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
            error_messages.append(constant.ErrorMessage.LOGIN_EMAIL_NULL)
        if not password:
            error_messages.append(constant.ErrorMessage.LOGIN_PASSWORD_NULL)
        if not user:
            error_messages.append(constant.ErrorMessage.LOGIN_NO_SUCH_USER)
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
            'password': request.POST.get('password'),
            'firstname': request.POST.get('firstname'),
            'lastname': request.POST.get('lastname'),
            'middlename': request.POST.get('middlename'),
            'registration_hash': registration_hash,
            'service': 'registration'
        })
        redis_instance.setex(registration_hash, REGISTRATION_EXPIRATION_TIME, registration_data)
        redis_instance.publish('registration_email_channel', registration_data)
        return render(request, 'login.html', context={
            'success_message': constant.SuccessMessage.REGISTRATION_SUCCESS
        })

    def get(self, request, registration_hash=None):
        if not registration_hash:
            return render(request, 'register.html')

        try:
            registration_data = json.loads(redis_instance.get(registration_hash).decode())
        except AttributeError:
            return render(request, 'register.html', context= {
                'error_message': constant.ErrorMessage.REGISTRATION_INVALID_HASH
            })

        user = PollUser(email=registration_data.get('email'),
                        firstname=registration_data.get('firstname'),
                        lastname=registration_data.get('lastname'),
                        middlename=registration_data.get('middlename')
                        )
        user.set_password(registration_data.get('password'))
        try:
            user.save()
            redis_instance.delete(registration_hash)
            return render(request, 'login.html', context={
                'success_message': constant.SuccessMessage.REGISTRATION_SUCCESS
            })
        except IntegrityError:
            return render(request, 'register.html', context={
                'error_message': constant.ErrorMessage.REGISTRATION_USER_EXISTS
            })

    def _validate_registration_data(self, request_post):
        email = request_post.get("email")
        password = request_post.get("password")
        password_confirmation = request_post.get("password_confirmation")

        try:
            PollUser.objects.get(email=email)
            return {'status': False, 'error_message': 'Такой пользователь уже существует'}
        except PollUser.DoesNotExist:
            pass

        if not all([value for value in request_post.values()]):
            return {'status': False, 'error_message': 'Все поля должны быть заполнены'}
        if not password == password_confirmation:
            return {'status': False, 'error_message': 'Пароли не совпадают'}
        return {'status': True}


class PasswordRecoveryView(View):
    def get(self, request, recovery_hash=None):
        if not recovery_hash:
            return render(request, 'password-recovery.html')



class LogoutView(View):
    def get(self, request):
        logout(request)
        return response_message(success=True)
