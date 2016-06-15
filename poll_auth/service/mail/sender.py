import json
import platform
import requests
from dj_docs.settings import redis_instance, SENDGRID_URL
from poll_auth.service.mail.templates import PasswordRecoveryTemplate, RegistrationConfirmationTemplate

if platform.system() == 'Windows':
    from threading import Thread as Process
else:
    from multiprocessing import Process as Process


def start_publishing():
    def publish():
        pubsub = redis_instance.pubsub()
        pubsub.subscribe('registration_email_channel')
        for raw_message in pubsub.listen():
            try:
                if raw_message['type'] == 'message':
                    registration_data = json.loads(raw_message['data'].decode())
                    if registration_data.get('service') == 'registration':
                        template_class = RegistrationConfirmationTemplate
                    else:
                        template_class = PasswordRecoveryTemplate
                    template = template_class(registration_data.get('email'),
                                              registration_data.get('registration_hash'))
                    requests.post(SENDGRID_URL,
                                  data=json.dumps(template.__str__()),
                                  headers=template.headers,
                                  verify=False)
            except Exception as e:
                print(e)

    p = Process(target=publish)
    p.daemon = True
    p.start()
