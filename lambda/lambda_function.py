# -*- coding: utf-8 -*-

import logging
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_s3.adapter import S3Adapter
from core.default_intents import (
    LaunchRequestHandler,
    HelpIntentHandler,
    SessionEndedRequestHandler,
    IntentReflectorHandler,
    CatchAllExceptionHandler,
)
from core.intents import (
    MoveIntentHandler,
    LookIntentHandler,
    CharUpdateIntent,
    CheckInventoryIntent,
    GetIntent,
    DropIntent,
    ListIntent,
    SellIntent,
    BuyIntent,
    DonIntent,
    DoffIntent,
    AttackIntent,
    GoInCharacterIntent,
)
from core.interceptors import LoggingRequestInterceptor
from ask_sdk_core.view_resolvers import FileSystemTemplateLoader
from ask_sdk_jinja_renderer import JinjaTemplateRenderer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.debug("Initializing")

storage = S3Adapter(bucket_name="amzn1-ask-skill-59314ad7-6f29-buildsnapshotbucket-1m7jwign3zu2z")
sb = CustomSkillBuilder(persistence_adapter=storage)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(MoveIntentHandler())
sb.add_request_handler(LookIntentHandler())
sb.add_request_handler(CharUpdateIntent())
sb.add_request_handler(CheckInventoryIntent())
sb.add_request_handler(GetIntent())
sb.add_request_handler(DropIntent())
sb.add_request_handler(ListIntent())
sb.add_request_handler(SellIntent())
sb.add_request_handler(BuyIntent())
sb.add_request_handler(DonIntent())
sb.add_request_handler(DoffIntent())
sb.add_request_handler(AttackIntent())
sb.add_request_handler(GoInCharacterIntent())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler())  # INTENTREFLECTOR MUST BE LAST

sb.add_exception_handler(CatchAllExceptionHandler())

sb.add_global_request_interceptor(LoggingRequestInterceptor())
# sb.add_global_response_interceptor(LoggingResponseInterceptor())

sb.add_loader(FileSystemTemplateLoader(dir_path=".", encoding="utf-8"))
sb.add_renderer(JinjaTemplateRenderer())
lambda_handler = sb.lambda_handler()
