from service import CharacterService as characterService
class ChatService:
    @staticmethod
    async def process_chat(user_chat):
        character = await characterService.get_character_by_channel_id(user_chat.channel.id)
        if character:
            response = await ChatService.generate_chat(character, user_chat.content)
            await ChatService.send_character_chat(character, response)

    @staticmethod
    async def generate_chat(character, user_chat):
        # 여기에 AI 응답 생성 로직을 구현
        # 예: OpenAI API 호출 등
        return f"{character['character_name']}의 응답: {user_chat}에 대한 생각을 말해볼게요."

    @staticmethod
    async def send_character_chat(character, character_chat):
        import aiohttp
        import json

        # 웹훅 URL로 메시지 전송
        webhook_url = character["webhook_url"]
        character_image_url = character.get("character_image_url","")
        async with aiohttp.ClientSession() as session:
            webhook_data = {
                "content": character_chat,
                "username": character["character_name"],
            }

            if character_image_url:
                webhook_data["avatar_url"] = character_image_url

            async with session.post(webhook_url, data=json.dumps(webhook_data),
                                    headers={"Content-Type": "application/json"}) as resp:
                return resp.status == 204

