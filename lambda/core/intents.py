from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from core.websocket_protocol import SetupWebSocket

import logging
import asyncio

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MoveIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("MoveIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        handler_input.attributes_manager.session_attributes["command"] = "move {direction}".format(
            direction=slots["direction"].value
        )
        logger.debug("Handling Move Intent")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SetupWebSocket(handler_input))
        return handler_input.response_builder.response


class LookIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("LookIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        handler_input.attributes_manager.session_attributes["command"] = "look {object}".format(
            object=slots["object"].value or ""
        )
        logger.debug("Handling Look Intent")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SetupWebSocket(handler_input))
        return handler_input.response_builder.response


class CharUpdateIntent(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("CharacterUpdateIntent")(handler_input)

    def handle(self, handler_input):
        logger.debug("Handling CharUpdate Intent")
        slots = handler_input.request_envelope.request.intent.slots
        handler_input.attributes_manager.session_attributes[
            "command"
        ] = "charupdate {rating}".format(rating=slots["numerical_rating"].value)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SetupWebSocket(handler_input))
        return handler_input.response_builder.response


class CheckInventoryIntent(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("CheckInventoryIntent")(handler_input)

    def handle(self, handler_input):
        logger.debug("Handling CheckInventoryIntent")
        handler_input.attributes_manager.session_attributes["command"] = "inventory"
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SetupWebSocket(handler_input))
        return handler_input.response_builder.response


class GetIntent(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("GetIntent")(handler_input)

    def handle(self, handler_input):
        logger.debug("Handling GetIntent")
        slots = handler_input.request_envelope.request.intent.slots
        handler_input.attributes_manager.session_attributes["command"] = "get {item}".format(
            item=slots["item"].value
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SetupWebSocket(handler_input))
        return handler_input.response_builder.response


class DropIntent(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("DropIntent")(handler_input)

    def handle(self, handler_input):
        logger.debug("Handling DropIntent")
        slots = handler_input.request_envelope.request.intent.slots
        handler_input.attributes_manager.session_attributes["command"] = "drop {item}".format(
            item=slots["item"].value
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SetupWebSocket(handler_input))
        return handler_input.response_builder.response


class ListIntent(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("ListIntent")(handler_input)

    def handle(self, handler_input):
        logger.debug("Handling ListIntent")
        handler_input.attributes_manager.session_attributes["command"] = "list"
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SetupWebSocket(handler_input))
        return handler_input.response_builder.response


class SellIntent(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("SellIntent")(handler_input)

    def handle(self, handler_input):
        logger.debug("Handling SellIntent")
        slots = handler_input.request_envelope.request.intent.slots
        handler_input.attributes_manager.session_attributes["command"] = "sell {item}".format(
            item=slots["item"].value
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SetupWebSocket(handler_input))
        return handler_input.response_builder.response


class BuyIntent(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BuyIntent")(handler_input)

    def handle(self, handler_input):
        logger.debug("Handling BuyIntent")
        slots = handler_input.request_envelope.request.intent.slots
        handler_input.attributes_manager.session_attributes["command"] = "buy {item}".format(
            item=slots["item"].value
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SetupWebSocket(handler_input))
        return handler_input.response_builder.response


class DonIntent(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("DonIntent")(handler_input)

    def handle(self, handler_input):
        logger.debug("Handling DonIntent")
        slots = handler_input.request_envelope.request.intent.slots
        handler_input.attributes_manager.session_attributes["command"] = "don {item}".format(
            item=slots["item"].value
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SetupWebSocket(handler_input))
        return handler_input.response_builder.response


class DoffIntent(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("DoffIntent")(handler_input)

    def handle(self, handler_input):
        logger.debug("Handling DoffIntent")
        slots = handler_input.request_envelope.request.intent.slots
        handler_input.attributes_manager.session_attributes["command"] = "doff {item}".format(
            item=slots["item"].value
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SetupWebSocket(handler_input))
        return handler_input.response_builder.response


class AttackIntent(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AttackIntent")(handler_input)

    def handle(self, handler_input):
        logger.debug("Handling AttackIntent")
        slots = handler_input.request_envelope.request.intent.slots
        handler_input.attributes_manager.session_attributes["command"] = "kill {target}".format(
            target=slots["target"].value
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SetupWebSocket(handler_input))
        return handler_input.response_builder.response

class GoInCharacterIntent(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("GoInCharacter")(handler_input)

    def handle(self, handler_input):
        logger.debug("Handling GoInCharacter")
        handler_input.attributes_manager.session_attributes["command"] = "ic"
        loop = asyncio.get_event_loop()
        loop.run_until_complete(SetupWebSocket(handler_input))
        return handler_input.response_builder.response