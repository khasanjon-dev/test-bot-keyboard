import json
from datetime import datetime


def keys_serializer(text: str) -> json:
    keys = {}
    if text.isalnum():
        res = ''
        for letter in text:
            if letter.isalpha():
                res += letter
        text = res
    for i, value in enumerate(text, 1):
        keys.update({i: value})
    result = json.dumps(keys, indent=2)
    return result


async def check_answer(keys: str, keys_api: str) -> tuple:
    """
    return true and false answers count
    """
    true_answers, false_answers = 0, 0
    keys = keys_serializer(keys)
    for k1, k2 in zip(keys, keys_api):
        if k1 == k2:
            true_answers += 1
        else:
            false_answers += 1
    return true_answers, false_answers


def date_change_format(date: str):
    datetime_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")
    formatted_time = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
    return formatted_time
