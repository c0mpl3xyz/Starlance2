import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from manual import get_manual_link
from modal import JobModal, BankRegistrationModal
from selects import SelectRoles, SelectBankNames
from discord.ui import View
from usecases.get_user_jobs import GetUserJobs
from usecases.get_company_jobs import GetCompanyJobs
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
URL = os.getenv('URL')
intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', intents=intents)

def is_influencer(interaction):
    roles = [role.name for role in interaction.user.roles]
    return 'Influencer' in roles

@client.event
async def on_ready():
    synced = await client.tree.sync()
    print(f'I\'m Ready\nCommands {str(len(synced))}')

@client.tree.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(interaction: discord.Interaction): # a slash command will be created with the name "ping"
    await interaction.response.send_message(f"Pong! Latency is {client.latency}")

@client.tree.command(name='login')
async def login(interaction: discord.Interaction):
    if is_influencer(interaction):
        message = get_manual_link(interaction.user.id, interaction.user.name)
    else:
        message = 'You are not influencer'
    await interaction.response.send_message(message)

@client.tree.command(name='job_add')
async def job_add(interaction: discord.Interaction):
    roles = [role.name for role in interaction.user.roles]
    if is_influencer(interaction):
        message = 'You don\'t have permission'
        return await interaction.response.send_message(message)

    view = View()
    view.add_item(SelectRoles(client, roles, URL))
    success = await interaction.response.send_message('Select roles', view=view)
    print(f'result: {success}')

@client.tree.command(name='bank_register')
async def bank_register(interaction: discord.Interaction):
    roles = interaction.user.roles
    role_names = [role.name for role in roles]

    # if 'Influencer' not in role_names:
    #     message = 'You don\'t have permission'
    #     return await interaction.response.send_message(message)

    view = discord.ui.View()
    view.add_item(SelectBankNames(URL))
    await interaction.response.send_message('Bank registration', view=view)

@client.tree.command(name='jobs')
async def jobs(interaction: discord.Interaction):
    # influencer = is_influencer(interaction)
    # if influencer:
    job_views = GetUserJobs().execute(interaction.user.id)
    for view in job_views:
        interaction.user.send(view.description, view=view)

client.run(TOKEN)
# if __name__ == '__main__':

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    
#     if message.content.startswith('!'):
#         await client.process_commands(message)
#         return

#     response = 'Welcome'
#     await message.channel.send(response)