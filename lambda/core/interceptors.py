from ask_sdk_core.dispatch_components import AbstractRequestInterceptor, AbstractResponseInterceptor
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LoggingRequestInterceptor(AbstractRequestInterceptor):
    def process(self, handler_input):
        logger.debug("Request received: {}".format(handler_input.request_envelope.request))


class LoggingResponseInterceptor(AbstractResponseInterceptor):
    def process(handler_input, response):
        logger.debug("Response generated: {}".format(response))
