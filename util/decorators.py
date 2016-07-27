import platform
import logging

if platform.system() == 'Windows':
    from threading import Thread as Process
else:
    from multiprocessing import Process as Process


logger = logging.getLogger('DJ_DOCS')


class redis_subscribe:
    '''
    decorator which allows to listen specific redis channel
    and publish received message to decorated function.
    Runs in separate thread (Windows) or process (Linux)
    '''

    def __init__(self, redis_session, channel_name):
        '''
        :param redis_session: redis_session = redis.StrictRedis()
        :param channel_name: str. name of subscribed channel
        '''
        self.redis_session = redis_session
        self.channel_name = channel_name

    def __call__(self, func):

        def subscriber():
            pubsub = self.redis_session.pubsub()
            pubsub.subscribe(self.channel_name)

            for raw_message in pubsub.listen():
                try:
                    if raw_message['type'] == 'message':
                        func(raw_message['data'])
                except Exception as e:
                    logger.error(e)

        def wrapper():
            process = Process(target=subscriber)
            process.daemon = True
            process.start()

        return wrapper
