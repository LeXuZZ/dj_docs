from dj_docs.settings import redis_session, logger
from poll.models import PollResult
from docxtpl import DocxTemplate

from util.decorators import redis_subscribe


@redis_subscribe(redis_session, 'document_creator_channel')
def document_creator(pk):
    try:
        pk = int(pk.decode())
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
