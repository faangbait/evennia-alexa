from ask_sdk_core.utils import get_supported_interfaces
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.dialog import ElicitSlotDirective
import json
import logging
from utils.utils import _ERRORS

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Response:
    def __init__(self, handler_input):
        self.handler_input = handler_input

    def render(self):
        """
        Renders the appropriate handler based on the user's display.

        Calls:
            render_speech (func) : For speech-only interfaces
            render_card (func) : For speech+card interfaces
            render_apl (func) : For full APL interfaces
        """
        handler_input = self.handler_input
        if self.slot_to_elicit:
            logger.debug("Got a slot to elicit: {slot}".format(slot=self.slot_to_elicit))
            handler_input.response_builder.add_directive(
                ElicitSlotDirective(slot_to_elicit=self.slot_to_elicit)
            )

        logger.debug(
            "Supported interfaces: {sup}".format(sup=get_supported_interfaces(handler_input))
        )
        if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
            logger.debug("Rendering APL")
            return self.render_apl()
        elif supports_display(handler_input):
            logger.debug("Rendering card")
            return self.render_card()
        else:
            logger.debug("Rendering speech-only")
            return self.render_speech()

    def build_template(self, response_dict):
        """
        Converts received websocket variables into a usable template.

        Args:
            response_dict (dict)

        """

        self.raw_text = response_dict.get("text", [""])[0]
        self.card_text_verbose = strip_html(
            response_dict.get("card_text_verbose", [self.raw_text])[0]
        )
        self.card_text = strip_html(response_dict.get("card_text", [self.card_text_verbose])[0])
        self.card_title = strip_html(response_dict.get("card_title", ["Tidebreak"])[0])
        self.card_subtitle = response_dict.get("card_subtitle", [""])[0]
        self.card_type = response_dict.get("card_type", ["default"])[0]
        self.speech_verbose = response_dict.get("speech_verbose", [self.card_text])[0]
        self.speech_trunc = response_dict.get("speech_trunc", [self.speech_verbose])[0]
        self.reprompt = response_dict.get("reprompt", [self.speech_trunc])[0]
        self.exits = response_dict.get("exits", [])
        self.contents = response_dict.get("contents", [])
        self.hint_text = response_dict.get("hint_text", ["look"])[0]
        self.equipment = response_dict.get("equipment", [])
        self.background_image = response_dict.get("background_image", [""])[0]
        self.slot_to_elicit = response_dict.get("elicitSlot", [""])[0]
        self.end_session = False

    def render_speech(self):
        handler_input = self.handler_input
        try:
            if self.speech_verbose:
                handler_input.response_builder.speak(self.speech_verbose)
            if self.reprompt:
                handler_input.response_builder.ask(self.reprompt)
        except Exception as e:
            logger.debug("Exception in render_speech: {e}".format(e=e))
            handler_input.response_builder.speak(
                "This skill failed critically with error {error}".format(error=_ERRORS.get(101))
            )
        finally:
            return handler_input.response_builder.response

    def render_card(self):
        handler_input = self.handler_input
        try:
            if self.speech_verbose:
                handler_input.response_builder.speak(self.speech_verbose)
            if self.reprompt:
                handler_input.response_builder.ask(self.reprompt)
            if self.card_title or self.card_text_verbose:
                handler_input.response_builder.set_card(
                    SimpleCard(card_title=self.card_title, card_text=self.card_text_verbose)
                )
        except Exception as e:
            logger.debug("Exception in render_card: {e}".format(e=e))
            handler_input.response_builder.speak(
                "This skill failed critically with error {error}".format(error=_ERRORS.get(102))
            )
        finally:
            return handler_input.response_builder.response

    def render_apl(self):
        handler_input = self.handler_input
        try:
            apl_json = self.card_type + ".json"
            # data = _load_apl_document(apl_json).get("datasources")
            data = {
                "template_data": {
                    "type": "object",
                    "objectId": "bt2",
                    "backgroundImage": {
                        "contentDescription": None,
                        "smallSourceUrl": None,
                        "largeSourceUrl": None,
                        "sources": [],
                    },
                    "title": "Tidebreak",
                    "textContent": {
                        "title": {"type": "PlainText", "text": "Tidebreak"},
                        "subtitle": {"type": "PlainText", "text": ""},
                        "card_title": {"type": "PlainText", "text": ""},
                        "card_text": {"type": "PlainText", "text": ""},
                        "hint_text": {"type": "PlainText", "text": ""},
                    },
                    "uiContent": {
                        "exits": {"type": "Sequence", "data": [{"header": "You can go:"}]},
                        "contents": {"type": "Sequence", "data": [{"header": "You see:"}]},
                        "equipment": {"type": "Sequence", "data": []},
                        "player_stats": {"type": "Sequence", "data": []},
                        "enemy_stats": {"type": "Sequence", "data": []},

                    },
                }
            }
            document = _load_apl_document(apl_json).get("document")
        except Exception as e:
            logger.debug("Exception in render_apl: {e}".format(e=e))
            handler_input.response_builder.speak(
                "This skill failed critically with error {error}".format(error=_ERRORS.get(104))
            )
            return handler_input.response_builder.response

        try:
            data["template_data"]["backgroundImage"]["sources"] = [
                {
                    "url": "https://d2o906d8ln7ui1.cloudfront.net/images/BT2_Background.png",
                    "size": "small",
                    "widthPixels": 0,
                    "heightPixels": 0,
                },
                {
                    "url": "https://d2o906d8ln7ui1.cloudfront.net/images/BT2_Background.png",
                    "size": "large",
                    "widthPixels": 0,
                    "heightPixels": 0,
                },
            ]
            if self.background_image:
                data["template_data"]["backgroundImage"]["sources"]["url"] = self.background_image

        except Exception as e:
            logger.debug("Exception in render_apl: {e}".format(e=e))
            handler_input.response_builder.speak(
                "This skill failed critically with error {error}".format(error=_ERRORS.get(105))
            )
            return handler_input.response_builder.response

        try:
            data["template_data"]["title"] = "Tidebreak"

            if self.card_type in [
                "default",
            ]:
                data["template_data"]["textContent"]["card_text"]["text"] = self.raw_text

            if self.card_type in [
                "help",
            ]:
                # TODO: Back button visible
                pass
            if self.card_type in ["traverse", "help", "simple", "consider"]:
                data["template_data"]["textContent"]["card_title"]["text"] = self.card_title
                data["template_data"]["textContent"]["card_text"]["text"] = self.card_text

            if self.card_type in ["traverse", "character"] and self.contents:
                data["template_data"]["uiContent"]["contents"]["data"] += self.contents
            else:
                del data["template_data"]["uiContent"]["contents"]

            if self.card_type in ["traverse"] and self.exits:
                data["template_data"]["uiContent"]["exits"]["data"] += self.exits
            else:
                del data["template_data"]["uiContent"]["exits"]

            if self.card_type in ["character"]:
                data["template_data"]["uiContent"]["equipment"]["data"] += self.equipment

           # if self.card_type in ["consider"]:
            #    data["template_data"]["uiContent"]["player_stats"]["data"] += self.player_stats
             #   data["template_data"]["uiContent"]["enemy_stats"]["data"] += self.enemy_stats

            if self.hint_text:
                data["template_data"]["textContent"]["hint_text"]["text"] = self.hint_text

        except Exception as e:
            logger.debug("Exception in render_apl: {e}".format(e=e))
            #handler_input.response_builder.speak(
            #    "This skill failed critically with error {error}".format(error=_ERRORS.get(105))
            #)
            self.render_card()
            #return handler_input.response_builder.response

        try:
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(document=document, datasources=data, token=self.card_type,)
            )
        except Exception as e:
            logger.debug("Exception in render_apl: {e}".format(e=e))
            handler_input.response_builder.speak(
                "This skill failed critically with error {error}".format(error=_ERRORS.get(106))
            )
        finally:
            handler_input.response_builder.speak(self.speech_trunc)
            if self.reprompt:
                handler_input.response_builder.ask(self.reprompt)
            handler_input.response_builder.set_should_end_session(self.end_session)
            return self.handler_input.response_builder.response


def FallbackResponse(handler_input):
    handler_input.response_builder.speak("Tidebreak is full.").set_card(
        SimpleCard("Tidebreak Full!", "Try again later")
    )


def supports_display(handler_input):
    try:
        if hasattr(
            handler_input.request_envelope.context.system.device.supported_interfaces, "display"
        ):
            return (
                handler_input.request_envelope.context.system.device.supported_interfaces.display
                is not None
            )
    except:
        return False


def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)


def strip_html(html):
    s = SSMLStripper()
    s.feed(html)
    return s.get_data()


from html.parser import HTMLParser


class SSMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.full_str_list = []
        self.strict = False
        self.convert_charrefs = True

    def handle_data(self, d):
        self.full_str_list.append(d)

    def get_data(self):
        return "".join(self.full_str_list)
