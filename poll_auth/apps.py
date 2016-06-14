from django.apps import AppConfig
from poll_auth.service.mail.sender import start_publishing


class AuthConfig(AppConfig):
    name = 'poll_auth'

    def ready(self):
        super().ready()
        start_publishing()
