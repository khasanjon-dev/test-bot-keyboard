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
