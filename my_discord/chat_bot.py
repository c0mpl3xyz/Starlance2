import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from manual import get_manual_link
from modal import JobModal, BankRegistrationModal
from selects import SelectRoles, SelectBankNames
from discord.ui import View
from usecases.get_user_jobs import GetUserJobs
from usecases.get_jobs_by_user_roles import GetJobsByUserRoles
from usecases.get_company_jobs import GetCompanyJobs
from utils.error_message_enums import ErrorMessageEnum, MessageEnum
# from usecases.get_company_jobs import GetCompanyJobs
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
URL = os.getenv('URL')
intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', intents=intents)
# client.interaction_timeout = INTERACTION_TIMEOUT

def is_influencer(interaction):
    roles = [role.name for role in interaction.user.roles]
    return 'Influencer' in roles

async def is_dm(interaction):
    try:
        if interaction.user.roles is None or len(interaction.user.roles) == 0:
            await interaction.response.send_message(ErrorMessageEnum.NOT_DM.value)
            return True
        else:
            return False
    except AttributeError:
        await interaction.response.send_message(ErrorMessageEnum.NOT_DM.value)
        return True

@client.event
async def on_ready():
    synced = await client.tree.sync()
    print(f'I\'m Ready\nCommands {str(len(synced))}')

@client.tree.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(interaction: discord.Interaction): # a slash command will be created with the name "ping"
    await interaction.response.send_message(f"Pong! Latency is {client.latency}", ephemeral=True)

@client.tree.command(name='login')
async def login(interaction: discord.Interaction):
    if is_dm(interaction):
        return 
    
    if is_influencer(interaction):
        message = get_manual_link(interaction.user.id, interaction.user.name)
        await interaction.user.send(message)
        return await interaction.response.send_message(f'Log in link sent to user: <@{interaction.user.id}>', ephemeral=True)
    else:
        return await interaction.response.send_message(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)

@client.tree.command(name='bank_register')
async def bank_register(interaction: discord.Interaction):
    if is_dm(interaction):
        return
    
    if not is_influencer(interaction):
        return await interaction.response.send_message(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)
    
    view = discord.ui.View()
    view.add_item(SelectBankNames(URL))
    await interaction.user.send('Bank registration', view=view)
    await interaction.response.send_message(f'Bank registration form sent to <@{interaction.user.id}>', ephemeral=True)

@client.tree.command(name='my_jobs')
async def my_jobs(interaction: discord.Interaction):
    if is_dm(interaction):
        return

    if is_influencer(interaction):
        job_views = GetUserJobs().execute(interaction.user.id)
        if job_views is None or len(job_views) == 0:
            return await interaction.response.send_message(ErrorMessageEnum.NO_JOB.value + f'<@{interaction.user.id}>', ephemeral=True)
        else:
            for view in job_views:
                await interaction.user.send(view.description, view=view)
        return await interaction.response.send_message(f'Job list sent to <@{interaction.user.id}>', ephemeral=True)
    
    else:
        await interaction.response.send_message(ErrorMessageEnum.NOT_COMPANY.value, ephemeral=True)

@client.tree.command(name='all_jobs')
async def all_jobs(interaction: discord.Interaction):
    if is_dm(interaction):
        return

    if is_influencer(interaction):
        roles = [role.name for role in interaction.user.roles]
        job_views = GetJobsByUserRoles().execute(interaction.user.id, roles)
        if job_views is None or len(job_views) == 0:
            await interaction.user.send(ErrorMessageEnum.NO_JOB_ROLES.value)
        else:
            for view in job_views:
                await interaction.user.send(view.description, view=view)
        return await interaction.response.send_message(f'Job list sent to <@{interaction.user.id}>', ephemeral=True)
    else:
        return await interaction.response.send_message(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)

@client.tree.command(name='company_job_list')
async def company_job_list(interaction: discord.Interaction):
    if is_dm(interaction):
        return

    if not is_influencer(interaction):
        job_views = GetCompanyJobs().execute(interaction.user.guild.id)
        if job_views is None or len(job_views) == 0:
            return await interaction.response.send_message(ErrorMessageEnum.NO_JOB.value)
        else:
            for view in job_views:
                await interaction.channel.send(view.description, view=view)
        return await interaction.response.send_message(MessageEnum.SUCCESS.value)
    else:
        return await interaction.response.send_message(ErrorMessageEnum.NOT_COMPANY.value + f' <@{interaction.user.id}>', ephemeral=True)

@client.tree.command(name='company_job_add')
async def company_job_add(interaction: discord.Interaction):
    if is_dm(interaction):
        return
    
    if is_influencer(interaction):
        return await interaction.response.send_message(ErrorMessageEnum.NOT_COMPANY.value + f' <@{interaction.user.id}>', ephemeral=True)

    view = View()
    roles = [role.name for role in interaction.user.roles]
    view.add_item(SelectRoles(client, roles, URL))
    return await interaction.response.send_message('Select roles', view=view)

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    
#     print(message.author.id)
#     if message.content.startswith('!'):
#         await client.process_commands(message)
#         return

#     response = 'Welcome'
#     await message.channel.send(response)

client.run(TOKEN)