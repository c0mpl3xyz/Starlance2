import discord
from discord import Embed

class UserEmbed(Embed):
     def __init__(self, user_id, user_name):
        self.user_id = user_id
        super().__init__(
            title='User Status',
            color = discord.Color.random()
            )
        
        self.add_field(name='Name', value=user_name, inline=False)
        self.add_field(name="Content count", value='1')
        self.add_field(name="Like count", value='0')
        self.add_field(name="View count", value='3')
        self.add_field(name="Comment count", value='0')
        self.add_field(name="Points", value='4')

class JobEmbed(Embed):
    def __init__(self, job_data):
        if 'type' not in job_data:
            color = discord.Color.green()
        elif job_data['type'] == 'Pending':
            color = discord.Color.yellow()
        elif job_data['type'] == 'Rejected':
            color = discord.Color.red()
        elif job_data['type'] == 'Finished':
            color = discord.Color.red()
        elif job_data['type'] == 'Full':
            color = discord.Color.red()

        super().__init__(
            title=job_data['name'],
            description=job_data['description'],
            color=color
        )

        self.add_field(name="Start date", value=job_data['start_date'])
        self.add_field(name="Duration", value=f"{job_data['duration']} days")
        self.add_field(name="End date", value=job_data['end_date'])
        self.add_field(name="Participation date", value=job_data['participation_date'])
        self.add_field(name="Job files", value=f"[Click Here]({job_data['upload_link']})")
        self.add_field(name="Roles", value=job_data['roles'].replace(',', ' '), inline=False)

class ApproveEmbed(Embed):
    def __init__(self, data):
        self.user_name = data['user_name']
        # self.user_roles = data['user_roles']
        self.job_name = data['job_name']
        self.job_roles = data['job_roles']
        self.start_date = data['start_date']
        self.description = data['description']
        job_type = data['type']

        if job_type is not None and job_type == 'Rejected':
            color = discord.Color.red()
        
        if job_type is not None and job_type == 'Pending':
            color = discord.Color.green()

        if job_type is not None and job_type == 'Approved':
            color = discord.Color.dark_grey()

        super().__init__(
            title=self.job_name,
            description=self.description,
            color=color
        )

        self.add_field(name="User", value=self.user_name)
        self.add_field(name="Job name", value=self.job_name)
        self.add_field(name="Start date", value=self.start_date)
        self.add_field(name="Job roles", value=self.job_roles.replace(',', ' '), inline=False)
        # self.add_field(name="User roles", value=self.user_roles.replace(',', ' '), inline=False)