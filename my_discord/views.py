from discord.ui import View
import discord
import requests
from usecases.register_job import RegisterJob

class JobView(discord.ui.View):
    def __init__(self, job_data):
        self.job_data = job_data
        super().__init__(timeout=350)
        self.description = '\n'.join([f'{k}: {v}' for (k, v) in job_data.items() if k != 'discord_server_id'])

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger, custom_id='reject', emoji='✖')
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        self.stop()

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, custom_id='accept', emoji='✔')
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        reject_button = [x for x in self.children if x.custom_id == 'reject'][0]
        self.remove_item(reject_button)
        button.disabled = True
        button.label = 'Pending'
        button.style = discord.ButtonStyle.primary

        register_job = RegisterJob()
        response = register_job.register(interaction.user.id, self.job_data['job_id'])

        if response['success']:
            await interaction.response.edit_message(view=self)
        else:
            await interaction.response.send_message(response['message'])
        self.stop()