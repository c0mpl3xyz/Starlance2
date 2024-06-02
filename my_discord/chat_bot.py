import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from manual import get_manual_link
from selects import SelectRoles, SelectBankNames
from discord.ui import View
from usecases.get_user_jobs import GetUserJobViews
from usecases.get_jobs_by_user_roles import GetJobsByUserRoles
from usecases.get_company_jobs import GetCompanyJobs
from utils.error_message_enums import ErrorMessageEnum, MessageEnum
from embeds import UserEmbed
from datetime import datetime
from usecases.user_reviews import GetUserReview, GetUserReviewView, GetCompanyReviewView
from usecases.user_contents import GetUserContentView
from usecases.company_contents import GetCompanyContentView

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

# @client.tree.command(description='Status')
# async def status(interaction: discord.Interaction):
#     # if not await is_influencer(interaction):
#     #     return await interaction.response.send_message(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)
#     embed = UserEmbed(interaction.user.id, interaction.user.name)
#     await interaction.response.send_message(embed=embed)

@client.tree.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(interaction: discord.Interaction): # a slash command will be created with the name "ping"
    await interaction.response.send_message(f"Pong! Latency is {client.latency}", ephemeral=True)

@client.tree.command(name='login')
async def login(interaction: discord.Interaction):
    if await is_dm(interaction):
        return 
    
    if is_influencer(interaction):
        message = get_manual_link(interaction.user.id, interaction.user.name)
        await interaction.user.send(message)
        return await interaction.response.send_message(f'Log in link sent to user: <@{interaction.user.id}>', ephemeral=True)
    else:
        return await interaction.response.send_message(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)

@client.tree.command(name='bank_register')
async def bank_register(interaction: discord.Interaction):
    if await is_dm(interaction):
        return
    
    if not is_influencer(interaction):
        return await interaction.response.send_message(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)
    
    view = discord.ui.View()
    view.add_item(SelectBankNames(URL))
    await interaction.user.send(view=view)
    await interaction.response.send_message(f'Bank registration form sent to <@{interaction.user.id}>', ephemeral=True)

@client.tree.command(name='my_jobs')
async def my_jobs(interaction: discord.Interaction):
    if await is_dm(interaction):
        return

    # TODO: remove not
    if not is_influencer(interaction):
        await interaction.response.defer(ephemeral=True)
        job_views = GetUserJobViews().execute(interaction.user.id, client)
        if job_views is None or len(job_views) == 0:
            await interaction.followup.send(ErrorMessageEnum.NO_JOB.value + f'<@{interaction.user.id}>', ephemeral=True)
        else:
            for view in job_views:
                await interaction.user.send(embed=view.embed, view=view)
            await interaction.followup.send(f'Job list sent to <@{interaction.user.id}>', ephemeral=True)
    
    else:
        await interaction.response.send_message(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)
    
@client.tree.command(name='my_contents')
async def my_contents(interaction: discord.Interaction):
    if await is_dm(interaction):
        return

    # TODO: remove not
    if not is_influencer(interaction):
        await interaction.response.defer(ephemeral=True)
        content_views = GetUserContentView().execute(interaction.user.id, client)
        if content_views is None or len(content_views) == 0:
            await interaction.followup.send(ErrorMessageEnum.NO_CONTENT.value + f'<@{interaction.user.id}>', ephemeral=True)
        else:
            for view in content_views:
                await interaction.user.send(embed=view.embed, view=view)
            await interaction.followup.send(f'Content list sent to <@{interaction.user.id}>', ephemeral=True)
    
    else:
        await interaction.response.send_message(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)

@client.tree.command(name='my_reviews')
async def my_reviews(interaction: discord.Interaction):
    if await is_dm(interaction):
        return

    # TODO: remove not
    if not is_influencer(interaction):
        await interaction.response.defer(ephemeral=True)
        review_views = GetUserReviewView().execute(interaction.user.id, client)
        if review_views is None or len(review_views) == 0:
            await interaction.followup.send(ErrorMessageEnum.NO_REVIEWS.value + f'<@{interaction.user.id}>', ephemeral=True)
        else:
            for view in review_views:
                await interaction.user.send(embed=view.embed, view=view)
            await interaction.followup.send(f'Review list sent to <@{interaction.user.id}>', ephemeral=True)
    else:
        await interaction.response.send_message(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)

@client.tree.command(name='all_jobs')
async def all_jobs(interaction: discord.Interaction):
    if await is_dm(interaction):
        return

    if is_influencer(interaction):
        roles = [role.name for role in interaction.user.roles]
        job_views = GetJobsByUserRoles().execute(interaction.user.id, roles, client)
        if job_views is None or len(job_views) == 0:
            await interaction.user.send(ErrorMessageEnum.NO_JOB_ROLES.value)
        else:
            for view in job_views:
                await interaction.user.send(embed=view.embed, view=view)
        return await interaction.response.send_message(f'Job list sent to <@{interaction.user.id}>', ephemeral=True)
    else:
        return await interaction.response.send_message(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)

