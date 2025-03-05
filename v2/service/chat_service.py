from v2.repository import ChannelRepository as channelRepository
from v2.repository import ChatGenerator as chatGenerator
from v2.repository import ChatRepository as chatRepository
from v2.repository import ContextChatGenerator as contextChatGenerator
from v2.image import ImageURL

async def process_chat(message,is_private):
        user_id = message.author.id
        username = message.author.display_name
        channel_id = message.channel.id
        channel_data = channelRepository().get_private_channel_by_channel_id(channel_id)
        character_name = channel_data.get("character_name")
        now_chat = message.content
        if is_private:
            ai_response = await contextChatGenerator().generate_private_response(character_name, now_chat,channel_id,username)
        else:
            ai_response = await chatGenerator().generate_public_response(character_name, now_chat)
        await _send_chat(channel_data,ai_response)

async def _send_chat(channel_data,ai_response):
        import aiohttp
        import json

        webhook_url = channel_data["webhook_url"]
        character_name = channel_data.get("character_name","")
        character_image_url = ImageURL.CHARACTER_MAP.value.get(character_name)
        async with aiohttp.ClientSession() as session:
            webhook_data = {
                "content": ai_response,
                "username": character_name,
                "tts":True
            }
            if character_image_url:
                webhook_data["avatar_url"] = character_image_url
            async with session.post(webhook_url, data=json.dumps(webhook_data),
                                    headers={"Content-Type": "application/json"}) as resp:
                text_sent= resp.status == 204
            return text_sent



