from django.apps import AppConfig

from poll.service import document_creator


class PollConfig(AppConfig):
    name = 'poll'
    document_creator()

