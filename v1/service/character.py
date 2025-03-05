from v1.repository import CharacterRepository as characterRepository
from v1.repository import ChatRepository as chatRepository
from v1.image import ImageGenerator
class CharacterService:

    @staticmethod
    async def initialize_character(ctx, character_name: str):
        print("create_character called")
        if character_name == "":
            return await ctx.send("캐릭터 이름을 입력해주세요. 예시: !캐릭터생성 <캐릭터이름>")
        guild = ctx.guild
        user = ctx.author

        channel = await guild.create_text_channel(name=f"{character_name}")
        await channel.edit(nsfw=True)
        webhook = await channel.create_webhook(name=channel.id)

        characterRepository().initialize_character(character_name, user.id,channel.id,webhook.url)
        await channel.set_permissions(guild.default_role, read_messages=False)
        await channel.set_permissions(user, read_messages=True, send_messages=True)

        await ctx.send(f"{channel.mention}에서 `{character_name}`와 대화를 시작하세요!")
        # 새로 생성된 채널에 메시지 보내기
        await channel.send(f"안녕하세요, {user.mention}님! `{character_name}` 캐릭터 채널이 생성되었습니다.")
        await channel.send("!설명 입력하여 명령어 목록을 확인하고 프롬프트를 작성해보세요!")
    @staticmethod
    async def get_character_by_channel_id(channel_id):
        # 데이터베이스에서 채널 ID로 캐릭터 정보 조회
        return characterRepository().get_character_by_channel_id(channel_id)

    # 기존 메서드들은 공통 메서드를 호출하도록 변경
    @staticmethod
    async def create_gender(ctx, gender: str):
        return await CharacterService.update_character_attribute(ctx, "gender", gender, "성별")

    @staticmethod
    async def create_intro(ctx, intro: str):
        return await CharacterService.update_character_attribute(ctx, "intro", intro, "소개")

    @staticmethod
    async def create_mbti(ctx, mbti: str):
        return await CharacterService.update_character_attribute(
            ctx, "mbti", mbti, "MBTI", lambda x: x.upper()
        )

    @staticmethod
    async def create_init_affection(ctx, init_affection: int):
        return await CharacterService.update_character_attribute(ctx, "init_affection", init_affection, "초기 호감도")

    @staticmethod
    async def create_world_view(ctx, world_view: str):
        return await CharacterService.update_character_attribute(ctx, "world_view", world_view, "세계관")

    @staticmethod
    async def create_init_chat(ctx, init_chat: str):
        return await CharacterService.update_character_attribute(ctx, "init_chat", init_chat, "초기 대화")

    @staticmethod
    async def create_init_situation(ctx, init_situation: str):
        # 문자열 앞뒤에 괄호 추가
        modified_init_situation = f"({init_situation})"
        return await CharacterService.update_character_attribute(ctx, "init_situation", modified_init_situation, "초기 상황")

    @staticmethod
    async def create_secret(ctx, secret: str):
        return await CharacterService.update_character_attribute(ctx, "secret", secret, "비밀")

    @staticmethod
    async def create_image(ctx, image_prompt: str):
        image_url = ImageGenerator().generate_image(image_prompt)
        return await CharacterService.update_character_attribute(ctx, "character_image_url", image_url, "이미지")




    @staticmethod
    async def update_character_attribute(ctx, field_name, value, display_name=None, transform_func=None):
        character = characterRepository().get_character_by_channel_id(ctx.channel.id)
        if not character:
            await ctx.send("이 채널에 연결된 캐릭터가 없습니다.")
            return False

        # 값 변환이 필요하면 적용
        if transform_func:
            value = transform_func(value)

        # 필드 업데이트
        result = characterRepository().update_character(
            character["_id"],
            {field_name: value}
        )

        # 표시 이름이 없으면 필드 이름 사용
        display_name = display_name or field_name

        if result.modified_count > 0 or result.matched_count > 0:
            # 필드별 성공 메시지 출력
            if field_name == "gender":
                await ctx.send(f"캐릭터의 성별이 '{value}'로 설정되었습니다.")
            elif field_name == "mbti":
                await ctx.send(f"캐릭터의 MBTI가 '{value}'로 설정되었습니다.")
            else:
                await ctx.send(f"캐릭터의 {display_name}이(가) 설정되었습니다.")
            return True
        else:
            await ctx.send("캐릭터 정보 업데이트에 실패했습니다.")
            return False


    @staticmethod
    async def restart_chat(ctx):
        character = characterRepository().get_character_by_channel_id(ctx.channel.id)
        chatRepository.delete_all_by_channel_id(ctx.channel.id)
        start_chat = character.get("init_chat", "먼저 채팅을 시작해보세요")
        await ctx.send(start_chat)
