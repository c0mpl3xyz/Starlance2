import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from manual import get_manual_link

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('I\'m Ready')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('!'):
        await bot.process_commands(message)
        return

    response = 'Welcome'
    await message.channel.send(response)

@commands.command(name='temp')
async def foo(ctx, *arg):
    await ctx.send(' '.join(arg))

@bot.command(name='login')
async def send_form(ctx, *arg):
    username = 'test'

    if len(arg) > 0:
        username = arg[0]
    link = get_manual_link(username)
    await ctx.send(link)

bot.add_command(foo)
bot.run(TOKEN)
# if __name__ == '__main__':
    