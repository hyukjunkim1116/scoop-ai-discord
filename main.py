import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from service import UserService as userService
from service import CharacterService as characterService
from service import ChatService as chatService

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
discord_bot = commands.Bot(command_prefix='!', intents=intents)


@discord_bot.event
async def on_member_join(member):
    await userService.initialize_user(member.id)
    await userService.send_welcome_message(member)


@discord_bot.event
async def on_member_remove(member):
    await userService.delete_user(member, discord)


@discord_bot.event
async def on_message(message):
    if message.author == discord_bot.user or message.webhook_id is not None:
        return
    if message.content.startswith('!'):
        return await discord_bot.process_commands(message)
    roles = message.author.roles
    role_names = [role.name for role in roles]
    if str(message.channel.id) not in role_names:
        return
    return await chatService.process_chat(message)


@discord_bot.command(name="캐릭터생성")
async def create_character(ctx, *, character_name: str):
    await characterService.initialize_character(ctx, character_name)


@discord_bot.command(name="성별")
async def create_gender(ctx, *, gender: str):
    await characterService.create_gender(ctx, gender)


@discord_bot.command(name="소개")
async def create_intro(ctx, *, intro: str):
    await characterService.create_intro(ctx, intro)


@discord_bot.command(name="mbti")
async def create_mbti(ctx, *, mbti: str):
    await characterService.create_mbti(ctx, mbti)


@discord_bot.command(name="시작호감도")
async def create_init_affection(ctx, *, init_affection: int):
    await characterService.create_init_affection(ctx, init_affection)


@discord_bot.command(name="세계관")
async def create_world_view(ctx, *, world_view: str):
    await characterService.create_world_view(ctx, world_view)


@discord_bot.command(name="첫메세지")
async def create_init_chat(ctx, *, init_chat: str):
    await characterService.create_init_chat(ctx, init_chat)


@discord_bot.command(name="처음상황")
async def create_init_situation(ctx, *, init_situation: str):
    await characterService.create_init_situation(ctx, init_situation)


@discord_bot.command(name="비밀")
async def create_secret(ctx, *, secret: str):
    await characterService.create_secret(ctx, secret)


@discord_bot.command(name="이미지프롬프트")
async def create_image(ctx, *, image_prompt: str):
    print(image_prompt, "image_prompt")
    await characterService.create_image(ctx, image_prompt)


@discord_bot.command(name="확인")
async def get_confirm_list(ctx):
    await characterService.get_confirm_list(ctx, discord)


@discord_bot.command(name="시작")
async def init_chat(ctx):
    print("init chat")
    # 올바른 역할 찾기 방법 (방법 1: discord.utils.get 사용)
    role_name = str(ctx.channel.id)
    exist_role = discord.utils.get(ctx.author.roles, name=role_name)
    print(exist_role, "exist_role")
    if exist_role is None:
        role = await ctx.guild.create_role(
            name=str(ctx.channel.id),
            reason="Character chat access role in this channel"
        )
        await ctx.author.add_roles(role)
    await characterService.init_chat(ctx)


@discord_bot.command(name="다시시작")
async def restart_chat(ctx):
    await characterService.restart_chat(ctx)


@discord_bot.command(name="설명")
async def show_help(ctx):
    """봇 명령어 사용법을 보여줍니다."""

    embed = discord.Embed(
        title="🤖 Scoop AI 캐릭터 챗봇 사용 설명서",
        description="나만의 AI 캐릭터를 만들고 대화해보세요!",
        color=0x00b0f4  # 파란색 계열
    )

    # 캐릭터 생성 및 관리
    embed.add_field(
        name="🎭 캐릭터 생성 및 시작",
        value=(
            "**`!시작`** - 캐릭터와의 대화를 시작합니다. (모든 설정 완료 후)\n"
            "**`!확인`** - 현재 캐릭터의 설정 상태를 확인합니다."
        ),
        inline=False
    )

    # 캐릭터 설정
    embed.add_field(
        name="✏️ 캐릭터 설정하기",
        value=(
            "**`!성별 [내용]`** - 캐릭터의 성별을 설정합니다.\n"
            "**`!소개 [내용]`** - 캐릭터의 소개글을 설정합니다.\n"
            "**`!mbti [유형]`** - 캐릭터의 MBTI 성격 유형을 설정합니다.\n"
            "**`!시작호감도 [0~100]`** - 캐릭터의 초기 호감도를 설정합니다.\n"
            "**`!세계관 [내용]`** - 캐릭터가 속한 세계관을 설정합니다.\n"
            "**`!처음상황 [내용]`** - 대화가 시작되는 상황을 설정합니다.\n"
            "**`!첫메세지 [내용]`** - 캐릭터가 처음 보낼 메시지를 설정합니다.\n"
            "**`!비밀 [내용]`** - 캐릭터의 비밀이나 숨겨진 설정을 추가합니다.\n"
            "**`!이미지프롬프트 [내용]`** - 캐릭터 이미지 생성용 프롬프트를 설정합니다."
        ),
        inline=False
    )

    # 사용 예시
    embed.add_field(
        name="📝 사용 예시",
        value=(
            "1. **`!캐릭터생성 나기사`** - '나기사'라는 이름의 캐릭터 생성\n"
            "2. **`!성별 여성`**, **`!mbti ENFP`** 등으로 캐릭터 속성 설정\n"
            "3. **`!확인`** - 모든 필요한 설정이 완료되었는지 확인\n"
            "4. **`!시작`** - 캐릭터와 대화 시작\n"
            "5. 이제 채널에 일반 메시지를 입력하면 캐릭터와 대화할 수 있습니다!"
        ),
        inline=False
    )

    # 팁
    embed.add_field(
        name="💡 팁",
        value=(
            "• 모든 설정은 캐릭터의 채널에서 입력해야 합니다.\n"
            "• 캐릭터 설정이 많을수록 더 개성있는 대화가 가능합니다.\n"
            "• 세계관과 상황 설정을 자세히 적으면 캐릭터의 대답이 더 풍부해집니다."
        ),
        inline=False
    )

    embed.set_footer(text="Powered by Scoop AI | 추가 도움이 필요하면 관리자에게 문의하세요.")

    await ctx.send(embed=embed)


if __name__ == '__main__':
    discord_bot.run(DISCORD_TOKEN)
