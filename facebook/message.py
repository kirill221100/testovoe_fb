import asyncio
import httpx
from pydantic import HttpUrl, BaseModel


class ResponseModel(BaseModel):
    status_code: int


class SuccessResponse(ResponseModel):
    recipient_id: int
    message_id: str


class ErrorResponse(ResponseModel):
    message: str
    type: str
    code: int
    fbtrace_id: str


class FacebookMessenger:
    def __init__(self, page_access_token: str, page_id: int):
        self.page_access_token = page_access_token
        self.page_id = page_id
        self.base_url = f'https://graph.facebook.com/v20.0/{self.page_id}/messages?platform=messenger&access_token={self.page_access_token}'

    async def send_message(self, psid: int, message_text: str):
        payload = {
            'recipient': {'id': psid},
            'message': {'text': message_text},
            'messaging_type': 'RESPONSE'
        }
        return await self._send_request(payload)

    async def send_media(self, psid: int, media_url: HttpUrl, media_type: str):
        payload = {
            'recipient': {'id': psid},
            'message': {
                'attachment': {
                    'type': media_type,
                    'payload': {
                        'url': media_url,
                        'is_reusable': True
                    }
                }
            }
        }
        return await self._send_request(payload)

    async def _send_request(self, message_data: dict):
        headers = {
            'Content-Type': 'application/json'
        }
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(self.base_url, headers=headers, json=message_data)
            response_json = response.json()
            if response.status_code == 200:
                return SuccessResponse(status_code=response.status_code, **response_json)
            else:
                return ErrorResponse(status_code=response.status_code, **response_json['error'])

