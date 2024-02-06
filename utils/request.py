import httpx

from root import settings

base_url = settings.bot.BASE_URL


class User:
    @staticmethod
    async def get(telegram_id: int) -> tuple:
        url = f'{base_url}/users/get-user/'
        context = {
            'telegram_id': telegram_id
        }
        response = httpx.post(url, data=context)
        return response.status_code, response.json()

    @staticmethod
    async def create(data: dict) -> dict:
        url = f'{base_url}/users/get-or-create/'
        response = httpx.post(url, data=data)
        return response.json()


class Block:
    @staticmethod
    async def create(data: dict) -> tuple:
        url = f'{base_url}/tests/block/'
        context = {
            'mandatory_keys': data['mandatory_keys'],
            'first_basic_keys': data['first_basic_keys'],
            'second_basic_keys': data['second_basic_keys'],
            'author': data['author']
        }
        response = httpx.post(url, data=context)
        return response.status_code, response.json()


class Science:
    @staticmethod
    async def create(data: dict) -> dict:
        url = f'{base_url}/tests/science/'
        context = {
            'name': data['name'],
            'keys': data['keys'],
            'author': data['id'],
        }
        response = httpx.post(url, data=context)
        return response.json()

    @staticmethod
    async def get(science_id: int) -> tuple:
        url = f'{base_url}/tests/science/{science_id}/'
        response = httpx.get(url)
        return response.status_code, response.json()


class Answer:
    @staticmethod
    async def create(data: dict) -> tuple:
        url = f'{base_url}/answers/science/'
        context = {
            "true_answers": data['true_answers'],
            "false_answers": data['false_answers'],
            "science": data['science'],
            "user": data['user']
        }
        response = httpx.post(url, data=context)
        return response.status_code, response.json()

    @staticmethod
    async def get(data: dict) -> tuple:
        url = f'{base_url}/answers/science/get-answer/'
        response = httpx.post(url, data=data)
        return response.status_code, response.json()


user = User()
block = Block()
science = Science()
answer = Answer()
