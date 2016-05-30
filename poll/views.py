import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from poll.models import PollUser


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
        email = request.POST.get('email')
        password = request.POST.get('password')
        new_user = PollUser(email=email)
        new_user.set_password(password)
        try:
            new_user.is_active = True
            new_user.save()
            return HttpResponse(response_message(success=True,
                                                 text='Ви успішно зарєструвались',
                                                 info=True))
        except IntegrityError:
            return HttpResponse(response_message(success=False,
                                                 error=True,
                                                 text='Такий користувач вже існує'))


class LogoutView(View):

    def post(self, request):
        logout(request)
        return HttpResponse(response_message(success=True))
