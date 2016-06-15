import platform
import requests
from dj_docs.settings import redis_instance, SENDGRID_URL, SENDGRID_API_KEY

if platform.system() == 'Windows':
    from threading import Thread as Process
else:
    from multiprocessing import Process as Process


def start_publishing():
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % SENDGRID_API_KEY
    }

    def publish():
        pubsub = redis_instance.pubsub()
        pubsub.subscribe('email_send_channel')
        for raw_message in pubsub.listen():
            try:
                if raw_message['type'] == 'message':
                    requests.post(SENDGRID_URL,
                                  data=raw_message['data'],
                                  headers=headers,
                                  verify=False)
            except Exception as e:
                print(e)

    p = Process(target=publish)
    p.daemon = True
    p.start()
