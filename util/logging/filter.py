from dj_docs.settings import APPLICATION_UUID
import logging


class ApplicationUUIDFilter(logging.Filter):
    '''
    Inject application uuid to logging
    '''

    def filter(self, record):
        record.APPLICATION_UUID = APPLICATION_UUID
        return super().filter(record)
