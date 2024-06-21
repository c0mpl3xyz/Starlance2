from discord.ui import View
from embeds import JobEmbed, LoginEmbed
from usecases.register_job import RegisterJob
import discord, requests, os
from usecases.register_job import RegisterJob
from usecases.review import Review
from usecases.get_job_by_id import GetJobById
from usecases.user_reviews import GetUserReview, UpdateReview
from usecases.user_status import UpdateUserPoints
from embeds import ApproveEmbed, ReviewEmbed, UserEmbed, CollectEmbed
from utils.enums import Enums
import time

URL = os.getenv('URL')

class LogInView(discord.ui.View):
    def __init__(self, guild_id, guild_name):
        from manual import get_manual_link
        link = get_manual_link(guild_id, guild_name)
        self.embed = LoginEmbed(guild_name)
        super().__init__()
        self.login_button = discord.ui.Button(label="Log in with Facebook", style=discord.ButtonStyle.url, url=link)
        self.login_button.callback = self.login_button_callback
        self.add_item(self.login_button)

    async def login_button_callback(self, interaction: discord.Interaction):
        pass

    async def on_timeout(self):
        self.clear_items()
        timeout_button = discord.ui.Button(label='Time-out!, Re-use BOT Command', style=discord.ButtonStyle.primary, emoji='⏳')
        timeout_button.disabled = True
        self.add_item(timeout_button)
        await self.message.edit(view=self)

class CollectView(discord.ui.View):
    def __init__(self, user_data, bot, collect_id, points):
        super().__init__()
        self.user_data = user_data
        self.collect_id = collect_id
        self.message = None
        self.bot = bot
        self.points = points
        self.embed = CollectEmbed(user_data, points)

        self.collect_button = discord.ui.Button(label=f"Uprove Collect request", style=discord.ButtonStyle.green, emoji='✨')
        self.collect_button.callback = self.collect_button_callback
        self.add_item(self.collect_button)

    async def collect_button_callback(self, interaction: discord.Interaction):
        # collected = UpdateUserPoints().execute(self.user_data['user_id'], self.points)
        await interaction.response.defer()

        data = {
            'collect_id': self.collect_id,
            'user_id': self.user_data['user_id'],
            'points': self.points
        }

        response = requests.put(URL + '/collect', json=data).json()
        if response['success']:
            self.collect_button.label = 'Approved'
            self.collect_button.disabled = True
            await interaction.message.edit(view=self)
            guild = self.bot.get_guild(Enums.GUILD_ID.value)
            user = discord.utils.get(guild.members, id=self.user_data['user_id'])
            self.message = await user.send('Your points are collected', view=self)
        else:
            self.collect_button.label = 'Already approved'
            self.collect_button.disabled = True
            self.message = await interaction.message.edit(embed=self.embed, view=self)
        
        self.stop()
    
    async def on_timeout(self):
        self.clear_items()
        timeout_button = discord.ui.Button(label='Time-out!, Re-use BOT Command /my_status', style=discord.ButtonStyle.primary, emoji='⏳')
        timeout_button.disabled = True
        self.add_item(timeout_button)
        await self.message.edit(view=self)

