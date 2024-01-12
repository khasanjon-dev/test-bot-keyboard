from datetime import datetime


def keys_serializer(text: str) -> str:
    if text.isalnum():
        res = ''
        for letter in text:
            if letter.isalpha():
                res += letter
        return res
    return text


def date_change_format(date: str):
    datetime_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z")
    formatted_time = datetime_object.strftime("%m/%d/%Y, %H:%M:%S")
    return formatted_time
