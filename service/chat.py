from datetime import datetime
from repository import CharacterRepository as characterRepository
from repository import ChatRepository as chatRepository
from repository import ChatGenerator as chatGenerator
from .embed import EmbedService as embedService


class ChatService:

    async def process_chat(self, message):
        user_id = message.author.id
        channel_id = message.channel.id
        character = characterRepository().get_character_by_channel_id(channel_id)
        recent_chats = chatRepository().get_recent_chats_asc(user_id, channel_id)
        chat_summary = chatRepository().get_chat_summary_asc(user_id, channel_id)

        # 새 메시지가 10개 쌓일 때마다 요약 업데이트
        if len(recent_chats) > 10 and len(recent_chats) % 2 == 0:
            new_chat_summary = self._get_summary_and_delete_chats(user_id, channel_id, recent_chats[:10])
            chat_summary.append(new_chat_summary)
            recent_chats = recent_chats[10:]

        # 현재 메시지 추가
        now_chat = message.content

        # 응답 생성(self,character, recent_chats, chat_summary, now_chat)
        character_chat,character_situation,character_affection = await chatGenerator().generate_response(character, recent_chats,
                                                                                      chat_summary, now_chat)
        print(character_chat, "character_chat")
        print(character_situation, "character_situation")
        print(character_affection, "character_affection")

        embed = embedService().get_chat_embed(character_situation,character_chat,character_affection)
        await self._send_chat(character, embed)
        # 채팅 저장 및 반환
        character_situation_chat = f"{character_situation}\n{character_chat}"
        chatRepository().save_chat(user_id, channel_id, "human", now_chat)
        chatRepository().save_chat(user_id, channel_id, "ai", character_situation_chat, character_affection)

    @staticmethod
    async def _get_summary_and_delete_chats(user_id, channel_id, recent_chats):
        new_chat_summary = await chatGenerator().generate_summary(recent_chats)
        chatRepository().delete_chats(user_id, channel_id, recent_chats)
        chatRepository().save_summary(user_id, channel_id, new_chat_summary)
        return new_chat_summary

    @staticmethod
    async def _send_chat(character, embed):
        import aiohttp
        import json

        # 웹훅 URL로 메시지 전송
        webhook_url = character["webhook_url"]
        character_image_url = character.get("character_image_url", "")
        async with aiohttp.ClientSession() as session:

            webhook_data = {
                "content": "",
                "username": character["character_name"],
                "embeds": [embed.to_dict()]
            }
            if character_image_url:
                webhook_data["avatar_url"] = character_image_url
            embed.set_footer(text=f"{datetime.now().strftime('%Y-%m-%d %H:%M')}")
            async with session.post(webhook_url, data=json.dumps(webhook_data),
                                    headers={"Content-Type": "application/json"}) as resp:
                return resp.status == 204

    async def init_chat(self,ctx):
        character = characterRepository().get_character_by_channel_id(ctx.channel.id)
        init_situation = character.get("init_situation")
        init_chat = character.get("init_chat")
        init_affection = character.get("init_affection")
        start_chat = ""
        if init_situation is not None:
            start_chat += f"{init_situation}\n"
        if init_chat is not None:
            start_chat += f"{init_chat}\n"
        start_chat = start_chat.rstrip("\n")
        if start_chat == "":
            await ctx.send("먼저 채팅을 시작해보세요!")
        else:
            embed = embedService().get_chat_embed(init_situation, init_chat, init_affection)
            await self._send_chat(character, embed)
            chatRepository().save_chat(ctx.author.id, ctx.channel.id, "ai", start_chat, init_affection)
