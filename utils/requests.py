import httpx

from root import settings

base_url = settings.bot.BASE_URL


async def get_user(telegram_id: int) -> tuple:
    url = f'{base_url}/user/get-user/'
    context = {
        'telegram_id': telegram_id
    }
    response = httpx.post(url, data=context)
    return response.status_code, response.json()


def create_user(data: dict) -> dict:
    url = f'{base_url}/user/get-or-create/'
    response = httpx.post(url, data=data)
    return response.json()


async def create_test(data: dict) -> dict:
    url = f'{base_url}/science/'
    context = {
        'name': data['name'],
        'keys': data['keys'],
        'size': data['size'],
        'author': data['id'],
    }
    response = httpx.post(url, data=context)
    return response.json()


async def create_block_test(data: dict) -> dict:
    url = f'{base_url}/block/'
    context = {
        'keys': data['keys'],
        'author': data['id'],
        'size': data['size']
    }
    response = httpx.post(url, data=context)
    return response.json()
