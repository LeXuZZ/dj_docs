import requests
from docxtpl import DocxTemplate

from dj_docs.settings import redis_session, SENDGRID_API_KEY, SENDGRID_URL, logger
from poll.models import PollResult
from util.decorators import redis_subscribe


@redis_subscribe(redis_session, 'email_send_channel')
def email_sender(message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % SENDGRID_API_KEY
    }
    requests.post(SENDGRID_URL,
                  data=message.get('template'),
                  headers=headers,
                  verify=False)


@redis_subscribe(redis_session, 'document_creator_channel')
def document_creator(message):
    try:
        pk = int(message.get('pk').decode())
    except ValueError as e:
        logger.error(e)
        return
    try:
        poll_result = PollResult.objects.get(pk=pk)
    except PollResult.DoesNotExist as e:
        logger.error(e)
        return

    for template in poll_result.poll.templates.objects.all():
        doc = DocxTemplate(template.file)
        doc.render(poll_result.poll_result)
        doc.save()
