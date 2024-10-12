import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from manual import get_manual_link
from selects import SelectRoles, SelectBankNames, MessageSelect
from discord.ui import View
from usecases.get_user_jobs import GetUserJobViews
from usecases.get_jobs_by_user_roles import GetJobsByUserRoles
from usecases.get_company_jobs import GetCompanyJobs, GetServerJobs
from utils.error_message_enums import ErrorMessageEnum, MessageEnum
from utils.enums import Enums
from datetime import datetime
from usecases.user_reviews import * 
from modal import EmonosModal
from usecases.user_contents import *
from views import LogInView
from usecases.company_contents import GetCompanyContentView
from usecases.get_user import GetUserStatus, GetUsersReport
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio, os, uuid, aiofiles, pytz
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
URL = os.getenv('URL')

print(f'{TOKEN=}')
print(f'{URL=}')
print(f'{Enums.ROLES.value}')
print(f'{Enums.GUILD_ID.value}')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)
timezone = pytz.timezone('Asia/Ulaanbaatar')
scheduler = AsyncIOScheduler()

def send_message():
    guild = client.get(Enums.GUILD_ID.value)
    channel = discord.utils.get(guild.channels, name=Enums.LEADER_BOARD.value)
    if channel:
        pass

# scheduler.add_job(send_message, CronTrigger(day_of_week=0, ="0"))

def is_main_server(intearaction) -> bool:
    return intearaction.guild.id == Enums.GUILD_ID.value

def is_our_company(intearaction) -> bool:
    return intearaction.guild.id == Enums.OUR_COMPANY.value
    
def is_influencer(roles):
    return Enums.ROLES.value in roles
    # return True

def is_admin(roles):
    return Enums.ADMIN.value in roles
    # return True

def is_dm(interaction):
    try:
        guild_id = Enums.GUILD_ID.value
        guild = client.get_guild(guild_id)
        user = discord.utils.get(guild.members, id=interaction.user.id)
        if not user:
            return []

        return [role.name for role in user.roles]
    except AttributeError as e:
        return []

@client.event
async def on_ready():
    synced = await client.tree.sync()
    print(f'I\'m Ready\nCommands {str(len(synced))}')
    scheduler.start()

@client.event
async def on_message(message):
    # Prevent the bot from responding to its own messages
    if message.author == client.user:
        return
    
    # Check if the message is a DM
    response = 'Welcome to the UGC Mongolia, Please contact UGC Mongolia server Admins'
    try:
        if message.guild is None:
            # Your response
            await message.channel.send(response)
    except:
        await message.channel.send(response)

@client.tree.command(description="Sends the bot's latency.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! Latency is {client.latency}", ephemeral=True)

@client.tree.command(name='bank_register')
async def bank_register(interaction: discord.Interaction):
    await interaction.response.defer()
    roles = is_dm(interaction)
    
    if not is_influencer(roles):
        return await interaction.followup.send(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)
    
    view = discord.ui.View()
    view.add_item(SelectBankNames(URL))
    await interaction.user.send(view=view)
    await interaction.followup.send(f'Bank registration form sent to <@{interaction.user.id}>', ephemeral=True)

@client.tree.command(name='e_monos')
async def e_monos(interaction: discord.Interaction):
    # roles = is_dm(interaction)
    
    # if not is_influencer(roles):
    #     return await interaction.followup.send(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)
     
    modal = EmonosModal()
    await interaction.response.send_modal(modal)

