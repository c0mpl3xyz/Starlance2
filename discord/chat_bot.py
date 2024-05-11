import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from manual import get_manual_link
from modal import JobModal
from selects import SelectRoles
from discord import app_commands
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    synced = await client.tree.sync()
    print(f'I\'m Ready\nCommands {str(len(synced))}')

@client.tree.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(interaction: discord.Interaction): # a slash command will be created with the name "ping"
    await interaction.response.send_message(f"Pong! Latency is {client.latency}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!'):
        await client.process_commands(message)
        return

    print(message)
    response = 'Welcome'
    print(response)
    await message.channel.send(response)

@client.tree.command(name='login')
async def send_form(interaction: discord.Interaction):
    link = get_manual_link(interaction.user.id, interaction.user.name)
    await interaction.response.send_message(link)

@client.tree.command()
async def job_add(interaction: discord.Interaction):
    view = discord.ui.View()
    select_roles = SelectRoles(roles=['role1', 'role2', 'role3', 'role4', 'role5'])
    view.add_item(select_roles)
    response = await interaction.response.send_message('hi', view=view)
    print(response)

client.run(TOKEN)
# if __name__ == '__main__':
    