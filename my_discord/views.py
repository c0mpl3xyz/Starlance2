from discord.ui import View
from embeds import JobEmbed, LoginEmbed
from usecases.register_job import RegisterJob
import discord, requests, os
from usecases.register_job import RegisterJob
from usecases.review import Review
from usecases.get_job_by_id import GetJobById, GetJobReportById
from usecases.user_reviews import GetUserReview, UpdateReview
from usecases.get_user import UpdateUserPoints
from embeds import ApproveEmbed, ReviewEmbed, UserEmbed, CollectEmbed
from utils.enums import Enums
import aiohttp, asyncio
from datetime import datetime
import time, uuid, aiofiles, pytz

URL = os.getenv('URL')

class LogInView(discord.ui.View):
    def __init__(self, user_id, user_name):
        from manual import get_manual_link
        link = get_manual_link(user_id, user_name)
        self.embed = LoginEmbed(user_name)
        super().__init__()
        self.login_button = discord.ui.Button(label="Log in with Facebook", style=discord.ButtonStyle.url, url=link)
        self.login_button.callback = self.login_button_callback
        self.add_item(self.login_button)

    async def login_button_callback(self, interaction: discord.Interaction):
        pass

    # async def on_timeout(self):
    #     self.clear_items()
    #     timeout_button = discord.ui.Button(label='Time-out!, Re-use BOT Command', style=discord.ButtonStyle.primary, emoji='⏳')
    #     timeout_button.disabled = True
    #     self.add_item(timeout_button)
    #     await self.message.edit(view=self)

