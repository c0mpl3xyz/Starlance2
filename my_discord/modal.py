from typing import List
import discord, requests
from discord.ui import Modal, TextInput
from discord import Interaction

start_date, duration, end_date, modified_date, participation_date, job_delete_date, description, upload_file_links, requirements) -> bool:
class JobModal(Modal, title="Job registration"):    
    def __init__(self, roles):
        
        self.name = TextInput(label="Job Name", placeholder="Your job name here", required=True, min_length=2, max_length=100)
        self.age = TextInput(label="Age", placeholder="Your age here", required=True, style=discord.TextStyle.short)
        self.date = TextInput(label="Birth Date", placeholder="DD/MM/YYYY", required=True, style=discord.TextStyle.short)
        self.date = TextInput(label="Birth Date", placeholder="DD/MM/YYYY", required=True, style=discord.TextStyle.short)
        self.date = TextInput(label="Birth Date", placeholder="DD/MM/YYYY", required=True, style=discord.TextStyle.short)
        self.date = TextInput(label="Birth Date", placeholder="DD/MM/YYYY", required=True, style=discord.TextStyle.short)
        self.date = TextInput(label="Birth Date", placeholder="DD/MM/YYYY", required=True, style=discord.TextStyle.short)
        self.date = TextInput(label="Birth Date", placeholder="DD/MM/YYYY", required=True, style=discord.TextStyle.short)
        self.date = TextInput(label="Birth Date", placeholder="DD/MM/YYYY", required=True, style=discord.TextStyle.short)
        self.roles = roles

        super().__init__()
        self.add_item(self.name)
        self.add_item(self.age)
        self.add_item(self.date)

    async def on_submit(self, interaction: Interaction):
        await interaction.response.send_message(f'roles {self.roles} Hello **{self.name}**')

class BankRegistrationModal(Modal, title='Bank Registration'):
    def __init__(self, bank_name, url):
        self.url = url
        self.bank_name = bank_name
        self.bank_number = TextInput(label="Bank number", placeholder="Your bank number", required=True, min_length=2, max_length=100)
        self.register = TextInput(label="Register", placeholder="Your register", required=True, min_length=2, max_length=100)

        super().__init__()
        self.add_item(self.bank_number)
        self.add_item(self.register)

    async def on_submit(self, interaction: Interaction):
        success = False
        message: str = ''

        data = {
            'user_id': interaction.user.id,
            'bank_name': str(self.bank_name.replace('Bank', '').strip()),
            'bank_number': str(self.bank_number),
            'register': str(self.register)
        }

        response = requests.post(self.url + '/user/bank_register', json=data)
        if response and 'success' in response.json():
            success = response.json()['success']

        channel_name = '' #TODO: CHANGE IT
        channel = discord.utils.get(interaction.guild.channels, name=channel_name)
        if success:
            message = f'Bank Registration\nUser: {interaction.user.global_name}\nBank name: {self.bank_name}\nBank number: {self.bank_number}\nRegister: {self.register}'
            if channel:
                await channel.send(message)
                await interaction.message.delete()
        else:
            message = 'Bank registration failed'

        await interaction.response.send_message(message)


