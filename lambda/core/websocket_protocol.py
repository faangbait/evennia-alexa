import logging
import json
import aiohttp
from templates.response_template import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def SetupWebSocket(handler_input):
    return await ExecWebSocket(handler_input)


# REFACTORED 3/7/20
async def ExecWebSocket(handler_input):
    logger.debug("Starting websocket client")
    response_dict = {}
    try:
        csessid = handler_input.request_envelope.session.user.user_id[-30:]
    except AttributeError:
        csessid = "CSESSIDERROR"
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(
            "ws://trhr.invertedspectra.com:5000/?{csessid}".format(csessid=csessid)
        ) as ws:
            async for msg in ws:
                logger.debug(msg.json())
                if msg.type == aiohttp.WSMsgType.TEXT:
                    cmdarray = msg.json()
                    if "logged_in" in cmdarray[0]:
                        print("Logged in")
                        sent_text = handler_input.attributes_manager.session_attributes.get(
                            "command", "look"
                        )  # Default to 'look' command if no command)
                        await ws.send_str(json.dumps(["text", (sent_text), {}]))
                        logger.debug("Sent: {}".format(sent_text))

                    else:
                        try:
                            response_dict.update({cmdarray[0]: cmdarray[1]})
                        except Exception:
                            logger.warn("Problem with response in websocket")

                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    logger.debug("Got close signal")
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    logger.warn("Error condition in websockets")
                else:
                    logger.debug("Got a weird frame: {msg}".format(msg=msg.data))

    logger.debug("Websocket is closed, let's respond.")
    logger.debug(response_dict)

    response = Response(handler_input)
    response.build_template(response_dict)
    return response.render()
    # return build_template(handler_input, response_dict=response_dict)
