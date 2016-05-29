from django.db import models


class Poll(models.Model):

    poll_file = models.FileField(upload_to='poll/surveys')