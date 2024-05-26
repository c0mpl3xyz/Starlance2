from discord.ui import View
from embeds import JobEmbed
import discord
import requests
from usecases.register_job import RegisterJob
from usecases.get_job_by_id import GetJobById
from embeds import ApproveEmbed
from utils.enums import Enums

class JobView(discord.ui.View):
    def __init__(self, job_data, bot, company=False):
        self.job_data = job_data
        self.bot = bot
        self.embed = JobEmbed(job_data)
        if 'type' in job_data:
            self.type = job_data['type']

        super().__init__(timeout=350)
        self.description = '\n'.join([f'{k}: {v}' for (k, v) in job_data.items() if k != 'discord_server_id'])
        
        self.reject_button = discord.ui.Button(label="Reject", style=discord.ButtonStyle.danger, custom_id='reject', emoji='✖')
        self.reject_button.callback = self.reject_button_callback
        
        self.accept_button = discord.ui.Button(label="Accept", style=discord.ButtonStyle.green, custom_id='accept', emoji='✔')
        self.accept_button.callback = self.accept_button_callback

        self.pending_button = discord.ui.Button(label="Pending", style=discord.ButtonStyle.primary, custom_id='pending')
        self.pending_button.disabled = True

        self.upload_button = discord.ui.Button(label='Upload link', style=discord.ButtonStyle.green, custom_id='upload', emoji='➕')
        self.upload_button.callback = self.upload_button_callback

        if not company:
            if 'type' not in job_data or job_data['type'] is None:
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
                self.add_item(self.upload_button)

    async def reject_button_callback(self, interaction: discord.Interaction):
        register_job = RegisterJob()
        response = register_job.register(interaction.user.id, self.job_data['job_id'], 'Rejected')
        if response['success']:
            await interaction.message.delete()
        self.stop()

    async def upload_button_callback(self, interaction: discord.Interaction):
        from selects import UploadLinkSelect
        view = View()
        view.add_item(UploadLinkSelect(self.bot, interaction.user.id, self.job_data['job_id'], self.job_data['discord_server_id']))
        await interaction.send_response('Upload social links', view=view)
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
            register_job = RegisterJob()
            response = register_job.update(self.user_id, self.server_id, 'Rejected')
            if response['success']:
                await interaction.message.delete()
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

                print(f'JOB DATA: {self.job_data}')
                job_view = JobView(self.job_data, self.bot)
                await user.send(embed=job_view.embed, view=job_view)
                await interaction.response.edit_message(view=self)
            else:
                await interaction.response.send_message(response['message'])
            self.stop()