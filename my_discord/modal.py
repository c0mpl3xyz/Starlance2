from typing import List
import discord, requests
from discord.ui import Modal, TextInput
from discord import Interaction

class JobModal(Modal, title="Job registration"):    
    def __init__(self, roles):
        self.name = TextInput(label="Job Name", placeholder="Your job name here", required=True, min_length=2, max_length=100)
        self.age = TextInput(label="Age", placeholder="Your age here", required=True, style=discord.TextStyle.short)
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
        print(f'debug 1')
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
        print(response.text)
        if response and 'success' in response.json():
            success = response.json()['success']
        if success:
            message = 'Bank registration succeeded'
        else:
            message = 'Bank registration failed'

        await interaction.response.send_message(message)


