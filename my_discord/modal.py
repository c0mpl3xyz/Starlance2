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
        await interaction.response.defer()
        valid_messages = self.validate(str(self.start_date), str(self.duration))
        if len(valid_messages) > 0:
            await interaction.followup.send('Job registration failed')

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
            'requirements': "",
            'type': 'Open',
            'user_count': '20'
        }

        response = requests.post(self.url + '/job', json=data)
        response = response.json()
        if response and 'success' in response:
            success = ['success']
            data['job_id'] = response['job_id']

        # channel_name =  ChannelEnum.GUILD.value #TODO: CHANGE IT
        # channel = discord.utils.get(interaction.guild.channels, name=channel_name)
        # if channel:
        #     await channel.send(message)
        
        if success:
            user_job_view = JobView(data, self.bot)
            company_job_view = JobView(data, self.bot, company=True)
            company_job_view.message = await interaction.followup.send('New Job added', embed=company_job_view.embed, view=company_job_view)
            await interaction.message.delete()

            # TODO: change user id to job registered users
            guild = self.bot.get_guild(Enums.GUILD_ID.value)

            job_roles = set(self.roles)
            for user in guild.members:

                user_roles = set([role.name for role in user.roles])
                intersection_set = user_roles & job_roles

                if isinstance(user, discord.User) or isinstance(user, discord.Member):
                    if list(intersection_set):
                        dm_channel = user.dm_channel
                        if not dm_channel:
                            dm_channel = await user.create_dm()
                        user_job_view.message = await dm_channel.send(embed=user_job_view.embed, view=user_job_view)
                    else:
                        await interaction.followup.send(response['message'])
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

        guild_id = Enums.GUILD_ID.value
        guild = self.bot.get_guild(guild_id)
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
                view.message = await channel.send(embed=view.embed, view=view)
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
    def __init__(self, user_id, job_id, server_id, job_register_id, review_id, socials, bot, edit):
        self.bot = bot
        self.user_id = user_id
        self.job_id = job_id
        self.server_id = server_id
        self.job_register_id = job_register_id
        self.review_id = review_id
        self.edit = edit

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
            response = None
            if self.edit:
                response = requests.put(URL + '/content/link_by_review', json=data)
            else:
                response = requests.post(URL + '/content', json=data)
            content_ids.append(response.json()['content_id'])

        message = f'<@{self.user_id}>: Social links succesfully uploaded {", ".join(socials)}'

        review_data = GetUserReviewById().execute(self.review_id, self.bot)
        for content_id in content_ids:
            content_data = GetContentById().execute(content_id)
            view = ContentView(review_data, content_data, self.bot)
            view_main = ContentView(review_data, content_data, self.bot, main=True)
            
            #await interaction.followup.send(message, embed=view.embed, view=view)
            guild = self.bot.get_guild(Enums.GUILD_ID.value)
            channel = discord.utils.get(guild.channels, name=Enums.CONTENT.value)
            view_main.message = await channel.send(message, embed=view_main.embed, view=view_main)

            guild_company = self.bot.get_guild(int(data['server_id']))
            channel_company = discord.utils.get(guild_company.channels, name=Enums.CONTENT.value)
            view.message = await channel_company.send(message, embed=view.embed, view=view)
        self.stop()

class ReviewRejectModal(Modal, title='Description'):
    def __init__(self):
        super().__init__()
        self.description = TextInput(label="Description", placeholder='Tell me why you rejected this', required=True,  style=discord.TextStyle.paragraph)
        self.add_item(self.description)

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer()
        return str(self.description)

class UserCollectModal(Modal, title='Collect User Points'):
    def __init__(self, user_data, bot):
        super().__init__()
        self.requested = False
        self.user_data = user_data
        self.bot = bot
        self.valid = False
        self.points = TextInput(label="Points to collect", placeholder='Input your points to collect', required=True, style=discord.TextStyle.short)
        self.add_item(self.points)

    def validate(self, user_points: int, points: str):
        messages = []
        if not points.isnumeric():
            messages.append(f'You entered this {points}. And this is not a valid number')
        if points.isnumeric() and int(points) > user_points:
            messages.append(f'Your availabled Points: {user_points}, You can\'t collect more than this!')
        return messages

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer()
        from views import CollectView
        points = str(self.points)
        messages = self.validate(self.user_data['points'], points)
        if len(messages):
            await interaction.followup.send('User collect points failed')
            for message in messages:
                await interaction.channel.send(message)
        else:
            self.valid = True
            data = {
                'user_id': self.user_data['user_id'],
                'points': int(points)
            }

            response = requests.post(URL + '/collect', json=data)
            response = response.json()
            print(f'collect id: {response}')
            if response['success']:
                collect_id = response['collect_id']
                print(f'{collect_id=}')
                guild = self.bot.get_guild(Enums.GUILD_ID.value)
                channel = discord.utils.get(guild.channels, name=Enums.COLLECT.value)            
                collect_view = CollectView(self.user_data, self.bot, collect_id, int(points))
                collect_view.message = await channel.send(embed=collect_view.embed, view=collect_view)
            else:
                self.requested = True
    
    # async def wait_for_submit(self):
    #     await self._event.wait()  # Wait until the event is set
    #     return self._return_value