class UserView(discord.ui.View):
    def __init__(self, user_data, bot):
        self.user_data = user_data
        self.message = None
        self.bot = bot
        self.embed = UserEmbed(user_data)
        super().__init__()
        collectable_points = user_data['points'] - 2000
        collectable = collectable_points > 0 #TODO: add threshold
        
        self.collect_button = discord.ui.Button(label=f"Collect Points: {user_data['points']}", style=discord.ButtonStyle.green, emoji='✨')
        self.collect_button.callback = self.collect_button_callback

        if not collectable:
            self.collect_button.label = f'No enough points to collect: {user_data["points"]}'
            self.collect_button.disabled = True
        else:
            result: list = requests.get(URL + '/collect/user', json={'user_id': user_data['user_id']}).json()
            if len(result):
                self.collect_button.label = 'Collect request is already sent'
                self.collect_button.disabled = True
        self.add_item(self.collect_button)

    async def collect_button_callback(self, interaction: discord.Interaction):
        from modal import UserCollectModal
        # await interaction.response.defer()
        modal = UserCollectModal(self.user_data, self.bot)
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.requested:
            self.collect_button.label = 'Collect request already sent'
            self.collect_button.disabled = True
            await interaction.message.edit(view=self)
            self.stop()
            return

        if modal.valid:
            self.collect_button.label = 'Collect request sent'
            self.collect_button.disabled = True
            await interaction.message.edit(view=self)
            self.stop()

    async def on_timeout(self):
        self.clear_items()
        timeout_button = discord.ui.Button(label='Time-out!, Re-use BOT Command /my_status', style=discord.ButtonStyle.primary, emoji='⏳')
        timeout_button.disabled = True
        self.add_item(timeout_button)
        await self.message.edit(view=self)

class JobView(discord.ui.View):
    def __init__(self, job_data, bot, company=False, has_review=False, contents=[]):
        self.message = None
        self.register_job = None
        timeout = 350
        self.job_data = job_data
        self.bot = bot
        self.company = company
        self.type = None
        self.embed = JobEmbed(job_data, contents)
        if 'type' in job_data:
            self.type = job_data['type']
        else:
            self.type = 'Open'

        super().__init__(timeout=timeout)
        self.description = '\n'.join([f'{k}: {v}' for (k, v) in job_data.items() if k != 'discord_server_id'])
        
        self.reject_button = discord.ui.Button(label="Reject", style=discord.ButtonStyle.danger, emoji='✖')
        self.reject_button.callback = self.reject_button_callback
        
        self.accept_button = discord.ui.Button(label="Accept", style=discord.ButtonStyle.green, emoji='✔')
        self.accept_button.callback = self.accept_button_callback

        self.pending_button = discord.ui.Button(label="Pending", style=discord.ButtonStyle.primary)
        self.pending_button.disabled = True

        self.review_button = discord.ui.Button(label='Content Review Add', style=discord.ButtonStyle.green, emoji='👀')
        self.review_button.callback = self.review_button_callback

        self.new_button = discord.ui.Button(label='Click here', style=discord.ButtonStyle.green, emoji='➕')
        self.new_button.callback = self.new_button_callback

        if not company:
            if self.type == 'Open':
                self.add_item(self.reject_button)
                self.add_item(self.accept_button)
            
            elif self.type == 'Pending':
                self.add_item(self.pending_button)
            
            elif self.type == 'Rejected':
                self.reject_button.label = 'Rejected'
                self.reject_button.disabled = True
                self.add_item(self.reject_button)
            
            elif self.type == 'Approved':
                self.accept_button.label = 'Approved'
                self.accept_button.style = discord.ButtonStyle.primary
                self.accept_button.disabled = True

                self.add_item(self.accept_button)

                if has_review:
                    self.review_button.label = "Review request sent"
                    self.review_button.disabled = True
                self.add_item(self.review_button)

    async def reject_button_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        register_job = RegisterJob()
        response = register_job.register(interaction.user.id, self.job_data['job_id'], 'Rejected')
        if response['success']:
            await interaction.message.delete()
        self.stop()

    async def new_button_callback(self, interaction: discord.Interaction):
        from modal import ReviewUserModal
        modal = ReviewUserModal(self.bot, interaction.user.id, self.register_job, self.job_data, 'Pending', self.company)
        await interaction.response.send_modal(modal)
        await modal.wait()

        self.new_button.label = 'Review request sent'
        self.new_button.disabled = True
        await interaction.message.edit(view=self)
        self.stop()

    async def review_button_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = {
            'user_id': interaction.user.id,
            'job_ids': [self.job_data['job_id']]
        }

        DICT = {}
        response = requests.get(URL + '/review/not_approved_count', json=data)

        if response:
            DICT = response.json()

        if str(self.job_data['job_id']) in DICT.keys():
            self.review_button.label = 'Review request is already sent'
            self.review_button.disabled = True
            await interaction.message.edit(view=self)
        else:
            register_job = RegisterJob().get_by_user_job(interaction.user.id, self.job_data['job_id'])
            register_job['job_register_id'] = register_job['id']
            self.register_job = register_job
            self.add_item(self.new_button)
            self.review_button.disabled = True
            await interaction.message.edit(view=self)

    async def accept_button_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        register_job = RegisterJob()
        response = register_job.register(interaction.user.id, self.job_data['job_id'], 'Pending')

        if response['success']:
            self.remove_item(self.reject_button)
            self.remove_item(self.accept_button)
            self.add_item(self.pending_button)

            guild_id = Enums.GUILD_ID.value
            guild = self.bot.get_guild(guild_id)
            user = discord.utils.get(guild.members, id=interaction.user.id)

            embed_data = {
                'user_id': interaction.user.id,
                'server_id': self.job_data['discord_server_id'],
                'job_id': self.job_data['job_id'],
                'user_roles': [role.name for role in user.roles],
                'job_name': self.job_data['name'],
                'job_roles': self.job_data['roles'],
                'start_date': self.job_data['start_date'],
                'description': self.job_data['description'],
                'type': 'Pending'
            }

            self.job_data['type'] = 'Approved'            
            job_approve_view = ApprovementJobView(embed_data, self.job_data, self.bot)
            guild_id = Enums.OUR_COMPANY.value
            guild = self.bot.get_guild(guild_id)
            # guild = discord.utils.get(self.bot.guilds, id=self.job_data['discord_server_id'])
            channel_name =  Enums.APPROVE_GUILD.value
            channel = discord.utils.get(guild.channels, name=channel_name)
            job_approve_view.message = await channel.send(embed=job_approve_view.embed, view=job_approve_view)
            await interaction.message.edit(view=self)
        else:
            await interaction.message.edit('failed')
        
        self.stop()

    async def on_timeout(self):
        self.clear_items()
        timeout_button = discord.ui.Button(label='Time-out!, Re-use BOT Command /my_new_jobs or /my_jobs', style=discord.ButtonStyle.primary, emoji='⏳')
        timeout_button.disabled = True
        self.add_item(timeout_button)
        await self.message.edit(view=self)

