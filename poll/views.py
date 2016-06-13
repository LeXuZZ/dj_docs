from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
from poll.models import *
from util.response import response_message


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
