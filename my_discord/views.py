from discord.ui import View
from embeds import JobEmbed
from usecases.register_job import RegisterJob
import discord
import requests
from usecases.register_job import RegisterJob
from usecases.review import Review
from usecases.get_job_by_id import GetJobById
from usecases.user_reviews import GetUserReview, CreateUserReview
from embeds import ApproveEmbed, ReviewEmbed
from utils.enums import Enums

class JobView(discord.ui.View):
    def __init__(self, job_data, bot, company=False):
        self.job_data = job_data
        self.bot = bot
        self.company = company
        self.embed = JobEmbed(job_data)
        if 'type' in job_data:
            self.type = job_data['type']

        super().__init__(timeout=350)
        self.description = '\n'.join([f'{k}: {v}' for (k, v) in job_data.items() if k != 'discord_server_id'])
        
        self.reject_button = discord.ui.Button(label="Reject", style=discord.ButtonStyle.danger, emoji='✖')
        self.reject_button.callback = self.reject_button_callback
        
        self.accept_button = discord.ui.Button(label="Accept", style=discord.ButtonStyle.green, emoji='✔')
        self.accept_button.callback = self.accept_button_callback

        self.pending_button = discord.ui.Button(label="Pending", style=discord.ButtonStyle.primary)
        self.pending_button.disabled = True

        self.review_button = discord.ui.Button(label='add Review', style=discord.ButtonStyle.green, emoji='➕')
        self.review_button.callback = self.review_button_callback

        if not company:
            if job_data['type'] == 'Open':
                self.add_item(self.reject_button)
                self.add_item(self.accept_button)
            
            elif job_data['type'] == 'Pending':
                self.add_item(self.pending_button)
            
            elif job_data['type'] == 'Rejected':
                self.reject_button.label = 'Rejected'
                self.reject_button.disabled = True
                self.add_item(self.reject_button)
            
            elif job_data['type'] == 'Approved':
                self.accept_button.label = 'Approved'
                self.accept_button.style = discord.ButtonStyle.primary
                self.accept_button.disabled = True

                self.add_item(self.accept_button)
                self.add_item(self.review_button)

    async def reject_button_callback(self, interaction: discord.Interaction):
        register_job = RegisterJob()
        response = register_job.register(interaction.user.id, self.job_data['job_id'], 'Rejected')
        if response['success']:
            await interaction.message.delete()
        self.stop()

    async def review_button_callback(self, interaction: discord.Interaction):
        from modal import ReviewUserModal

        register_job = RegisterJob().get_by_user_job(interaction.user.id, self.job_data['job_id'])
        server_id = self.job_data['discord_server_id']

        print(f'{server_id=}')

        await interaction.response.send_modal(ReviewUserModal(self.bot, interaction.user.id, register_job['id'], self.job_data, 'Pending', self.company))
        print(register_job)
        self.review_button.label = 'Review request sent'
        self.review_button.disabled = True
        await interaction.message.edit(view=self)
        self.stop()

    async def accept_button_callback(self, interaction: discord.Interaction):
        register_job = RegisterJob()
        response = register_job.register(interaction.user.id, self.job_data['job_id'], 'Pending')

        if response['success']:
            self.remove_item(self.reject_button)
            self.remove_item(self.accept_button)
            self.add_item(self.pending_button)
            embed_data = {
                'user_id': interaction.user.id,
                'job_id': self.job_data['job_id'],
                'user_name': interaction.user.name,
                # 'user_roles': interaction.user.roles,
                'job_name': self.job_data['name'],
                'job_roles': self.job_data['roles'],
                'start_date': self.job_data['start_date'],
                'description': self.job_data['description'],
                'type': 'Pending'
            }

            self.job_data['type'] = 'Approved'            
            job_approve_view = ApprovementJobView(embed_data, self.job_data, self.bot)
            guild = discord.utils.get(self.bot.guilds, id=self.job_data['discord_server_id'])
            channel_name =  Enums.APPROVE_GUILD.value
            channel = discord.utils.get(guild.channels, name=channel_name)
            await channel.send(embed=job_approve_view.embed, view=job_approve_view)
            await interaction.response.edit_message(view=self)
        else:
            await interaction.response.send_message(response['message'])
        self.stop()