class CollectView(discord.ui.View):
    def __init__(self, user_data, bot, collect_id, point_100, point_75, point_25, income, balance, points_minus):
        super().__init__()
        self.user_data = user_data
        self.collect_id = collect_id
        self.message = None
        self.bot = bot
        self.point_100 = point_100
        self.point_75 = point_75
        self.point_25= point_25
        self.income = income
        self.balance = balance
        self.points_minus = points_minus

        self.embed = CollectEmbed(user_data, point_100, point_75, point_25, income, balance, points_minus)

        self.collect_button = discord.ui.Button(label=f"Uprove Collect request", style=discord.ButtonStyle.green, emoji='✨')
        self.collect_button.callback = self.collect_button_callback
        self.add_item(self.collect_button)

    async def collect_button_callback(self, interaction: discord.Interaction):
        # await interaction.response.defer()
        from modal import CollectAckModal
        modal = CollectAckModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.finished:
            data = {
                'collect_id': self.collect_id,
                'user_id': self.user_data['user_id'],
                'points': self.points_minus
            }

            response = requests.delete(URL + '/collect', json=data).json()
            if response['success']:
                from embeds import CollectedMessageEmbed
                self.collect_button.label = 'Approved'
                self.collect_button.disabled = True
                await interaction.message.edit(view=self)
                guild = self.bot.get_guild(Enums.GUILD_ID.value)
                user = discord.utils.get(guild.members, id=self.user_data['user_id'])
                embed = CollectedMessageEmbed(self.points_minus, self.user_data['bank_name'], self.user_data['bank_number'])
                self.message = await user.send(f'Your points are collected', embed=embed, view=self)
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
        self.collectable_points = (user_data['points']) * 0.75 // 10000 * 10000
        collectable = self.collectable_points >= 20000
        
        self.collect_button = discord.ui.Button(label=f"Collect Points: {format(self.collectable_points, ',')}", style=discord.ButtonStyle.green, emoji='✨')
        self.collect_button.callback = self.collect_button_callback

        if not collectable:
            self.collect_button.label = f"Not enough points to collect: {format(self.collectable_points, ',')}"
            self.collect_button.disabled = True
        # else:
        #     # result: list = requests.get(URL + '/collect/user', json={'user_id': user_data['user_id']}).json()
        #     result = await self.get_collects(user_data['user_id'])
        #     if len(result):
        #         self.collect_button.label = 'Collect request is already sent'
        #         self.collect_button.disabled = True
        self.add_item(self.collect_button)

    async def setup(self):
        result = await self.get_collects(self.user_data['user_id'])
        if len(result):
            self.collect_button.label = 'Collect request is already sent'
            self.collect_button.disabled = True
        return self

    async def get_collects(self, user_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(URL + '/collect/user', json={'user_id': user_id}) as response:
                result = await response.json()
                return result

    async def collect_button_callback(self, interaction: discord.Interaction):
        from modal import UserCollectModal
        # await interaction.response.defer()
        modal = UserCollectModal(self.user_data, self.user_data['points'], self.bot)
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
    def __init__(self, job_data, bot, company=False, has_review=False, contents=None, server=False):
        if contents == None:
            contents = []
        self.message = None
        self.register_job = None
        timeout = 350
        self.job_data = job_data
        self.bot = bot
        self.company = company
        self.type = None
        self.embed = JobEmbed(job_data, contents, company)
        
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

        self.delete_button = discord.ui.Button(label='Delete', style=discord.ButtonStyle.red, emoji='✖')
        self.delete_button.callback = self.delete_button_callback

        self.report_button = discord.ui.Button(label='Report', style=discord.ButtonStyle.secondary, emoji='📄')
        self.report_button.callback = self.report_button_callback

        if server:
            self.add_item(self.delete_button)
            self.add_item(self.report_button)

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

    async def report_button_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        get_report = GetJobReportById()
        report = await get_report.execute(self.job_data['job_id'])

        if report:
            file_name = str(uuid.uuid1()) + '.docx'
            async with aiofiles.open(file_name, 'wb') as f:
                await f.write(report)
            
            self.timezone = pytz.timezone('Asia/Ulaanbaatar')
            date = datetime.now(self.timezone)
            date_str = date.strftime('%Y_%m_%d')
            download_file_name = f'{self.job_data["name"]}_report_{date_str}.docx'
            file = discord.File(file_name, filename=download_file_name)
            
            await interaction.followup.send(f'Job Report: {self.job_data["name"]}:', file=file)
            os.remove(file_name)
        else:
            await interaction.followup.send('Failed to fetch the job report.')

    async def reject_button_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        register_job = RegisterJob()
        response = register_job.register(interaction.user.id, self.job_data['job_id'], 'Rejected')
        if response['success']:
            await interaction.message.delete()
        self.stop()

    async def new_button_callback(self, interaction: discord.Interaction):
        from modal import ReviewUserModal
        saved_interaction = interaction
        modal = ReviewUserModal(self.bot, interaction.user.id, self.register_job, self.job_data, 'Pending', self.company)
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.finished:
            self.new_button.label = 'Review request sent'
            self.new_button.disabled = True
            await saved_interaction.message.edit(view=self)
            self.stop()

    async def review_button_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = {
            'user_id': interaction.user.id,
            'job_ids': [self.job_data['job_id']]
        }
        
        DICT = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(URL + '/review/not_approved_count', json=data) as asyc_response:
                DICT = await asyc_response.json()
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

    async def delete_button_callback(self, interaction: discord.Interaction):
        from modal import DeleteJobModal
        delete_modal = DeleteJobModal(self.job_data)
        await interaction.response.send_modal(delete_modal)
        await delete_modal.wait()
        if delete_modal.finished:
            self.clear_items()
            self.delete_button.disabled = True
            self.delete_button.label = 'Deleted'
            self.add_item(self.delete_button)
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
            guild_id = Enums.GUILD_ID.value
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
        saved_interaction = interaction
        modal = ReviewUserModal(self.bot, interaction.user.id, self.review_data, self.job_data, 'Pending', self.company, update=self.update)
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.finished:
            self.new_button.label = 'Review request sent'
            self.new_button.disabled = True
            await saved_interaction.message.edit(view=self)
            self.stop()

    async def review_button_callback(self, interaction: discord.Interaction):
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
        select = UploadLinkSelect(self.bot, self.review_data['user_id'], self.review_data['job_id'], self.review_data['server_id'], self.review_data['job_register_id'], self.review_data['id'])
        view.add_item(select)
        await interaction.followup.send('Select social accounts', view=view)

        self.upload_button.disabled = True
        self.upload_button.label = 'Used'
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
        select = UploadLinkSelect(self.bot, self.review_data['user_id'], self.review_data['job_id'], self.review_data['server_id'], self.review_data['job_register_id'], self.review_data['id'], content_data=self.content_data, edit=True)
        view.add_item(select)
        await interaction.followup.send('Select social accounts', view=view)

        self.edit_button.label = 'Used'
        self.edit_button.disabled = True
        await interaction.message.edit(view=self)

    async def on_timeout(self):
        self.clear_items()
        timeout_button = discord.ui.Button(label='Time-out!, Re-use BOT Command /my_contents', style=discord.ButtonStyle.primary, emoji='⏳')
        timeout_button.disabled = True
        self.add_item(timeout_button)
        if self.main:
            await self.message.edit(view=self)