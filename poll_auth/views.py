import logging

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from dj_docs.settings import redis_session, REGISTRATION_EXPIRATION_TIME, REGISTRATION_HASH_LENGTH, \
    RECOVERY_PASSWORD_LENGTH
from poll_auth.models import *
from poll_auth.util import constant
from poll_auth.util.credentials import LoginCredentials, RegistrationCredentials, CredentialsValidationException
from poll_auth.util.helpers import generate_hash
from service.mail.templates import RegistrationConfirmationTemplate, PasswordRecoveryTemplate
from util.response import response_message
from dj_docs.settings import logger
from redis.exceptions import ConnectionError


class LoginView(View):
    def get(self, request):
        logger.debug("LoginView GET")
        return render(request, 'login.html')

    def post(self, request):
        try:
            user = LoginCredentials(**{str(k): request.POST.get(k) for k in request.POST}).user
            logger.debug('LoginView POST. user=%s', user)
        except CredentialsValidationException as error_message:
            logger.debug('LoginView POST. Login invalid. request.POST: %s', request.POST)
            return render(request, 'login.html', context={'error_message': error_message})
        login(request, user)
        logger.debug('LoginView POST. Login succeed for user %s' % user.email)
        return redirect("/")


class RegisterView(View):
    def post(self, request):
        try:
            credentials = RegistrationCredentials(**{str(k): request.POST.get(k) for k in request.POST})
            logger.debug('RegisterView POST. credentials: %s' % credentials)
        except CredentialsValidationException as error_message:
            logger.debug('RegisterView POST. credentials invalid: %s' % credentials)
            return render(request, 'register.html', {'error_message': error_message})

        registration_hash = generate_hash(REGISTRATION_HASH_LENGTH)
        logger.debug('RegisterView POST. registration hash: %s' % registration_hash)

        redis_session.setex(registration_hash, REGISTRATION_EXPIRATION_TIME, json.dumps(request.POST))
        redis_session.publish('email_send_channel',
                              json.dumps(
                                  RegistrationConfirmationTemplate(
                                      to=credentials.email, hash=registration_hash
                                  ).sendgrid_dump()
                              )
                              )
        logger.debug('RegisterView POST. credentials dispatched')
        return render(request, 'login.html', context={
            'success_message': constant.SuccessMessage.REGISTRATION_MAIL_SENT
        })

    def get(self, request, registration_hash=None):
        if not registration_hash:
            logger.debug('RegisterView GET')
            return render(request, 'register.html')
        try:
            logger.debug('RegisterView GET. registration hash: %s' % registration_hash)
            registration_request = redis_session.get(registration_hash)
            credentials = RegistrationCredentials(**json.loads(registration_request.decode()))
            logger.debug('RegisterView GET. registration hash: %s. credentials: %s' % (registration_hash, credentials))
        except AttributeError:
            # no such hash in redis
            logger.debug('RegisterView GET. hash was not found in redis. registration hash: %s' % registration_hash)
            return render(request, 'register.html', context={
                'error_message': constant.ErrorMessage.REGISTRATION_INVALID_HASH
            })
        except CredentialsValidationException as error_message:
            logger.debug('RegisterView GET. credentials are invalid.')
            return render(request, 'register.html', context={'error_message': error_message})
        except Exception:
            logger.debug('RegisterView GET. Bad request')
            return HttpResponse(status_code=400)

        user = PollUser(**credentials.poll_user_data())
        try:
            with transaction.atomic():
                user.set_password(credentials.password)
                user.save()
                redis_session.delete(registration_hash)
                logger.debug('RegisterView GET. User has been created. Registration successful')
                return render(request, 'login.html', context={
                    'success_message': constant.SuccessMessage.REGISTRATION_SUCCESS
                })
        except IntegrityError as e:
            # if something went wrong on DB side - put redis data back
            # todo: expiration time must not "reset" to 1 day again
            logger.error('RegisterView GET.', e)
            redis_session.setex(registration_hash, REGISTRATION_EXPIRATION_TIME, registration_request)
            return render(request, 'register.html', context={
                'error_message': constant.ErrorMessage.REGISTRATION_USER_EXISTS
            })


class PasswordRecoveryView(View):
    def get(self, request, recovery_hash=None):
        if not recovery_hash:
            logger.debug("PasswordRecoveryView GET")
            return render(request, 'password-recovery.html')
        password_recovery_request = redis_session.get(recovery_hash)
        credentials = json.loads(password_recovery_request.decode())
        logger.debug("PasswordRecoveryView GET. recovery_hash: %s. credentials: %s" % (recovery_hash, credentials))
        try:
            user = PollUser.objects.get(email=credentials.get('email'))
        except PollUser.DoesNotExist as e:
            logger.error("PasswordRecoveryView GET ", e)
            return render(request, 'password-recovery.html', context={
                'error_message': constant.ErrorMessage.RECOVERY_NO_SUCH_USER
            })
        try:
            with transaction.atomic():
                user.set_password(credentials.get('password'))
                redis_session.delete(recovery_hash)
                user.save()
            logger.debug("PasswordRecoveryView GET. Password was recovered successful")
            return render(request, 'login.html', context={'success_message': 'successfully changed'})
        except IntegrityError as e:
            logger.error("PasswordRecoveryView GET ", e)
            redis_session.setex(recovery_hash, REGISTRATION_EXPIRATION_TIME, password_recovery_request)
            return HttpResponse("404")

    def post(self, request):
        recovery_hash = generate_hash(REGISTRATION_HASH_LENGTH)
        new_password = generate_hash(RECOVERY_PASSWORD_LENGTH)
        logger.debug('PasswordRecoveryView POST. recovery_hash: %s. new_password: %s' % (recovery_hash, new_password))
        try:
            redis_session.setex(recovery_hash, REGISTRATION_EXPIRATION_TIME, json.dumps(
                {'email': request.POST.get('email'),
                 'password': new_password}
            ))
            redis_session.publish('email_send_channel', json.dumps(
                PasswordRecoveryTemplate(
                    to=request.POST.get('email'),
                    hash=recovery_hash,
                    new_password=new_password
                ).sendgrid_dump()))
        except ConnectionError as e:
            logger.error('PasswordRecoveryView POST. Cannot connect to Redis. ', e)
            return HttpResponse(status_code=400)
        return render(request, 'login.html',
                      context={'success_message': constant.SuccessMessage.PASSWORD_RECOVERY_MAIL_SENT})


class LogoutView(View):
    def get(self, request):
        logger.debug('LogoutView GET.')
        logout(request)
        return response_message(success=True)