@client.tree.command(name='my_jobs')
async def my_jobs(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    roles = is_dm(interaction)
    if is_influencer(roles):
        job_views = GetUserJobViews().execute(interaction.user.id, client)
        if job_views is None or len(job_views) == 0:
            await interaction.followup.send(ErrorMessageEnum.NO_JOB.value + f'<@{interaction.user.id}>', ephemeral=True)
        else:
            for view in job_views:
                view.message = await interaction.user.send(embed=view.embed, view=view)
                await asyncio.sleep(1.5)

            await interaction.followup.send(f'Job list sent to <@{interaction.user.id}>', ephemeral=True)
    
    else:
        await interaction.followup.send(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)
    
@client.tree.command(name='my_contents')
async def my_contents(interaction: discord.Interaction):
    await interaction.response.defer()
    roles = is_dm(interaction)

    if is_influencer(roles):
        content_views = GetUserContentView().execute(interaction.user.id, client)
        if content_views is None or len(content_views) == 0:
            await interaction.followup.send(ErrorMessageEnum.NO_CONTENT.value + f'<@{interaction.user.id}>', ephemeral=True)
        else:
            for view in content_views:
                view.message = await interaction.user.send(embed=view.embed, view=view)
                await asyncio.sleep(1.5)
            await interaction.followup.send(f'Content list sent to <@{interaction.user.id}>', ephemeral=True)
    
    else:
        await interaction.followup.send(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)

@client.tree.command(name='my_reviews')
async def my_reviews(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    roles = is_dm(interaction)

    if not is_influencer(roles):
        review_views = GetUserReviewView().execute(interaction.user.id, client)
        if review_views is None or len(review_views) == 0:
            await interaction.followup.send(ErrorMessageEnum.NO_REVIEWS.value + f'<@{interaction.user.id}>', ephemeral=True)
        else:
            for view in review_views:
                view.message = await interaction.user.send(embed=view.embed, view=view)
                await asyncio.sleep(1.5)
            await interaction.followup.send(f'Review list sent to <@{interaction.user.id}>', ephemeral=True)
    else:
        await interaction.followup.send(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)

@client.tree.command(name='my_new_jobs')
async def my_new_jobs(interaction: discord.Interaction):
    await interaction.response.defer()
    roles = is_dm(interaction)

    if is_influencer(roles):
        job_views = GetJobsByUserRoles().execute(interaction.user.id, roles, client)
        if job_views is None or len(job_views) == 0:
            await interaction.user.send(ErrorMessageEnum.NO_JOB_ROLES.value)
        else:
            for view in job_views:
                view.message = await interaction.user.send(embed=view.embed, view=view)
                await asyncio.sleep(1.5)
        return await interaction.followup.send(f'Job list sent to <@{interaction.user.id}>', ephemeral=True)
    else:
        return await interaction.followup.send(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)

@client.tree.command(name='my_status')
async def my_status(interaction: discord.Interaction):
    await interaction.response.defer()
    roles = is_dm(interaction)

    if is_influencer(roles):
        get_user_status = GetUserStatus()
        user_views = await get_user_status.execute(interaction.user.id, client)
        if user_views is None or len(user_views) == 0:
            await interaction.user.send(ErrorMessageEnum.NO_USER.value)
        else:
            for view in user_views:
                view.message = await interaction.user.send(embed=view.embed, view=view)
                await asyncio.sleep(1.5)
        return await interaction.followup.send(f'User status sent to <@{interaction.user.id}>', ephemeral=True)
    else:
        return await interaction.followup.send(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)

@client.tree.command(name='company_job_add')
async def company_job_add(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    roles = is_dm(interaction)
    
    if is_influencer(roles):
        return await interaction.followup.send(ErrorMessageEnum.NOT_COMPANY.value + f' <@{interaction.user.id}>', ephemeral=True)

    try:
        if is_main_server(interaction):
            return await interaction.followup.send(ErrorMessageEnum.FOR_COMPANY.value, ephemeral=True)
        
        else:
            view = View()
            guild = client.get_guild(interaction.guild.id)
            roles = [role.name for role in guild.roles]
            select = SelectRoles(client, roles, URL)
            view.add_item(select)
            channel = discord.utils.get(interaction.guild.channels, name=Enums.JOB.value)
            if not channel:
                channel = interaction.channel
            if channel:
                select.message = await channel.send('Add new Job here \nSelect roles', view=view)

            await interaction.followup.send(f'Job add sent to <#{channel.id}>')
    except AttributeError:
        return await interaction.followup.send(ErrorMessageEnum.FOR_COMPANY.value, ephemeral=True)

@client.tree.command(name='company_jobs')
async def company_jobs(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    roles = is_dm(interaction)

    if is_influencer(roles):
        return await interaction.followup.send(ErrorMessageEnum.NOT_COMPANY.value + f' <@{interaction.user.id}>', ephemeral=True)

    try:
        if is_main_server(interaction):
            return await interaction.followup.send(ErrorMessageEnum.FOR_COMPANY.value, ephemeral=True)

        job_views = GetCompanyJobs().execute(interaction.user.guild.id, client)
        if job_views is None or len(job_views) == 0:
            return await interaction.followup.send(ErrorMessageEnum.NO_JOB.value)
        else:
            channel = discord.utils.get(interaction.guild.channels, name=Enums.JOB.value)
            if not channel:
                channel = interaction.channel
            for view in job_views:
                view.message = await channel.send(embed=view.embed, view=view)
                await asyncio.sleep(1.5)
        return await interaction.followup.send(f'Job list sent to <#{channel.id}>')
    except AttributeError:
        return await interaction.followup.send(ErrorMessageEnum.FOR_COMPANY.value, ephemeral=True)

@client.tree.command(name='company_contents')
async def company_contents(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    roles = is_dm(interaction)
    
    if is_influencer(roles):
        return await interaction.followup.send(ErrorMessageEnum.NOT_COMPANY.value, ephemeral=True)

    try:
        if is_main_server(interaction):
            return await interaction.followup.send(ErrorMessageEnum.FOR_COMPANY.value, ephemeral=True)

        else:
            content_views = GetCompanyContentView().execute(interaction.guild.id, client)
            if content_views is None or len(content_views) == 0:
                await interaction.followup.send(ErrorMessageEnum.NO_CONTENT.value + f'<@{interaction.user.id}>', ephemeral=True)
            else:
                channel = discord.utils.get(interaction.guild.channels, name=Enums.CONTENT.value)
                if not channel:
                    channel = interaction.channel
                for view in content_views:
                    view.message = await channel.send(embed=view.embed, view=view)
                    await asyncio.sleep(1.5)
                await interaction.followup.send(f'Content list sent to <#{channel.id}>', ephemeral=True)
    except AttributeError:
        return await interaction.followup.send(ErrorMessageEnum.FOR_COMPANY.value, ephemeral=True)

@client.tree.command(name='server_reviews')
async def server_reviews(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    roles = is_dm(interaction)

    if not is_admin(roles):
        return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)
    
    try:
        if not is_main_server(interaction):
            return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)
        
        review_views = GetServerReviewView().execute(client)
        if review_views is None or len(review_views) == 0:
            await interaction.followup.send(ErrorMessageEnum.NO_REVIEWS.value + f'<@{interaction.user.id}>', ephemeral=True)
        else:
            channel = discord.utils.get(interaction.guild.channels, name=Enums.REVIEW.value)
            if not channel:
                channel = interaction.channel
            for view in review_views:
                view.message = await channel.send(embed=view.embed, view=view)
                await asyncio.sleep(1.5)
            await interaction.followup.send(f'Review list sent to <#{channel.id}>', ephemeral=True)
    except AttributeError:
        return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)

@client.tree.command(name='server_contents')
async def server_contents(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    roles = is_dm(interaction)

    if not is_admin(roles):
        return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)
    
    try:
        if not is_main_server(interaction):
            return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)
        
        content_views = GetServerContentView().execute(client)
        if content_views is None or len(content_views) == 0:
            await interaction.followup.send(ErrorMessageEnum.NO_CONTENT.value + f'<@{interaction.user.id}>', ephemeral=True)
        else:
            channel = discord.utils.get(interaction.guild.channels, name=Enums.CONTENT.value)
            if not channel:
                channel = interaction.channel
            for view in content_views:
                view.message = await channel.send(embed=view.embed, view=view)
                await asyncio.sleep(1.5)
            await interaction.followup.send(f'Content list sent to <#{channel.id}>', ephemeral=True)
    except AttributeError:
        return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)

@client.tree.command(name='server_approves')
async def server_approves(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    roles = is_dm(interaction)

    if not is_admin(roles):
        return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)
    
    try:
        if not is_main_server(interaction):
            return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)
        
        approve_views = GetServerApprovementView().execute(client)
        if approve_views is None or len(approve_views) == 0:
            try:
                await interaction.followup.send(ErrorMessageEnum.NO_APPROVES.value + f'<@{interaction.user.id}>', ephemeral=True)
            except discord.errors.InteractionResponded:
                await interaction.followup.send(ErrorMessageEnum.NO_APPROVES.value + f'<@{interaction.user.id}>', ephemeral=True)
        else:
            channel = discord.utils.get(interaction.guild.channels, name=Enums.APPROVE_GUILD.value)
            if not channel:
                channel = interaction.channel
            for view in approve_views:
                view.message = await channel.send(embed=view.embed, view=view)
                await asyncio.sleep(1.5)
            await interaction.followup.send(f'Approvement list sent to <#{channel.id}>', ephemeral=True)
    except AttributeError:
        return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)

