import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from v2.service import command_service,chat_service
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
discord_bot = commands.Bot(command_prefix='!', intents=intents)
# 도커파일 테스투

@discord_bot.event
async def on_ready():
    print(f'Logged in as {discord_bot.user.name}')

@discord_bot.event
async def on_member_join(member):
    await command_service.send_welcome_message(member)

@discord_bot.command(name="설명")
async def show_help(ctx):
    member = ctx.author
    await command_service.send_welcome_message(member)

@discord_bot.command(name="캐릭터")
async def show_characters(ctx):
    await command_service.show_characters(ctx)

@discord_bot.command(name="비밀챗")
async def create_character(ctx, *, character_name: str):
    await command_service.create_private_channel(ctx, character_name)
@discord_bot.command(name = "전체")
async def create_public_channel(ctx, *,character_name: str):
    await command_service.create_public_channel(ctx, character_name)
@discord_bot.event
async def on_message(message):

    if message.author == discord_bot.user or message.webhook_id is not None or message.channel.id == 1344347307151196262:
        return
    if message.content.startswith('!'):
        return await discord_bot.process_commands(message)
    is_private =message.channel.nsfw
    await chat_service.process_chat(message,is_private)

if __name__ == '__main__':
    discord_bot.run(DISCORD_TOKEN)
