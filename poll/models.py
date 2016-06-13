import json
from django.db import models

from poll_auth.models import PollUser


class Poll(models.Model):
    name = models.CharField(max_length=255)
    json = models.TextField()

    def json_serialize(self):
        return json.dumps({
            'name': self.name,
            'json': self.json
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

    def __str__(self):
        return 'poll: %s. username: %s' % (self.poll.name, self.user.email)

    def json_serialize(self):
        return json.dumps({
            'user': self.user.json_serialize(),
            'poll': self.poll.json_serialize()
        })
