import json
import platform
from dj_docs.settings import APPLICATION_UUID, logger

if platform.system() == 'Windows':
    from threading import Thread as Process
else:
    from multiprocessing import Process as Process


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
        logger.debug('create redis listener on channel: %s' % self.channel_name)

    def __call__(self, func):

        def subscriber():
            pubsub = self.redis_session.pubsub()
            pubsub.subscribe(self.channel_name)

            for raw_message in pubsub.listen():
                try:
                    if raw_message['type'] == 'message':
                        logger.debug(
                            'received new message on channel: %s. message: %s' % (self.channel_name, raw_message))
                        try:
                            message = json.loads(raw_message.get('data'))
                        except ValueError:
                            logger.warn("%s. %s. Cannot load message" % (APPLICATION_UUID, func.__name__))
                            continue
                        if message.get('application_id') == APPLICATION_UUID:
                            func(message)
                except Exception as e:
                    logger.error(e)

        def wrapper():
            process = Process(target=subscriber)
            process.daemon = True
            process.start()

        return wrapper


class log_request:
    def __init__(self, logger):
        self.logger = logger

    def __call__(self, func):
        def wrapper(request, *args, **kwargs):
            session_key = request.session.session_key
            self.logger.info("%s. %s. %s. START" % (APPLICATION_UUID, func.__name__, session_key))
            self.logger.debug('%s. %s. %s. request: %s. request.POST: %s. request.GET: %s'
                              % (APPLICATION_UUID, func.__name__, session_key, request, request.POST, request.GET))
            return func(request, *args, **kwargs)

        return wrapper
