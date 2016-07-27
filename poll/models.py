import json
from django.db import models

from dj_docs.settings import redis_instance
from poll_auth.models import PollUser


class Template(models.Model):
    name = models.CharField(max_length=255)
    template = models.FileField(upload_to='poll/template_files/docx/')


class Poll(models.Model):
    name = models.CharField(max_length=255)
    json = models.TextField()
    templates = models.ForeignKey(to=Template)

    def json_serialize(self):
        return json.dumps({
            'name': self.name,
            'json': self.json,
            'templates': [t for t in self.templates.all()]
        })

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.json = self.json\
            .replace('\r', '')\
            .replace('\n', '')\

        super().save()

    def __str__(self):
        return self.name


class PollResult(models.Model):
    user = models.ForeignKey(to=PollUser)
    poll = models.ForeignKey(to=Poll)
    poll_result = models.TextField()

    def json_serialize(self):
        return json.dumps({
            'user': self.user.json_serialize(),
            'poll': self.poll.json_serialize()
        })

    def save(self, *args, **kwargs):
        #  send id of finished poll to document creator service
        redis_instance.publish("document_creator_channel", self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return 'poll: %s. username: %s' % (self.poll.name, self.user.email)