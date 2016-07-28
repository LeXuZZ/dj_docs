from django.apps import AppConfig

from service.mail.sender import email_sender


class AuthConfig(AppConfig):
    name = 'poll_auth'

    def ready(self):
        super().ready()
        email_sender()
