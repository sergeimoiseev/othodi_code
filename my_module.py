import logging

# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def foo():
    logger.info('Hi, foo')
    logger.debug('Hi, foo')
    print("in foo --module")

class Bar(object):
    def bar(self):
        logger.info('Hi, bar')
        logger.debug('Hi, bar')
        print("in bar --module")