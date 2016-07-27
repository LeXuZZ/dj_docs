import logging
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
from poll.models import *
from util.response import response_message


logger = logging.getLogger("DJ_DOCS")


@ensure_csrf_cookie
def get_csrf(request):
    return HttpResponse("")


class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')


class PollView(View):

    def get(self, request, pk=None):
        if pk:
            try:
                poll = Poll.objects.get(pk=pk)
                return response_message(success=True, data=poll.json_serialize())
            except Poll.DoesNotExist:
                return response_message(success=False, error=True, text='no such poll')

        return response_message(success=True, data=Poll.objects.json_serialize_all())

    def post(self, request, pk):
        user = request.user
        try:
            poll = Poll.objects.get(pk=pk)
        except Poll.DoesNotExist:
            return response_message(success=False, error=True, text='no such poll')
        name, json = request.POST.get("name"), request.POST.get("json")
        try:
            result = PollResult.objects.create(
                user=user,
                poll=poll,
                poll_result=json
            )
            result.save()
            return response_message(success=True)
        except IntegrityError:
            return response_message(success=False, error=True, text='cannot save poll to db')
