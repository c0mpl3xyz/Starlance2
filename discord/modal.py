from typing import List
from discord.ui import Modal, TextInput
from discord import Interaction
from discord import ui
import discord

class JobModal(ui.Modal, title="Job registration"):    
    def __init__(self, roles):
        self.name = ui.TextInput(label="Job Name", placeholder="Your job name here", required=True, min_length=2, max_length=100)
        self.age = ui.TextInput(label="Age", placeholder="Your age here", required=True, style=discord.TextStyle.short)
        self.date = ui.TextInput(label="Birth Date", placeholder="DD/MM/YYYY", required=True, style=discord.TextStyle.short)
        self.roles = roles

        super().__init__()
        self.add_item(self.name)
        self.add_item(self.age)
        self.add_item(self.date)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'roles {self.roles} Hello **{self.name}**')