@client.tree.command(name='server_jobs')
async def server_jobs(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    roles = is_dm(interaction)

    if not is_admin(roles):
        return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)
    
    try:
        if not is_main_server(interaction):
            return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)
        
        job_views = GetServerJobs().execute(client)
        if job_views is None or len(job_views) == 0:
            try:
                await interaction.followup.send(ErrorMessageEnum.NO_JOB.value + f'<@{interaction.user.id}>', ephemeral=True)
            except discord.errors.InteractionResponded:
                await interaction.followup.send(ErrorMessageEnum.NO_JOB.value + f'<@{interaction.user.id}>', ephemeral=True)
        else:
            channel = discord.utils.get(interaction.guild.channels, name=Enums.JOB.value)
            if not channel:
                channel = interaction.channel
            for view in job_views:
                view.message = await channel.send(embed=view.embed, view=view)
                await asyncio.sleep(1.5)
            await interaction.followup.send(f'Job list sent to <#{channel.id}>', ephemeral=True)
    except AttributeError:
        return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)

@client.tree.command(name='server_collects')
async def server_collects(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    roles = is_dm(interaction)

    if not is_admin(roles):
        return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)
    
    try:
        if not is_main_server(interaction):
            return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)
        
        collect_views = GetServerCollectView().execute(client)
        if collect_views is None or len(collect_views) == 0:
            try:
                await interaction.followup.send(ErrorMessageEnum.NO_COLLECT.value + f'<@{interaction.user.id}>', ephemeral=True)
            except discord.errors.InteractionResponded:
                await interaction.followup.send(ErrorMessageEnum.NO_COLLECT.value + f'<@{interaction.user.id}>', ephemeral=True)
        else:
            channel = discord.utils.get(interaction.guild.channels, name=Enums.COLLECT.value)
            if not channel:
                channel = interaction.channel
            for view in collect_views:
                view.message = await channel.send(embed=view.embed, view=view)
                await asyncio.sleep(1.5)
            await interaction.followup.send(f'Collect request list sent to <#{channel.id}>', ephemeral=True)
    except AttributeError:
        return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)

