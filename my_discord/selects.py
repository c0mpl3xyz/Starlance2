from typing import Any
import discord
from discord.ui import Select
from modal import JobModal, BankRegistrationModal
from utils.enums import Enums

class SelectRoles(Select):
    def clean_roles(self, roles):
        roles = [role for role in roles if '[job]' in role.lower()]
        return roles

    def __init__(self, roles):
        roles = self.clean_roles(roles)
        options = [discord.SelectOption(label=role, value=role, description='') for role in roles[:25]]
        print('test3')
        super().__init__(options = options, placeholder='Please select roles')

    async def callback(self, interaction: discord.Interaction) -> Any:
        roles = self.values
        print('test2')
        return await interaction.response.send_modal(JobModal(roles))
    
class SelectBankNames(Select):
    def __init__(self, url):
        self.url = url
        bank_names = Enums.BANK_NAMES.value
        options = [discord.SelectOption(label=bank + ' Bank', description='') for bank in bank_names]
        super().__init__(options=options, placeholder='Please Bank name', min_values=1)

    async def callback(self, interaction: discord.Interaction) -> Any:
        bank_name = self.values[0]
        return await interaction.response.send_modal(BankRegistrationModal(bank_name, self.url))