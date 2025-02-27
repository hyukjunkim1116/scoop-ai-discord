import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from service import UserService as userService
from service import CharacterService as characterService
from service import ChatService as chatService
from service import EmbedService as embedService
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
discord_bot = commands.Bot(command_prefix='!', intents=intents)


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
    return await chatService().process_chat(message)


@discord_bot.event
async def on_member_join(member):
    await userService.initialize_user(member.id)
    await userService.send_welcome_message(member)


@discord_bot.event
async def on_member_remove(member):
    print("Member left")
    await userService.delete_user(member, discord)


@discord_bot.command(name="캐릭터생성")
async def create_character(ctx, *, character_name: str):
    if ctx.channel.id != 1344347307151196262:
        return ctx.send("현재 채널에서 사용할 수 없습니다.")
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
    embed = embedService.get_confirm_list(ctx, discord)
    if embed:
        await ctx.send(embed=embed)
    else:
        await ctx.send("이 채널에 연결된 캐릭터가 없습니다.")


@discord_bot.command(name="시작")
async def init_chat(ctx):
    await chatService().init_chat(ctx)


@discord_bot.command(name="다시시작")
async def restart_chat(ctx):
    await characterService.restart_chat(ctx)


@discord_bot.command(name="설명")
async def show_help(ctx):
    embed = embedService().get_help_embed()
    await ctx.send(embed=embed)


if __name__ == '__main__':
    discord_bot.run(DISCORD_TOKEN)
