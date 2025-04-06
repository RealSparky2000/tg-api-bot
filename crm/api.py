import aiohttp
import os
import json
import crm.api_requests as crm_requests
import asyncio
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API")

async def make_request(method, endpoint, data=None):
    url = f"{API_URL}/{endpoint}"

    try:
        async with aiohttp.ClientSession() as session:
            if method == "GET":
                async with session.get(url, params=data) as response:
                    response.raise_for_status()
                    return await response.json()
            elif method == "POST":
                async with session.post(url, json=data) as response:
                    response.raise_for_status()
                    return await response.json()
            elif method == "PUT":
                async with session.put(url, json=data) as response:
                    response.raise_for_status()
                    return await response.json()
            elif method == "DELETE":
                async with session.delete(url, json=data) as response:
                    response.raise_for_status()
                    return await response.json()
            else:
                raise ValueError(f"Неподдерживаемый метод: {method}")

    except aiohttp.ClientError as e:
        print(f"Ошибка при запросе {endpoint}: {e}")
        return None

async def add_lead(user_data):
    post_data = {
        "fields": {
            "TITLE": "Заполенная анкета",
            "NAME": user_data["name"],
            "COMMENTS": f"Telegram user ID: {user_data['tg_id']}",
            "UF_CRM_1743292532": user_data['age'],
            "UF_CRM_1743292547": user_data['activity'],
            "UF_CRM_1743292567": user_data['goal'],
            "UF_CRM_1743292559": user_data['average_income']
        }
    }
    json_response = await make_request("POST", crm_requests.ADD_LEAD, post_data)

    if json_response:
        return True
    else:
        return False

async def get_lead_by_tg_id(tg_id: str) -> bool:
    response = await make_request("POST", crm_requests.GET_LEAD_LIST, data={
        "filter": {"%COMMENTS": tg_id},
        "select": ["NAME", "COMMENTS"]
    })
    # print(type(response))
    # print(tg_id, type(tg_id), sep=" | ")

    existing_lead = any(tg_id in value["COMMENTS"] for value in response["result"])

    if existing_lead:
        return True
    else:
        return False
