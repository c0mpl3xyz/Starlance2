from typing import Any
import discord
from discord.ui import Select, View
from modal import JobModal, BankRegistrationModal, SocialRegisterModal
from utils.enums import Enums

class MessageSelect(Select):
    def __init__(self, bot, roles):
        self.bot = bot
        self.roles_message = None
        roles = self.clean_roles(roles)
        self.all_roles = 'All Roles'
        roles = [self.all_roles] + roles
        roles = roles[:25]
        options = [discord.SelectOption(label=role, description='') for role in roles]
        super().__init__(options = options, placeholder='Please select roles', min_values=1, max_values=len(roles))

    async def callback(self, interaction: discord.Interaction) -> Any:
        from modal import MessageModal
        roles = self.values
        if self.all_roles in roles:
            i = roles.index(self.all_roles)
            roles[i] = '@everyone'

        modal = MessageModal(self.bot, roles=roles)
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.finished:
            message = self.roles_message
            await message.delete()
        return
    
    def clean_roles(self, roles):
        roles = [role.lower().replace('[job]', '').strip() for role in roles if '[job]' in role.lower()]
        return roles[:25]
    
class SelectRoles(Select):
    def __init__(self, bot, roles, url):
        self.bot = bot
        self.url = url
        self.message = None
        roles = self.clean_roles(roles)
        self.all_roles = 'All Roles'
        roles = [self.all_roles] + roles
        roles = roles[:25]
        options = [discord.SelectOption(label=role, description='') for role in roles]
        super().__init__(options = options, placeholder='Please select roles', min_values=1, max_values=len(roles))

    async def callback(self, interaction: discord.Interaction) -> Any:
        roles = self.values
        if self.all_roles in roles:
            i = roles.index(self.all_roles)
            roles[i] = '@everyone'

        view = View()
        select = SelectBudget(self.bot, roles, self.url)
        select.select_roles_message = self.message
        view.add_item(select)
        await interaction.response.send_message('Select budget', view=view)
        return
    
    def clean_roles(self, roles):
        roles = [role.lower().replace('[job]', '').strip() for role in roles if '[job]' in role.lower()]
        return roles[:25]
    
class SelectBudget(Select):
    def __init__(self, bot, roles, url):
        self.bot = bot
        self.roles = roles
        self.url = url
        self.finished = False
        self.select_roles_message = None
        self.select_budget_message = None

        cashes = list(range(2000000, 6000000, 250000))
        options = [discord.SelectOption(label=str(f"{cash:,}") + ' ₮', description='') for cash in cashes[:25]]
        super().__init__(options=options, placeholder='Please select Budget', min_values=1)

    async def callback(self, interaction: discord.Interaction) -> Any:
        budget = self.values[0].split(' ')[0].replace(',', '')
        job_modal = JobModal(self.bot, self.roles, int(budget), self.url)
        await interaction.response.send_modal(job_modal)
        await job_modal.wait()
        if job_modal.finished:
            await self.select_roles_message.delete()
    
class UploadLinkSelect(Select):
    def __init__(self, bot, user_id, job_id, server_id, job_register_id, review_id, edit=False):
        self.user_id = user_id
        self.job_id = job_id
        self.server_id = server_id
        self.job_register_id = job_register_id
        self.review_id = review_id
        self.bot = bot
        self.edit = edit

        socials = Enums.SOCIAL_ACCOUNTS.value
        options = [discord.SelectOption(label=social, description='') for social in socials]
        super().__init__(options=options, placeholder='Please select Your Social account', min_values=1, max_values=len(options))

    async def callback(self, interaction: discord.Interaction) -> Any:
        socials = self.values
        modal = SocialRegisterModal(self.user_id, self.job_id, self.server_id, self.job_register_id, self.review_id, socials, self.bot, self.edit)
        await interaction.response.send_modal(modal)
        await modal.wait()
        await interaction.message.delete()

class SelectBankNames(Select):
    def __init__(self, url):
        self.url = url
        bank_names = Enums.BANK_NAMES.value
        options = [discord.SelectOption(label=bank + ' Bank', description='') for bank in bank_names]
        super().__init__(options=options, placeholder='Please Bank name', min_values=1)

    async def callback(self, interaction: discord.Interaction) -> Any:
        bank_name = self.values[0]
        return await interaction.response.send_modal(BankRegistrationModal(bank_name, self.url))