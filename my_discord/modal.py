from typing import List
from views import JobView, ReviewView
import discord, requests
from discord.ui import Modal, TextInput
from discord import Interaction
from utils.enums import Enums
from datetime import datetime, timedelta
from validator.validator import Validator
import re, os, pytz

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

    def validate(self, start_date_string, duration):
        validator = Validator()
        messages = []
        # timezone = pytz.timezone('Asia/Ulaanbaatar')

        date = datetime.now()
        today = datetime(date.year, date.month, date.day)
        if not validator.date_validator(start_date_string):
            messages.append('Start date is invalid')
        elif datetime.strptime(start_date_string, '%Y/%m/%d') < today:
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
            'server_name': interaction.guild.name,
            'name': str(self.name),
            'roles': str(','.join(self.roles)),
            'budget': int(self.budget),
            'start_date': str(self.start_date),
            'end_date': end_date,
            'participation_date': str(participation_date),
            'duration': int(str(self.duration)),
            'description': str(self.description),
            'upload_link': str(self.upload_link),
            'requirements': "str(self.requirements)",
            'type': 'Open',
            'user_count': '20'
        }

        response = requests.post(self.url + '/job', json=data)
        print(response.text)
        response = response.json()
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

class ReviewUserModal(Modal, title='Review upload'):
    def __init__(self, bot, user_id, job_register_id, job_data: dict, review_type, company=False):
        super().__init__(title='Review upload')
        self.bot = bot
        self.review_type = review_type
        self.user_id = user_id
        self.job_register_id = job_register_id
        self.job_data = job_data
        self.company = company
        self.link = TextInput(label="We transfer link", placeholder="https://we.tl/t-A6GJNEtest", required=True, min_length=1, max_length=200)
        self.description = TextInput(label="Description", placeholder='', required=True,  style=discord.TextStyle.paragraph)
        if not company:
            self.add_item(self.link)
        self.add_item(self.description)

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer()
        data = {
            'user_id': self.user_id,
            'discord_server_id': self.job_data['discord_server_id'],
            'job_register_id': self.job_register_id,
            'job_id': self.job_data['job_id'],
            'job_name': self.job_data['name'],
            'job_description': self.job_data['description'],
            'type': self.review_type,
            'description': str(self.description),
        }

        if not self.company:
            data['link'] = str(self.link)

        guild = discord.utils.get(self.bot.guilds, id=self.job_data['discord_server_id'])
        if not guild:
            return await interaction.response.send_message('Failed this company doesn\'t exists')
        data['server_id'] = self.job_data['discord_server_id']
        data['server_name'] = guild.name

        response = requests.post(URL + '/review', json=data)
        
        if response.json()['success']:
            data['id'] = response.json()['review_id']
            channel_name = Enums.REVIEW.value
            channel = discord.utils.get(guild.channels, name=channel_name)  # Replace 'general' with your channel name or ID
            view = ReviewView(data, self.bot, company=True)
            if channel:
                await channel.send(embed=view.embed, view=view)
        #     return await interaction.response.send_message('Successfully sent link to company')
        # else:
        #     return await interaction.response.send_message('Error has been accured please, try again')
                   
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
    def __init__(self, user_id, job_id, server_id, job_register_id, review_id, socials, bot):
        self.bot = bot
        self.user_id = user_id
        self.job_id = job_id
        self.server_id = server_id
        self.job_register_id = job_register_id
        self.review_id = review_id

        self.instagram = None
        self.facebook = None
        self.tiktok = None
        self.youtube = None

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
        from embeds import ContentEmbed
        from usecases.user_reviews import GetUserReviewById
        from usecases.get_content import GetContentById
        from views import ContentView
        await interaction.response.defer()

        print('debug1')

        data = {
            'user_id': self.user_id,
            'job_id': self.job_id,
            'server_id': self.server_id,
            'job_register_id': self.job_register_id,
            'review_id': self.review_id
        }

        socials = []
        types = []
        if self.instagram is not None and str(self.instagram) != '':
            types.append('instagram')
            socials.append(str(self.instagram))
        if self.facebook is not None and str(self.facebook) != '':
            types.append('facebook')
            socials.append(str(self.facebook))
        if self.tiktok is not None and str(self.tiktok) != '':
            types.append('tiktok')
            socials.append(str(self.tiktok))
        if self.youtube is not None and str(self.youtube) != '':
            types.append('youtube')
            socials.append(str(self.youtube))

        content_ids = []
        for i, social in enumerate(socials):
            data['type'] = types[i]
            data['link'] = social
            response = requests.post(URL + '/content', json=data)
            content_ids.append(response.json()['content_id'])

        message = f'<@{self.user_id}>: Social links succesfully uploaded {", ".join(socials)}'

        review_data = GetUserReviewById().execute(self.review_id, self.bot)
        for content_id in content_ids:    
            content_data = GetContentById().execute(content_id)
            view = ContentView(review_data, content_data, self.bot)
            await interaction.followup.send(message, embed=view.embed, view=view)

            guild = discord.utils.get(self.bot.guilds, id=self.server_id)
            channel_name =  Enums.CONTENT.value
            channel = discord.utils.get(guild.channels, name=channel_name)
            await channel.send(message, embed=view.embed, view=view)
        self.stop()

class ReviewRejectModal(Modal, title='Description'):
    def __init__(self):
        super().__init__()
        self.description = TextInput(label="Description", placeholder='Tell me why you rejected this', required=True,  style=discord.TextStyle.paragraph)
        self.add_item(self.description)

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer()
        return str(self.description)
    
    # async def wait_for_submit(self):
    #     await self._event.wait()  # Wait until the event is set
    #     return self._return_value