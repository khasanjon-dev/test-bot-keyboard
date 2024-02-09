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


class Test:
    @staticmethod
    async def create_block(data: dict) -> tuple:
        url = f'{base_url}/tests/block/'
        context = {
            'keys': data['keys'],
            'author': data['author']
        }
        response = httpx.post(url, data=context)
        return response.status_code, response.json()

    @staticmethod
    async def get_block(block_id: int) -> tuple:
        url = f'{base_url}/tests/block/{block_id}/'
        response = httpx.get(url)
        return response.status_code, response.json()

    @staticmethod
    async def create_science(data: dict) -> dict:
        url = f'{base_url}/tests/science/'
        context = {
            'name': data['name'],
            'keys': data['keys'],
            'author': data['id'],
        }
        response = httpx.post(url, data=context)
        return response.json()

    @staticmethod
    async def get_science(science_id: int) -> tuple:
        url = f'{base_url}/tests/science/{science_id}/'
        response = httpx.get(url)
        return response.status_code, response.json()


class Answer:
    @staticmethod
    async def create_science(data: dict) -> tuple:
        url = f'{base_url}/answers/science/'
        context = {
            'false_keys': data['false_keys'],
            'science': data['science'],
            'user': data['user']
        }
        response = httpx.post(url, data=context)
        return response.status_code, response.json()

    @staticmethod
    async def get_science(data: dict) -> tuple:
        url = f'{base_url}/answers/science/get-answer/'
        context = {
            'user': data['user'],
            'science': data['science']
        }
        response = httpx.post(url, data=context)
        return response.status_code, response.json()

    @staticmethod
    async def get_block(data: dict) -> tuple:
        url = f'{base_url}/answers/block/get-answer/'
        context = {
            'user': data['user'],
            'block': data['block']
        }
        response = httpx.post(url, data=context)
        return response.status_code, response.json()

    @staticmethod
    async def create_block(data: dict) -> tuple:
        url = f'{base_url}/answers/block/'
        context = {
            'true_answers': data['true_answers'],
            'false_answers': data['false_answers'],
            'block': data['block'],
            'user': data['user']
        }
        response = httpx.post(url, data=context)
        return response.status_code, response.json()


user = User()
test = Test()
answer = Answer()
