import logging

import traceback


class ExceptionMessage(Exception):
    def __init__(self, m):
        self.message = m
       
        # logger = logging.getLogger(__name__)
        # logger.error('Logging Error: {0}'.format(m))
        # logging.exception('{0}'.format(m))
        logging.critical('{0}'.format(m))
        # logger.debug(u'Logging Error: "{}"'.format(m))

    def __str__(self):
        return self.message


