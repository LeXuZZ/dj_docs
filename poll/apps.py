from django.apps import AppConfig

from service.subscribers import document_creator


class PollConfig(AppConfig):
    name = 'poll'
    document_creator()