class ApprovementJobView(discord.ui.View):
    def __init__(self, embed_data, job_data, bot):
        self.job_data = job_data
        self.message = None
        timeout = 350
        self.bot = bot
        self.message = embed_data['description']
        self.embed = ApproveEmbed(embed_data)
        super().__init__(timeout=timeout)
        self.user_id = embed_data['user_id']

        self.server_id = embed_data['server_id']
        self.job_id = embed_data['job_id']
        self.reject_button = discord.ui.Button(label="Reject", style=discord.ButtonStyle.danger, custom_id='reject', emoji='✖')
        self.reject_button.callback = self.reject_button_callback
    
        self.accept_button = discord.ui.Button(label="Accept", style=discord.ButtonStyle.green, custom_id='accept', emoji='✔')
        self.accept_button.callback = self.accept_button_callback

        self.approve_button = discord.ui.Button(label="Approved", style=discord.ButtonStyle.primary, custom_id='approve')
        self.approve_button.disabled = True

        if 'type' not in embed_data or embed_data['type'] is None or embed_data['type'] == 'Pending':
            self.add_item(self.reject_button)
            self.add_item(self.accept_button)

        elif embed_data['type'] == 'Approved':
            self.add_item(self.approve_button)

    async def reject_button_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        register_job = RegisterJob()
        response = register_job.update(self.user_id, self.job_id, 'Rejected')
        guild_id = Enums.GUILD_ID.value
        guild = self.bot.get_guild(guild_id)
        user = discord.utils.get(guild.members, id=self.user_id)  # Fetch the user by ID

        if response['success']:
            self.remove_item(self.accept_button)
            await interaction.message.delete()
            await user.send(f'{self.job_data["name"]} uploaded link was Rejected, please check command: `/my_reviews`')
        

    async def accept_button_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        register_job = RegisterJob()
        response = register_job.update(self.user_id, self.job_id, 'Approved')
        if response['success']:
            self.remove_item(self.reject_button)
            self.remove_item(self.accept_button)
            self.add_item(self.approve_button)

            guild_id = Enums.GUILD_ID.value
            guild = self.bot.get_guild(guild_id)
            user = discord.utils.get(guild.members, id=self.user_id)

            self.job_data['type'] = 'Approved'
            job_view = JobView(self.job_data, self.bot)
            await interaction.message.edit(view=self)

            job_view.message = await user.send(embed=job_view.embed, view=job_view)
        else:
            await interaction.followup.send_message(response['message'])

    async def on_timeout(self):
        self.clear_items()
        timeout_button = discord.ui.Button(label='Time-out!, Re-use BOT Command /my_approves', style=discord.ButtonStyle.primary, emoji='⏳')
        timeout_button.disabled = True
        self.add_item(timeout_button)
        await self.message.edit(view=self)

