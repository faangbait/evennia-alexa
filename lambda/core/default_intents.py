from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_core.utils import is_request_type, is_intent_name
from core.websocket_protocol import SetupWebSocket
from templates.response_template import FallbackResponse
from ask_sdk_model.ui import SimpleCard
import ask_sdk_core.utils as ask_utils
import logging
import asyncio

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        """
        Args:
            handler_input: HandlerInput Object

        Returns:
            (HandlerInput) -> bool
        """
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        """

        Handles the launch of the skill. Since no 'command' is in session_attributes,
        this will follow the websocket_protocol default for what happens when a command
        isn't available ('look')

        Args:
            handler_input: HandlerInput Object

        Returns:
            Response
        """
        logger.debug("Handling Launch Request")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SetupWebSocket(handler_input))
        return handler_input.response_builder.response


#        return handler_input

# return FallbackResponse(handler_input)


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        """
        Args:
            handler_input: HandlerInput Object

        Returns:
            bool
        """
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        """
        Args:
            handler_input: HandlerInput Object

        Returns:
            Response
        """
        speech_text = "Try saying commands like 'look' or 'move'. For a full list of comands and gameplay tips, visit our website at https://trhr.invertedspectra.com"

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Tidebreak Help", speech_text)
        )
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        try:
            loop = asyncio.get_running_loop()
            loop.close()
        except Exception:
            pass
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return handler_input.response_builder.speak(speak_output).response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class UnitTestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("UnitTest")(handler_input)

    def handle(self, handler_input):
        from templates.response_template import build_template

        responses = {
            "speech": "Test speech returned",
            "text": "Test text returned",
            "card_type": "simple",
            "card_title": "Tidebreak",
            "onscreen_primary": "On-screen text",
        }
        x = build_template(handler_input, responses)
        logger.debug(x)
