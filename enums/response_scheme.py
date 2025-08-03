from enum import Enum


class ResponseFormat(str, Enum):
    RESPONSE_MODEL = "response_model"
    RESPONSE_DICTIONARY = "response_dict"
    RFC7807 = "rfc7807"