@client.tree.command(name="server_user_id", description="Get the user ID of a member")
@app_commands.describe(member="The member whose user ID you want to retrieve")
async def server_user_id(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer()
    roles = is_dm(interaction)
    
    if not is_admin(roles):
        return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)
    
    if not isinstance(member, discord.Member):
        return await interaction.response.send_message('You entered wrong User')

    await interaction.followup.send(f'ID: {str(member.id)}\nName: {member.name}')

@client.tree.command(name="server_users_report", description="Get Users Report")
async def server_users_report(interaction: discord.Interaction):
    await interaction.response.defer()

    roles = is_dm(interaction)
    if not is_admin(roles):
        return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)

    get_report = GetUsersReport()
    report = await get_report.execute()

    if report:
        file_name = str(uuid.uuid1()) + '.docx'
        async with aiofiles.open(file_name, 'wb') as f:
            await f.write(report)
        
        timezone = pytz.timezone('Asia/Ulaanbaatar')
        date = datetime.now(timezone)
        date_str = date.strftime('%Y_%m_%d')
        download_file_name = f'users_report_{date_str}.docx'
        file = discord.File(file_name, filename=download_file_name)
        
        channel = discord.utils.get(interaction.guild.channels, name=Enums.NOTIFICATION.value)
        if not channel:
            channel = interaction.channel

        await channel.send('Users Report:', file=file)
        await interaction.followup.send(f'User report sent to <#{channel.id}>')
        os.remove(file_name)
    else:
        await interaction.followup.send('Failed to fetch the user report.', ephemeral=True)

# @client.tree.command(name="get_user_report", description="Get the user ID of a member")
# @app_commands.describe(member="The member whose user ID you want to retrieve")
async def server_user_report(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer()
    roles = is_dm(interaction)
    
    if not is_admin(roles):
        return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)
    
    if not isinstance(member, discord.Member):
        return await interaction.response.send_message('You entered wrong User')

# @client.tree.command(name='ig_login')
# async def login(interaction: discord.Interaction):
#     await interaction.response.defer()
    
#     connections = await interaction.user.fetch_connections()
#     for connection in connections:
#         print(connection.type)
#     view = LogInView(interaction.user.id, interaction.user.name)
#     await interaction.user.send('Login with Facebook', view=view, embed=view.embed)
#     return await interaction.followup.send(f'Log in link sent to user: <@{interaction.user.id}>', ephemeral=True)

@client.tree.command(name='ig_login')
async def login(interaction: discord.Interaction):
    await interaction.response.defer()
    roles = is_dm(interaction)

    # if is_influencer(interaction):
    #     return await interaction.followup.send(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)
    
    # if is_main_server(interaction):
    #     return await interaction.followup.send(ErrorMessageEnum.NOT_MAIN.value, ephemeral=True)
    
    # else:
    view = LogInView(interaction.user.id, interaction.user.name)
    await interaction.user.send('Login with Facebook', view=view, embed=view.embed)
    return await interaction.followup.send(f'Log in link sent to user: <@{interaction.user.id}>', ephemeral=True)

client.run(TOKEN)