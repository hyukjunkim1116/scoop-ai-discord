from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from chat import test
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send(test())

if __name__ == '__main__':
    bot.run(TOKEN)
