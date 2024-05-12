import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from manual import get_manual_link
from modal import JobModal, BankRegistrationModal
from selects import SelectRoles, SelectBankNames
from discord.ui import View

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

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
    
#     if message.content.startswith('!'):
#         await client.process_commands(message)
#         return

#     response = 'Welcome'
#     await message.channel.send(response)

@client.tree.command(name='login')
async def send_form(interaction: discord.Interaction):
    roles = [role.name for role in interaction.user.roles]

    print(roles)
    print('NO ROLE' in roles)
    print(f"Influencer: {'Influencer' in roles}")
    print(f'guild id: {interaction.guild.id}')
    print(f'guild name: {interaction.guild.name}')

    if 'Influencer' in roles:
        message = get_manual_link(interaction.user.id, interaction.user.name)
    else:
        message = 'You are not influencer'
    await interaction.response.send_message(message)

@client.tree.command()
async def job_add(interaction: discord.Interaction):
    roles = interaction.user.roles
    role_names = [role.name for role in roles]
    print(f'{role_names=}')
    # if 'Influencer' in role_names:
    #     message = 'You don\'t have permission'
    #     return await interaction.response.send_message(message)

    view = View()
    view.add_item(SelectRoles(roles=role_names))

    response = await interaction.response.send_message('Select roles', view=view)
    print(response)

@client.tree.command()
async def bank_registration(interaction: discord.Interaction):
    roles = interaction.user.roles
    role_names = [role.name for role in roles]

    print(f'roles: {roles}')
    if 'Influencer' not in role_names:
        message = 'You don\'t have permission'
        return await interaction.response.send_message(message)

    view = discord.ui.View()
    view.add_item(SelectBankNames())

    response = await interaction.response.send_message('Bank registration', view=view)
    print(response)

client.run(TOKEN)
# if __name__ == '__main__':