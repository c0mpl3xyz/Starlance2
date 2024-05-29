from typing import List
from views import JobView
import discord, requests
from discord.ui import Modal, TextInput
from discord import Interaction
from utils.enums import Enums
from datetime import datetime, timedelta
from validator.validator import Validator
import re, os

URL = os.getenv('URL')
# start_date, duration, end_date, modified_date, participation_date, job_delete_date, description, upload_file_links, requirements) -> bool:
class JobModal(Modal, title="Job registration"):
    def __init__(self, bot, roles, budget, url, name=None, start_date=None, duration=7, upload_link=None):
        self.bot = bot
        self.url = url
        self.roles = roles
        self.budget = budget
        self.name = TextInput(label="Job Name", placeholder="Your job name here", default=name, required=True)
        self.start_date = TextInput(label="Start Date", placeholder="YYYY/MM/DD", default=start_date, required=True)
        # TODO make it number
        self.duration = TextInput(label="Duration", placeholder="days", required=True, default=duration, style=discord.TextStyle.short)
        self.upload_link = TextInput(label="We Transfer Upload link", placeholder="We transfer link here", default=upload_link, required=True)
        self.description = TextInput(label="Description", placeholder='', required=True,  style=discord.TextStyle.paragraph)

        # self.requirements = TextInput(label="Requirements", placeholder='', required=True)
        # self.participation_date = TextInput(label="Participation Date", placeholder="YY/MM/DD", default=participation_date, required=True)

        super().__init__()
        self.add_item(self.name)
        self.add_item(self.start_date)
        self.add_item(self.duration)
        self.add_item(self.description)
        self.add_item(self.upload_link)
        # self.add_item(self.description)
        # self.add_item(self.requirements)

    # def validate(self, data, interaction):
    #     validator = Validator()
    #     if not validator.date_validator(self.start_date):
    #         pass

    def validate(self, start_date, duration):
        validator = Validator()
        messages = []
        if not validator.date_validator(start_date):
            messages.append('Start date is invalid')
        elif datetime.strptime(start_date, '%Y/%m/%d') < datetime.now():
            messages.append('Start date must be after today')

        if not duration.isdigit():
            messages.append('Duration must be numeric days')

        return messages
    
    async def on_submit(self, interaction: Interaction):
        valid_messages = self.validate(str(self.start_date), str(self.duration))
        if len(valid_messages) > 0:
            await interaction.response.send_message('Job registration failed')

            for message in valid_messages:
                await interaction.channel.send(message)
            return

        start_date = datetime.strptime(str(self.start_date), '%Y/%m/%d')
        end_date_obj: datetime =  start_date + timedelta(days=int(str(self.duration)))
        participation_date_obj = start_date + timedelta(days=7)
        end_date: str = end_date_obj.strftime('%Y/%m/%d')
        participation_date: str = participation_date_obj.strftime('%Y/%m/%d')
        data = {
            'discord_server_id': interaction.guild.id,
            'name': str(self.name),
            'roles': str(','.join(self.roles)),
            'budget': int(self.budget),
            'start_date': str(self.start_date),
            'end_date': end_date,
            'participation_date': str(participation_date),
            'duration': int(str(self.duration)),
            'description': str(self.description),
            'upload_link': str(self.upload_link),
            'requirements': "str(self.requirements)"
        }

        response = requests.post(self.url + '/job', json=data).json()
        print(response)
        if response and 'success' in response:
            success = ['success']
            data['job_id'] = response['job_id']

        # channel_name =  ChannelEnum.GUILD.value #TODO: CHANGE IT
        # channel = discord.utils.get(interaction.guild.channels, name=channel_name)
        # if channel:
        #     await channel.send(message)
        
        if success:
            job_view = JobView(data, self.bot)
            message = '\n'.join(f'{k}: {v}' for (k, v) in data.items())
            await interaction.response.send_message(message)
            await interaction.message.delete()

            # TODO: change user id to job registered users
            user = await self.bot.fetch_user(537848640140476436)
            guild = await self.bot.fetch_guild(data['discord_server_id'])
            if user and guild:
                data['company name'] = guild.name
                await user.send(embed=job_view.embed, view=job_view)
        else:
            await interaction.response.send_message(response['message'])
        return success

class JobAdditionalModal(Modal, title='Additional Information'):
    def __init__(self, url):
        self.url = url

        self.requirements = TextInput(label="Requirements", placeholder='', required=True)
        self.description = TextInput(label="Description", placeholder='', required=True)
        super().__init__()

        self.add_item(self.description)
        self.add_item(self.requirements)

    def on_submit(self, interaction: discord.Interaction):
        data = {
            'description': self.description,
            'requirements': self.requirements
        }

        requests.put(self.url + '/job', json=data).json()

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

class SocialRegisterModal(Modal, title='Social account link upload'):
    def __init__(self, user_id, job_id, socials, server_id, bot):
        self.user_id = user_id
        self.bot = bot
        self.job_id = job_id
        self.server_id = server_id

        super().__init__()
        if 'Instagram' in socials:
            self.instagram = TextInput(label="Instagram link", placeholder="https://www.instagram.com/reel/C7YasAEtest/", required=False, min_length=1, max_length=100)
            self.add_item(self.instagram)
        if 'Youtube' in socials:
            self.youtube = TextInput(label="Youtube link", placeholder="https://www.youtube.com/shorts/VsbIaKctest", required=False, min_length=1, max_length=100)
            self.add_item(self.youtube)
        if 'TikTok' in socials:
            self.tiktok = TextInput(label="TikTok link", placeholder="https://www.youtube.com/shorts/VsbIaKctest", required=False, min_length=1, max_length=100)
            self.add_item(self.tiktok)
        if 'Facebook' in socials:
            self.facebook = TextInput(label="Facebook link", placeholder="https://www.facebook.com/100010907134752/videos/42146212077test/", required=False, min_length=1, max_length=100)
            self.add_item(self.facebook)

    async def on_submit(self, interaction: Interaction):
        self.instagram = None
        self.facebook = None
        self.tiktok = None
        self.youtube = None
        success = False
        data = {
            'user_id': self.user_id,
            'job_id': self.job_id
        }

        socials = []
        if self.instagram is not None and str(self.instagram) != '':
            data['instagram'] = str(self.instagram)
            socials.append( str(self.instagram))
        if self.facebook is not None and str(self.facebook) != '':
            data['facebook'] = str(self.facebook)
            socials.append( str(self.facebook))
        if self.tiktok is not None and str(self.tiktok) != '':
            data['tiktok'] = str(self.tiktok)
            socials.append( str(self.tiktok))
        if self.youtube is not None and str(self.youtube) != '':
            data['youtube'] = str(self.youtube)
            socials.append( str(self.youtube))

        response = requests.put(URL + '/job_register/link', json=data)
        if response and 'success' in response.json():
            success = response.json()['success']

            if success:
                message = f'<@{self.user_id}>: Social links succesfully uploaded {", ".join(socials)}'

                guild = discord.utils.get(self.bot.guilds, id=self.server_id)
                channel_name =  Enums.NOTIFICATION.value
                channel = discord.utils.get(guild.channels, name=channel_name)
                await channel.send(message)
                await interaction.response.send_message(message)
            else:
                message = 'Social link upload failed, pease try again'
                await interaction.response.send_message(message)