class ReviewView(discord.ui.View):
    def __init__(self, review_data, bot, company=False):
        self.review_data = review_data
        self.message = None
        timeout = 350
        self.bot = bot
        self.company = company
        self.embed = ReviewEmbed(review_data)

        super().__init__(timeout=timeout)
        self.reject_button = discord.ui.Button(label="Reject", style=discord.ButtonStyle.danger, emoji='✖')
        self.reject_button.callback = self.reject_button_callback
    
        self.accept_button = discord.ui.Button(label="Accept", style=discord.ButtonStyle.green, emoji='✔')
        self.accept_button.callback = self.accept_button_callback

        self.review_button = discord.ui.Button(label="Review", style=discord.ButtonStyle.green, emoji='👀')
        self.review_button.callback = self.review_button_callback

        self.new_button = discord.ui.Button(label="Click me", style=discord.ButtonStyle.green, emoji='➕')
        self.new_button.callback = self.new_button_callback

        self.approve_button = discord.ui.Button(label="Approved", style=discord.ButtonStyle.primary)
        self.approve_button.disabled = True

        self.upload_button = discord.ui.Button(label="Upload", style=discord.ButtonStyle.green, emoji='➕')
        self.upload_button.callback = self.upload_button_callback

        self.pending_button = discord.ui.Button(label="Pending", style=discord.ButtonStyle.primary)
        self.pending_button.disabled = True

        self.register_job = None
        self.update = False
        self.job_data = None
        if company:
            if review_data['type'] == 'Pending':
                self.add_item(self.reject_button)
                self.add_item(self.accept_button)

            elif review_data['type'] == 'Approved':
                self.add_item(self.approve_button)
                self.add_item(self.upload_button)

        else:
            if review_data['type'] == 'Pending':
                self.add_item(self.pending_button)

            elif review_data['type'] == 'Approved':
                self.review_button.label = 'Reviewed'
                self.review_button.disabled = True
                self.add_item(self.approve_button)
                # self.add_item(self.review_button)

            elif review_data['type'] == 'Rejected':
                self.reject_button.disabled = True
                self.add_item(self.reject_button)
                self.add_item(self.review_button)

    async def new_button_callback(self, interaction: discord.Interaction):
        from modal import ReviewUserModal
        modal = ReviewUserModal(self.bot, interaction.user.id, self.review_data, self.job_data, 'Pending', self.company, update=self.update)
        await interaction.response.send_modal(modal)
        await modal.wait()

        self.new_button.label = 'Review request sent'
        self.new_button.disabled = True
        await interaction.message.edit(view=self)
        self.stop()

    async def review_button_callback(self, interaction: discord.Interaction):
        from modal import ReviewUserModal
        await interaction.response.defer()
        job_data = GetJobById(self.review_data['job_id']).execute()
        update = False
        if 'type' in self.review_data and self.review_data['type'] == 'Rejected':
            update = True
        self.review_button.label = 'Review request sent'
        self.review_button.disabled = True
        self.update = update
        self.job_data = job_data
        self.add_item(self.new_button)
        await interaction.message.edit(view=self)
        
    async def reject_button_callback(self, interaction: discord.Interaction):
        from modal import ReviewRejectModal
        # interaction.response.defer()
        review = Review() 
        
        response = review.update(self.review_data['id'], link=self.review_data['link'], review_type='Rejected', descripton=self.review_data['description'])
        if response['success']:
            self.review_data['type'] = 'Rejected'
            modal = ReviewRejectModal()
            await interaction.response.send_modal(modal)
            await modal.wait()
            self.review_data['description'] = modal.description.value

            self.remove_item(self.accept_button)
            self.reject_button.label = 'Rejected'
            self.reject_button.disabled = True
            await interaction.message.edit(view=self)
            
            UpdateReview().execute(self.review_data)
            user = await self.bot.fetch_user(self.review_data['user_id'])
            view = ReviewView(self.review_data, self.bot)
            view.message = await user.send(embed=view.embed, view=view)
        else: 
            await interaction.followup.send_message('Failed to execute this command please try again')
        

    async def upload_button_callback(self, interaction: discord.Interaction):
        from selects import UploadLinkSelect
        await interaction.response.defer()
        view = View()
        view.add_item(UploadLinkSelect(self.bot, self.review_data['user_id'], self.review_data['job_id'], self.review_data['server_id'], self.review_data['job_register_id'], self.review_data['id']))
        await interaction.followup.send('Select social accounts', view=view)
        self.upload_button.disabled = True
        self.upload_button.label = 'Uploaded'
        await interaction.message.edit(view=self)
        

    async def accept_button_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        review = Review()
        response = review.update(self.review_data['id'], review_type='Approved')

        if response['success']:
            self.remove_item(self.reject_button)
            self.remove_item(self.accept_button)
            self.add_item(self.approve_button)
            self.add_item(self.upload_button)

            self.review_data['type'] = 'Approved'

            await interaction.message.edit(view=self)
            user = await self.bot.fetch_user(self.review_data['user_id'])
            view= ReviewView(self.review_data, self.bot)
            view.message = await user.send(embed=view.embed, view=view)

    async def on_timeout(self):
        self.clear_items()
        timeout_button = discord.ui.Button(label='Time-out!, Re-use BOT Command /my_reviews', style=discord.ButtonStyle.primary, emoji='⏳')
        timeout_button.disabled = True
        self.add_item(timeout_button)
        await self.message.edit(view=self)

