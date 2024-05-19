from discord.ui import View
import discord
import requests
from usecases.register_job import RegisterJob

class JobView(discord.ui.View):
    def __init__(self, job_data):
        self.job_data = job_data
        super().__init__(timeout=350)
        self.description = '\n'.join([f'{k}: {v}' for (k, v) in job_data.items() if k != 'discord_server_id'])
        
        self.reject_button = discord.ui.Button(label="Reject", style=discord.ButtonStyle.danger, custom_id='reject', emoji='✖')
        self.reject_button.callback = self.reject_button_callback
        
        self.accept_button = discord.ui.Button(label="Accept", style=discord.ButtonStyle.green, custom_id='accept', emoji='✔')
        self.accept_button.callback = self.accept_button_callback

        self.pending_button = discord.ui.Button(label="Pending", style=discord.ButtonStyle.primary, custom_id='pending')
        self.pending_button.disabled = True

        if 'type' not in job_data or job_data.type is None:
            self.add_item(self.reject_button)
            self.add_item(self.accept_button)
        
        elif job_data.type == 'Pending':
            self.add_item(self.pending_button)
        
        elif job_data.type == 'Rejected':
            self.reject_button.label = 'Rejected'
            self.reject_button.disabled = True
            self.add_item(self.reject_button)

    async def reject_button_callback(self, interaction: discord.Interaction):
        await interaction.message.delete()
        self.stop()

    async def accept_button_callback(self, interaction: discord.Interaction):
        register_job = RegisterJob()
        response = register_job.register(interaction.user.id, self.job_data['job_id'])

        if response['success']:
            self.remove_item(self.reject_button)
            self.remove_item(self.accept_button)
            self.add_item(self.pending_button)
            await interaction.response.edit_message(view=self)
        else:
            await interaction.response.send_message(response['message'])
        self.stop()