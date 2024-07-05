from typing import Any
import discord
from discord.ui import Select, View
from modal import JobModal, BankRegistrationModal, SocialRegisterModal
from utils.enums import Enums

class MessageSelect(Select):
    def __init__(self, bot, roles):
        self.bot = bot
        self.roles_message = None
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
            roles[i] = 'Influencer'

        modal = MessageModal(self.bot, roles=roles)
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.finished:
            message = self.roles_message
            await message.delete()
        return
    
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
            roles[i] = 'Influencer'

        view = View()
        select = SelectBudget(self.bot, roles, self.url)
        select.select_roles_message = self.message
        view.add_item(select)
        select.message = await interaction.response.send_message('Select budget', view=view)
        await view.wait()
        if select.finished:
            return
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
        self.message = None
        self.select_roles_message = None

        cashes = list(range(2000000, 6000000, 250000))
        options = [discord.SelectOption(label=str(f"{cash:,}") + ' ₮', description='') for cash in cashes[:25]]
        super().__init__(options=options, placeholder='Please select Budget', min_values=1)

    async def callback(self, interaction: discord.Interaction) -> Any:
        budget = self.values[0].split(' ')[0].replace(',', '')
        point_select = SelectPoint(self.bot, self.roles, int(budget), self.url)
        point_select.select_roles_message = self.select_roles_message
        point_select.select_budget_message = self.message

        view = View()
        view.add_item(point_select)
        await interaction.response.send_message('Select Budget', view=view)
        await view.wait()
        if point_select.finished:
            self.finished = True

class SelectPoint(Select):
    def __init__(self, bot, roles, budget, url):
        self.bot = bot
        self.roles = roles
        self.budget = budget
        self.url = url
        self.finished = False
        self.select_roles_message = None
        self.select_budget_message = None
        self.select_point_message = None

        points = list(range(10, 50, 5))
        options = [discord.SelectOption(label=str(f"{cash:,}") + ' ₮', description='') for cash in points[:25]]
        super().__init__(options=options, placeholder='Please select Points', min_values=1)

    async def callback(self, interaction: discord.Interaction) -> Any:
        point = int(str(self.values[0]).replace(' ₮', ''))
        job_modal = JobModal(self.bot, self.roles, self.budget, point, self.url)
        await interaction.response.send_modal(job_modal)
        await job_modal.wait()

        if job_modal.finished:
            self.finished = True
            await self.select_roles_message.delete()

class UploadLinkSelect(Select):
    def __init__(self, bot, user_id, job_id, server_id, job_register_id, review_id, content_data=None, edit=False):
        self.user_id = user_id
        self.job_id = job_id
        self.server_id = server_id
        self.content_data = content_data
        self.job_register_id = job_register_id
        self.review_id = review_id
        self.bot = bot
        self.edit = edit
        self.is_finished = False

        socials = Enums.SOCIAL_ACCOUNTS.value
        options = [discord.SelectOption(label=social, description='') for social in socials]
        super().__init__(options=options, placeholder='Please select Your Social account', min_values=1, max_values=len(options))

    async def callback(self, interaction: discord.Interaction) -> Any:
        socials = self.values
        modal = SocialRegisterModal(self.user_id, self.job_id, self.server_id, self.job_register_id, self.review_id, socials, self.bot, self.content_data, self.edit)
        await interaction.response.send_modal(modal)
        await modal.wait()
        if modal.finished:
            self.is_finished = True
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