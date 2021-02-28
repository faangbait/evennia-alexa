from ask_sdk_model.ui import SimpleCard, StandardCard
from ask_sdk_model.interfaces.display import (
    ImageInstance,
    Image,
    RenderTemplateDirective,
    BackButtonBehavior,
    BodyTemplate2,
)
from ask_sdk_core.response_helper import get_rich_text_content
import logging
import json
from ask_sdk_core.utils import get_supported_interfaces
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def build_template(
    handler_input, response_dict={}, template_name="simple", end_session=False,
):
    """
    Builds a jinja response template

    Args:
        handler_input
        response_dict (dict):
            speech
            card_type
            card_title
            onscreen_primary
            onscreen_secondary
            onscreen_tertiary
            reprompt
            image
            ...
        template_name (string)
        end_session (bool)
    """
    try:
        speech_text = response_dict.get("speech", None)
        card_type = response_dict.get("card_type", "simple")
        card_title = response_dict.get("card_title", "Tidebreak")
        onscreen_primary = response_dict.get("onscreen_primary", speech_text)
        onscreen_secondary = response_dict.get("onscreen_secondary", "")
        onscreen_tertiary = response_dict.get("onscreen_tertiary", "")
        reprompt = response_dict.get("reprompt", None)
        image = response_dict.get("image", None)
    except Exception:
        logger.debug("Error getting response_dict")
    # data_map = {
    #    "type": "APL",
    #    "version": "1.2",
    #    "description": "Tidebreak APL Response",
    #    "settings": {},
    #    "theme": "dark",
    #    "import": [{"name": "alexa-layouts", "version": "1.1.0"}],
    #    "resources": [],
    #    "styles": {},
    #    "onMount": [],
    #    "graphics": {},
    #    "commands": {},
    #    "layouts": {},
    #    "mainTemplate": {"parameters": ["payload"]},
    #    "items": [],
    # }
    # data_map.get("items").append(
    #    {
    #        "type": "Text",
    #        "height": "100vh",
    #        "textAlign": "center",
    #        "textAlignVertical": "center",
    #        "text": onscreen_primary,
    #    }
    # )

    if speech_text:
        handler_input.response_builder.speak(speech_text)

    if card_type:
        card = StandardCard(title=card_title, text=onscreen_primary)
        handler_input.response_builder.set_card(card)

    if get_supported_interfaces(handler_input).alexa_presentation_apl is not None:
        datasources = _load_apl_document("tidebreak.json").get("datasources")
        datasources.get("bodyTemplate2Data")["title"] = "Tidebreak"
        datasources.get("bodyTemplate2Data").get("textContent").get("title")["text"] = card_title
        datasources.get("bodyTemplate2Data").get("textContent").get("primaryText")[
            "text"
        ] = onscreen_primary
        datasources.get("bodyTemplate2Data").get("textContent").get("exits")[
            "text"
        ] = onscreen_tertiary
        datasources.get("bodyTemplate2Data").get("textContent").get("contents")[
            "text"
        ] = onscreen_secondary

        handler_input.response_builder.add_directive(
            RenderDocumentDirective(
                document=_load_apl_document("tidebreak.json").get("document"),
                datasources=datasources,
                token="tidebreakToken",
            )
        )

    elif supports_display(handler_input):
        text = get_rich_text_content(
            primary_text=onscreen_primary,
            secondary_text=onscreen_secondary,
            tertiary_text=onscreen_tertiary,
        )
        handler_input.response_builder.add_directive(
            RenderTemplateDirective(BodyTemplate2(title=card_title, text_content=text))
        )
    else:
        pass

    if reprompt:
        handler_input.response_builder.ask(reprompt)

    handler_input.response_builder.set_should_end_session(end_session)
    return handler_input.response_builder.response


#    try:
#        logger.debug("Returning templated response: {dict}".format(dict=data_map))
#        return handler_input.generate_template_response(
#            template_name, data_map, file_ext="jinja"
#        )  # TODO: A bunch of conditionals to render the template based on whats received
#    except Exception as e:
#        logger.debug("Got exception in templated response generator, {e}".format(e=e))
#        return handler_input.response_builder.speak(data_map["speech_text"]).response


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
