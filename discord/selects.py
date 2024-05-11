from typing import Any
import discord
from discord import ui
from modal import JobModal

class SelectRoles(ui.Select):
    def __init__(self, roles):
        options = [discord.SelectOption(label=role, description='') for role in roles]
        super().__init__(options = options, placeholder='Please select roles', min_values=1, max_values=5)

    async def callback(self, interaction: discord.Interaction) -> Any:
        roles = self.values
        return await interaction.response.send_modal(JobModal(roles))