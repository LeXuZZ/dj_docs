import random
import string
from django.contrib.auth import login, logout
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from poll_auth.models import *
from dj_docs.settings import redis_instance, REGISTRATION_EXPIRATION_TIME
from poll_auth.service.mail.templates import RegistrationConfirmationTemplate, PasswordRecoveryTemplate
from poll_auth.util import constant
from poll_auth.util.credentials import LoginCredentials, RegistrationCredentials, CredentialsValidationException
from util.response import response_message
from poll_auth.util.random_generator import generate_hash


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        try:
            user = LoginCredentials(**{str(k): request.POST.get(k) for k in request.POST}).user
        except CredentialsValidationException as error_message:
            return render(request, 'login.html', context={'error_message': error_message})
        login(request, user)
        return redirect("/")


class RegisterView(View):
    def post(self, request):
        try:
            credentials = RegistrationCredentials(**{str(k): request.POST.get(k) for k in request.POST})
        except CredentialsValidationException as error_message:
            return render(request, 'register.html', {'error_message': error_message})

        registration_hash = generate_hash(50)

        redis_instance.setex(registration_hash, REGISTRATION_EXPIRATION_TIME, json.dumps(request.POST))
        redis_instance.publish('email_send_channel',
                               json.dumps(
                                   RegistrationConfirmationTemplate(
                                       to=credentials.email, hash=registration_hash
                                   ).sendgrid_dump()
                               )
                           )
        return render(request, 'login.html', context={
            'success_message': constant.SuccessMessage.REGISTRATION_MAIL_SENT
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
        except CredentialsValidationException as error_message:
            return render(request, 'register.html', context={
                'error_message': error_message
            })
        except Exception:
            return HttpResponse("404")

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
        credentials = json.loads(redis_instance.get(recovery_hash).decode())
        try:
            user = PollUser.objects.get(email=credentials.get('email'))
        except Exception as e:
            print(e)
        user.set_password(credentials.get('password'))
        user.save()
        return render(request, 'login.html', context={'success_message': 'successfully changed'})

    def post(self, request):
        recovery_hash = generate_hash(50)
        new_password = generate_hash(10)
        redis_instance.setex(recovery_hash, REGISTRATION_EXPIRATION_TIME, json.dumps(
            {'email': request.POST.get('email'),
             'password': new_password}
        ))
        redis_instance.publish('email_send_channel',
                               json.dumps(
                                   PasswordRecoveryTemplate(
                                       to=request.POST.get('email'),
                                       hash=recovery_hash,
                                       new_password=new_password
                                   ).sendgrid_dump()
                               )
                           )
        return render(request, 'login.html', context={'success_message': constant.SuccessMessage.PASSWORD_RECOVERY_MAIL_SENT})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return response_message(success=True)
