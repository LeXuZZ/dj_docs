import logging

from django.contrib.auth import login, logout
from django.db import IntegrityError
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from dj_docs.settings import redis_instance, REGISTRATION_EXPIRATION_TIME
from poll_auth.models import *
from poll_auth.service.mail.templates import RegistrationConfirmationTemplate, PasswordRecoveryTemplate
from poll_auth.util import constant
from poll_auth.util.credentials import LoginCredentials, RegistrationCredentials, CredentialsValidationException
from poll_auth.util.random_generator import generate_hash
from util.response import response_message

logger = logging.getLogger('DJ_DOCS_LOGGER')


def debug_enabled():
    return logger.isEnabledFor(10)


class LoginView(View):
    def get(self, request):
        logger.debug('LoginView. GET request')
        return render(request, 'login.html')

    def post(self, request):
        logger.debug('LoginView. POST request. POST data = %', request.POST)
        try:
            user = LoginCredentials(**{str(k): request.POST.get(k) for k in request.POST}).user
            logger.debug('LoginView. user=%s', user)
        except CredentialsValidationException as error_message:
            logger.warn('Login invalid. request.POST is: %s' % request.POST)
            return render(request, 'login.html', context={'error_message': error_message})
        login(request, user)
        logger.debug('LoginView. Login succeed')
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
            registration_request = redis_instance.get(registration_hash)
            credentials = RegistrationCredentials(**json.loads(registration_request.decode()))
        except AttributeError:
            # no such hash in redis
            return render(request, 'register.html', context={
                'error_message': constant.ErrorMessage.REGISTRATION_INVALID_HASH
            })
        except CredentialsValidationException as error_message:
            return render(request, 'register.html', context={'error_message': error_message})
        except Exception:
            return HttpResponse("404")

        user = PollUser(**credentials.poll_user_data())
        try:
            with transaction.atomic():
                user.set_password(credentials.password)
                user.save()
                redis_instance.delete(registration_hash)
                return render(request, 'login.html', context={
                    'success_message': constant.SuccessMessage.REGISTRATION_SUCCESS
                })
        except IntegrityError:
            # if something went wrong on DB side - put redis data back
            # todo: expiration time must not "reset" to 1 day again
            redis_instance.setex(registration_hash, REGISTRATION_EXPIRATION_TIME, registration_request)
            return render(request, 'register.html', context={
                'error_message': constant.ErrorMessage.REGISTRATION_USER_EXISTS
            })


class PasswordRecoveryView(View):
    def get(self, request, recovery_hash=None):
        if not recovery_hash:
            return render(request, 'password-recovery.html')
        password_recovery_request = redis_instance.get(recovery_hash)
        credentials = json.loads(password_recovery_request.decode())
        try:
            user = PollUser.objects.get(email=credentials.get('email'))
        except PollUser.DoesNotExist:
            return render(request, 'password-recovery.html', context={
                'error_message': constant.ErrorMessage.RECOVERY_NO_SUCH_USER
            })
        try:
            with transaction.atomic():
                user.set_password(credentials.get('password'))
                redis_instance.delete(recovery_hash)
                user.save()
            return render(request, 'login.html', context={'success_message': 'successfully changed'})
        except IntegrityError:
            redis_instance.setex(recovery_hash, REGISTRATION_EXPIRATION_TIME, password_recovery_request)
            return HttpResponse("404")

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
