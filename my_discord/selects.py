from typing import Any
import discord
from discord.ui import Select
from modal import JobModal, BankRegistrationModal
from utils.enums import Enums

class SelectRoles(Select):
    def __init__(self, bot, roles, url):
        self.bot = bot
        self.url = url
        # roles = self.clean_roles(roles)
        options = [discord.SelectOption(label=role, description='') for role in roles[:25]]
        super().__init__(options = options, placeholder='Please select roles', min_values=1, max_values=len(roles))

    async def callback(self, interaction: discord.Interaction) -> Any:
        roles = self.values
        success = await interaction.response.send_modal(JobModal(self.bot, roles, self.url))

        print(f'{success=}')
        return success
    
    def clean_roles(self, roles):
        roles = [role.lower().replace('job', '') for role in roles if '[job]' in role.lower()]
        return roles[:25]
    
class SelectBankNames(Select):
    def __init__(self, url):
        self.url = url
        bank_names = Enums.BANK_NAMES.value
        options = [discord.SelectOption(label=bank + ' Bank', description='') for bank in bank_names]
        super().__init__(options=options, placeholder='Please Bank name', min_values=1)

    async def callback(self, interaction: discord.Interaction) -> Any:
        bank_name = self.values[0]
        return await interaction.response.send_modal(BankRegistrationModal(bank_name, self.url))