@client.tree.command(name='company_jobs')
async def company_jobs(interaction: discord.Interaction):
    if await is_dm(interaction):
        return

    if not is_influencer(interaction):
        job_views = GetCompanyJobs().execute(interaction.user.guild.id, client)
        if job_views is None or len(job_views) == 0:
            return await interaction.response.send_message(ErrorMessageEnum.NO_JOB.value)
        else:
            for view in job_views:
                await interaction.channel.send(embed=view.embed, view=view)
        return await interaction.response.send_message(MessageEnum.SUCCESS.value)
    else:
        return await interaction.response.send_message(ErrorMessageEnum.NOT_COMPANY.value + f' <@{interaction.user.id}>', ephemeral=True)

@client.tree.command(name='company_reviews')
async def company_reviews(interaction: discord.Interaction):
    if await is_dm(interaction):
        return

    if not is_influencer(interaction):
        await interaction.response.defer(ephemeral=True)
        review_views = GetCompanyReviewView().execute(interaction.guild.id, client)
        if review_views is None or len(review_views) == 0:
            await interaction.followup.send(ErrorMessageEnum.NO_REVIEWS.value + f'<@{interaction.user.id}>', ephemeral=True)
        else:
            for view in review_views:
                await interaction.channel.send(embed=view.embed, view=view)
            await interaction.followup.send(f'Review list sent to <@{interaction.user.id}>', ephemeral=True)
    else:
        await interaction.response.send_message(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)

@client.tree.command(name='company_contents')
async def company_contents(interaction: discord.Interaction):
    if await is_dm(interaction):
        return

    if not is_influencer(interaction):
        await interaction.response.defer(ephemeral=True)
        content_views = GetCompanyContentView().execute(interaction.guild.id, client)
        if content_views is None or len(content_views) == 0:
            await interaction.followup.send(ErrorMessageEnum.NO_CONTENT.value + f'<@{interaction.user.id}>', ephemeral=True)
        else:
            for view in content_views:
                await interaction.channel.send(embed=view.embed, view=view)
            await interaction.followup.send(f'Content list sent to <@{interaction.user.id}>', ephemeral=True)
    else:
        await interaction.response.send_message(ErrorMessageEnum.NOT_INFLUENCER.value, ephemeral=True)

@client.tree.command(name='company_job_add')
async def company_job_add(interaction: discord.Interaction):
    if await is_dm(interaction):
        return
    
    if is_influencer(interaction):
        return await interaction.response.send_message(ErrorMessageEnum.NOT_COMPANY.value + f' <@{interaction.user.id}>', ephemeral=True)

    view = View()
    roles = [role.name for role in interaction.user.roles]
    view.add_item(SelectRoles(client, roles, URL))
    return await interaction.response.send_message('Select roles', view=view)

# @client.tree.command(name='test_embed')
# async def test_embed(interaction: discord.Interaction):
#     some_url = "https://fallendeity.github.io/discord.py-masterclass/"
#     embed = discord.Embed(
#         title="Title",
#         description="Description",
#         url=some_url,
#         color=discord.Color.random(),
#         timestamp=datetime.utcnow()
#     )
#     embed.add_field(name="Field name", value="Color sets that <")
#     embed.add_field(name="Field name", value="Color should be an integer or discord.Colour object")
#     embed.add_field(name="Field name", value="You can't set image width/height")
#     embed.add_field(name="Non-inline field name", value="The number of inline fields that can shown on the same row is limited to 3", inline=False)
#     embed.set_author(name="Author", url=some_url,
#                      icon_url="https://cdn.discordapp.com/attachments/1112418314581442650/1124820259384332319/fd0daad3d291ea1d.png")
#     embed.set_image(url="https://cdn.discordapp.com/attachments/1028706344158634084/1124822236801544324/ea14e81636cb2f1c.png")
#     embed.set_thumbnail(url="https://media.discordapp.net/attachments/1112418314581442650/1124819948317986926/db28bfb9bfcdd1f6.png")
#     embed.set_footer(text="Footer", icon_url="https://cdn.discordapp.com/attachments/1112418314581442650/1124820375587528797/dc4b182a87ecee3d.png")
#     await interaction.response.send_message(embed=embed)

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     if message.content.startswith('!'):
#         await client.process_commands(message)
#         return

#     response = 'Welcome'
#     await message.channel.send(response)

client.run(TOKEN)