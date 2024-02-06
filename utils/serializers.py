import json
from datetime import datetime


async def keys_serializer(text: str, api=False) -> json:
    keys = {}
    if text.isalnum():
        res = ''
        for letter in text:
            if letter.isalpha():
                res += letter
        text = res
    for i, value in enumerate(text, 1):
        keys.update({str(i): value})
    if api:
        keys = json.dumps(keys, indent=2)
    return keys


async def check_answer(keys: dict, keys_api: dict) -> tuple:
    """
    return true and false answers dict
    """
    true_answers, false_answers = {}, {}
    for key in keys:
        if key in keys_api and keys[key] == keys_api[key]:
            true_answers[key] = keys[key]
        else:
            false_answers[key] = keys[key]
    return json.dumps(true_answers, indent=2), json.dumps(false_answers, indent=2)


def date_change_format(date: str):
    datetime_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")
    formatted_time = datetime_object.strftime("%H:%M:%S | %d-%m-%Y")
    return formatted_time
