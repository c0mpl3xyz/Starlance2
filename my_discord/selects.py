from typing import Any
import discord
from discord.ui import Select, View
from modal import JobModal, BankRegistrationModal, SocialRegisterModal
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
        view = View()
        view.add_item(SelectBudget(self.bot, roles, self.url))
        success = await interaction.response.send_message('Select budget', view=view)

        print(f'{success=}')
        return success
    
    def clean_roles(self, roles):
        roles = [role.lower().replace('job', '') for role in roles if '[job]' in role.lower()]
        return roles[:25]
    
class SelectBudget(Select):
    def __init__(self, bot, roles, url):
        self.bot = bot
        self.roles = roles
        self.url = url

        cashes = list(range(500000, 10250000, 250000))
        options = [discord.SelectOption(label=str(cash) + ' tugrik', description='') for cash in cashes[:25]]
        super().__init__(options=options, placeholder='Please select Budget', min_values=1)

    async def callback(self, interaction: discord.Interaction) -> Any:
        budget = self.values[0].split(' ')[0]
        await interaction.response.send_modal(JobModal(self.bot, self.roles, int(budget), self.url))

class UploadLinkSelect(Select):
    def __init__(self, bot, user_id, job_id, server_id):
        self.user_id = user_id
        self.job_id = job_id
        self.server_id = server_id
        self.bot = bot

        socials = ['Facebook', 'Instagram', 'TikTok', 'Youtube']
        options = [discord.SelectOption(label=social, description='') for social in socials]
        super().__init__(options=options, placeholder='Please select Your Social account', min_values=1, max_value=4)

    async def callback(self, interaction: discord.Interaction) -> Any:
        socials = self.values
        await interaction.response.send_modal(SocialRegisterModal(self.user_id, self.job_id, socials, self.server_id))

class SelectBankNames(Select):
    def __init__(self, url):
        self.url = url
        bank_names = Enums.BANK_NAMES.value
        options = [discord.SelectOption(label=bank + ' Bank', description='') for bank in bank_names]
        super().__init__(options=options, placeholder='Please Bank name', min_values=1)

    async def callback(self, interaction: discord.Interaction) -> Any:
        bank_name = self.values[0]
        return await interaction.response.send_modal(BankRegistrationModal(bank_name, self.url))