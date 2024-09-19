import pytest
from facebook.message import FacebookMessenger
from dotenv import load_dotenv
import os

load_dotenv()
page_access_token = os.getenv('PAGE_ACCESS_TOKEN')
page_id = int(os.getenv('PAGE_ID'))
psid = int(os.getenv('PSID'))
media_url = os.getenv('MEDIA_URL')


@pytest.fixture
def messenger():
    return FacebookMessenger(page_access_token=page_access_token, page_id=page_id)


@pytest.mark.asyncio
async def test_send_message(messenger):
    response = await messenger.send_message(psid, 'test')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_send_media(messenger):
    response = await messenger.send_media(psid, media_url, 'image')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_send_message_invalid_data(messenger):
    response = await messenger.send_message(psid, '')
    assert response.status_code == 400
    assert response.message == '(#100) Message cannot be empty, must provide valid attachment or text'

    response = await messenger.send_message(0, 'test')
    assert response.status_code == 400
    assert response.message == '(#100) Parameter error: You cannot send messages to this id'



@pytest.mark.asyncio
async def test_send_media_invalid_data(messenger):
    response = await messenger.send_media(psid, 'https://aewfawddadawdawdsadadasdawdwefhjjjj/4ebb06d', 'image')
    assert response.status_code == 400
    assert response.message == '(#100) https://aewfawddadawdawdsadadasdawdwefhjjjj/4ebb06d should represent a valid URL'

    response = await messenger.send_media(psid, media_url, 'imaaaagie')
    assert response.status_code == 400
    assert response.message == '(#100) Param message[attachment][type] is not supported. Please check developer docs for details'

    response = await messenger.send_media(0, media_url, 'image')
    assert response.status_code == 400
    assert response.message == '(#100) Parameter error: You cannot send messages to this id'