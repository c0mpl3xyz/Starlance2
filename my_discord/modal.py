from typing import List
from views import JobView
import discord, requests
from discord.ui import Modal, TextInput, Select
from discord import Interaction, SelectOption
from utils.channel_enums import ChannelEnum
from datetime import datetime, timedelta
from utils.validator import Validator
import re

# start_date, duration, end_date, modified_date, participation_date, job_delete_date, description, upload_file_links, requirements) -> bool:
class JobModal(Modal, title="Job registration"):
    def __init__(self, bot, roles, url):
        self.bot = bot
        self.url = url
        self.roles = roles
        self.name = TextInput(label="Job Name", placeholder="Your job name here", required=True)
        self.start_date = TextInput(label="Start Date", placeholder="YYYY/MM/DD", required=True, style=discord.TextStyle.short)
        # TODO make it number
        self.duration = TextInput(label="Duration", placeholder="days", required=True, style=discord.TextStyle.short)
        self.participation_date = TextInput(label="Participation Date", placeholder="YY/MM/DD", required=True, style=discord.TextStyle.short)
        self.description = TextInput(label="Description", placeholder='', required=True, style=discord.TextStyle.short)
        self.requirements = TextInput(label="Requirements", placeholder='', required=True, style=discord.TextStyle.short)
        self.upload_link = TextInput(label="We Transfer Upload link", placeholder="We transfer link here", required=False, style=discord.TextStyle.short)

        super().__init__()
        self.add_item(self.name)
        self.add_item(self.start_date)
        self.add_item(self.duration)
        self.add_item(self.participation_date)
        # self.add_item(self.description)
        # self.add_item(self.requirements)
        self.add_item(self.upload_link)

    # def validate(self, data, interaction):
    #     validator = Validator()
    #     if not validator.date_validator(self.start_date):
    #         pass

    async def on_submit(self, interaction: Interaction):
        end_date_obj: datetime = datetime.strptime(str(self.start_date), '%Y/%m/%d') + timedelta(int(str(self.duration)))
        end_date: str = end_date_obj.strftime('%Y/%m/%d')
        print(f'start_date: {str(self.start_date)}')

        print(f'company id: {interaction.guild.id}')
        data = {
            'discord_server_id': interaction.guild.id,
            'name': str(self.name),
            'roles': str(','.join(self.roles)),
            'start_date': str(self.start_date),
            'end_date': end_date,
            'participation_date': str(self.participation_date),
            'duration': int(str(self.duration)),
            'description': str(self.description),
            'upload_link': str(self.upload_link),
            'requirements': str(self.requirements)
        }

        print(f'roles {str(",".join(self.roles))}')

        response = requests.post(self.url + '/job', json=data)
        print(f'response {response.json()}')
        if response and 'success' in response.json():
            success = response.json()['success']

        # channel_name =  ChannelEnum.GUILD.value #TODO: CHANGE IT
        # channel = discord.utils.get(interaction.guild.channels, name=channel_name)
        # if channel:
        #     await channel.send(message)
        
        if success:
            message = '\n'.join(f'{k}: {v}' for (k, v) in data.items())
            await interaction.response.send_message(message)
            await interaction.message.delete()

            # change user id to job registered users
            user = await self.bot.fetch_user(537848640140476436)
            guild = await self.bot.fetch_guild(data['discord_server_id'])
            if user and guild:
                print('user found')
                data['company name'] = guild.name
                job_view = JobView(data)
                await user.send(job_view.description, view=job_view)
        else:
            message = 'Job registration failed'
            await interaction.response.send_message(message)
        return success

class BankRegistrationModal(Modal, title='Bank Registration'):
    def __init__(self, bank_name, url):
        self.url = url
        self.bank_name = bank_name
        self.bank_number = TextInput(label="Bank number", placeholder="Your bank number", required=True, min_length=1, max_length=100)
        self.register = TextInput(label="Register", placeholder="Your register", required=True, min_length=1, max_length=100)

        super().__init__()
        self.add_item(self.bank_number)
        self.add_item(self.register)

    async def on_submit(self, interaction: Interaction):
        success = False
        message: str = ''

        data = {
            'user_id': interaction.user.id,
            'bank_name': str(self.bank_name.replace('Bank', '').strip()),
            'bank_number': str(self.bank_number),
            'register': str(self.register)
        }

        response = requests.post(self.url + '/user/bank_register', json=data)
        if response and 'success' in response.json():
            success = response.json()['success']

        # channel_name =  ChannelEnum.GUILD.value #TODO: CHANGE IT
        # channel = discord.utils.get(interaction.guild.channels, name=channel_name)
        if success:
            message = f'Bank Registration\nUser: {interaction.user.global_name}\nBank name: {self.bank_name}\nBank number: {self.bank_number}\nRegister: {self.register}'
            await interaction.response.send_message(message)
            await interaction.message.delete()
            # if channel:
            #     await channel.send(message)
        else:
            message = 'Bank registration failed'
            await interaction.response.send_message(message)