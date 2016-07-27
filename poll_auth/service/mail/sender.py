import requests
import logging
from dj_docs.settings import redis_instance, SENDGRID_URL, SENDGRID_API_KEY
from util.decorators import redis_subscribe

logger = logging.getLogger('DJ_DOCS')


@redis_subscribe(redis_instance, 'email_send_channel')
def email_sender(raw_message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % SENDGRID_API_KEY
    }
    requests.post(SENDGRID_URL,
                  data=raw_message['data'],
                  headers=headers,
                  verify=False)