class ContentView(discord.ui.View):
    def __init__(self, review_data, content_data, bot, main=False):
        from embeds import ContentEmbed
        self.main = main
        self.message = None
        self.review_data = review_data
        self.content_data = content_data
        timeout = 250
        self.bot = bot
        self.embed = ContentEmbed(review_data, content_data)

        super().__init__(timeout=timeout)
        self.edit_button = discord.ui.Button(label="Edit", style=discord.ButtonStyle.secondary, emoji='✔')
        self.edit_button.callback = self.edit_button_callback

        if main:
            self.add_item(self.edit_button)

    async def edit_button_callback(self, interaction: discord.Interaction):
        from selects import UploadLinkSelect
        await interaction.response.defer()
        view = View()
        view.add_item(UploadLinkSelect(self.bot, self.review_data['user_id'], self.review_data['job_id'], self.review_data['server_id'], self.review_data['job_register_id'], self.review_data['id'], edit=True))
        await interaction.followup.send('Select social accounts', view=view)

        self.edit_button.lable = 'Link was beed updated'
        self.edit_button.disables = True
        await interaction.message.edit(view=self)

    async def on_timeout(self):
        self.clear_items()
        timeout_button = discord.ui.Button(label='Time-out!, Re-use BOT Command /my_contents', style=discord.ButtonStyle.primary, emoji='⏳')
        timeout_button.disabled = True
        self.add_item(timeout_button)
        if self.main:
            await self.message.edit(view=self)