class ApprovementJobView(discord.ui.View):
    def __init__(self, embed_data, job_data, bot):
        self.job_data = job_data
        self.bot = bot
        self.embed = ApproveEmbed(embed_data)
        super().__init__(timeout=350)
        self.user_id = embed_data['user_id']
        self.server_id = embed_data['job_id']
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

    #TODO: add rejected message to influencer
    async def reject_button_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        register_job = RegisterJob()
        print(f'user id: {self.user_id}')
        response = register_job.update(self.user_id, self.server_id, 'Rejected')
        guild_id = Enums.GUILD_ID.value
        guild = self.bot.get_guild(guild_id)
        user = discord.utils.get(guild.members, id=self.user_id)  # Fetch the user by ID

        if response['success']:
            self.remove_item(self.accept_button)
            await interaction.message.delete()
            await user.send(f'{self.job_data.name} uploaded link was Rejected, please check command: `/my_reviews`')
        self.stop()

    async def accept_button_callback(self, interaction: discord.Interaction):
        register_job = RegisterJob()
        response = register_job.update(self.user_id, self.server_id, 'Approved')

        print(f'{response=}')
        if response['success']:
            self.remove_item(self.reject_button)
            self.remove_item(self.accept_button)
            self.add_item(self.approve_button)

            guild_id = Enums.GUILD_ID.value  # The guild (server) where the command was called
            guild = self.bot.get_guild(guild_id)
            user = discord.utils.get(guild.members, id=self.user_id)  # Fetch the user by ID

            job_view = JobView(self.job_data, self.bot)
            await interaction.response.edit_message(view=self)

            
            await user.send(embed=job_view.embed, view=job_view)
        else:
            await interaction.response.send_message(response['message'])
        self.stop()

class ReviewView(discord.ui.View):
    def __init__(self, review_data, bot, company=False):
        self.review_data = review_data
        self.bot = bot
        self.embed = ReviewEmbed(review_data)

        super().__init__(timeout=350)
        self.reject_button = discord.ui.Button(label="Reject", style=discord.ButtonStyle.danger, custom_id='reject', emoji='✖')
        self.reject_button.callback = self.reject_button_callback
    
        self.accept_button = discord.ui.Button(label="Accept", style=discord.ButtonStyle.green, custom_id='accept', emoji='✔')
        self.accept_button.callback = self.accept_button_callback

        self.upload_button = discord.ui.Button(label="Upload", style=discord.ButtonStyle.green, custom_id='upload', emoji='➕')
        self.upload_button.callback = self.upload_button_callback

        self.approve_button = discord.ui.Button(label="Approved", style=discord.ButtonStyle.primary, custom_id='approve')
        self.approve_button.disabled = True

        self.pending_button = discord.ui.Button(label="Pending", style=discord.ButtonStyle.primary, custom_id='pending')
        self.pending_button.disabled = True

        if company:
            if review_data['type'] == 'Pending':
                self.add_item(self.reject_button)
                self.add_item(self.accept_button)

            elif review_data['type'] == 'Approved':
                self.add_item(self.approve_button)

        else:
            if review_data['type'] == 'Pending':
                self.add_item(self.pending_button)

            elif review_data['type'] == 'Approved':
                self.add_item(self.approve_button)
                self.add_item(self.upload_button)

            elif review_data['type'] == 'Rejected':
                self.reject_button.disabled = True
                self.add_item(self.reject_button)
                self.add_item(self.upload_button)

    async def upload_button_callback(self, interaction: discord.Interaction):
        print('upload button clicked')
        pass

    #TODO: add rejected message to influencer
    async def reject_button_callback(self, interaction: discord.Interaction):
        from modal import ReviewRejectModal
        review = Review()
        print(f'review data {self.review_data}')
        response = review.update(self.review_data['id'], link=self.review_data['link'], review_type='Rejected', descripton=self.review_data['description'])
        self.bot
        if response['success']:
            self.embed_data['type'] = 'Rejected'
            await interaction.response.send_modal(ReviewRejectModal(self.review_data, self.bot))
            
        self.stop()

    async def accept_button_callback(self, interaction: discord.Interaction):
        review = Review()
        response = review.update(self.review_data['id'], link=self.review_data['link'], review_type='Approved', descripton=self.review_data['description'])

        if response['success']:
            self.remove_item(self.reject_button)
            self.remove_item(self.accept_button)
            self.add_item(self.approve_button)

        #     guild_id = Enums.GUILD_ID.value  # The guild (server) where the command was called
        #     guild = self.bot.get_guild(guild_id)
        #     user = discord.utils.get(guild.members, id=self.user_id)  # Fetch the user by ID

        #     job_view = JobView(self.job_data, self.bot)
        #     await user.send(embed=job_view.embed, view=job_view)
            await interaction.response.edit_message(view=self)
        # else:
        #     await interaction.response.send_message(response['message'])
        # self.stop()