import discord
from discord import Embed

class LoginEmbed(Embed):
     def __init__(self, server_name):
        super().__init__(
            title='Login with Facebook',
            color = discord.Color.random()
            )
        
        self.add_field(name=f'Login to Facebook with discord server: <{server_name}>', value=server_name, inline=False)

class UserEmbed(Embed):
     def __init__(self, user_data):
        super().__init__(
            title='User Status',
            color = discord.Color.random()
            )
        
        self.add_field(name='User', value=f'<@{user_data["user_id"]}>', inline=False)
        self.add_field(name="Total Points Of Lifetime", value=user_data['total_points'])
        self.add_field(name="Available Points", value=user_data['points'])
        self.add_field(name="Register Number", value=user_data['register'])
        self.add_field(name="Bank Name", value=user_data['bank_name'])
        self.add_field(name="Bank Number", value=user_data['bank_number'])

class CollectEmbed(Embed):
     def __init__(self, user_data, points):
        super().__init__(
            title='User Status',
            color = discord.Color.random()
            )
        
        self.add_field(name='User', value=f'<@{user_data["user_id"]}>', inline=False)
        self.add_field(name="Register Number", value=user_data['register'])
        self.add_field(name="Bank Name", value=user_data['bank_name'])
        self.add_field(name="Bank Number", value=user_data['bank_number'])
        self.add_field(name="Collect points", value=points)

class ReviewEmbed(Embed):
     def __init__(self, data: dict):
        self.data = data
        super().__init__(
            title=data['server_name'],
            color = discord.Color.random()
            )
        self.add_field(name='Job Name', value=data['job_name'], inline=False)
        self.add_field(name='Job Description', value=data['job_description'], inline=False)
        self.add_field(name="Message", value=data['description'], inline=False)
        self.add_field(name='link', value=data['link'], inline=False)

class ContentEmbed(Embed):
     def __init__(self, review_data, content_data):
        self.review_data = review_data
        self.content_data = content_data

        color = None
        if content_data['active'] == 0 or not content_data['active']:
            color = discord.Color.red()
        else:
            color = discord.Color.green()

        super().__init__(
            title=review_data['server_name'],
            color = color
            )
        
        self.add_field(name='Job Name', value=review_data['job_name'], inline=False)
        self.add_field(name='Job Description', value=review_data['job_description'], inline=False)
        self.add_field(name='Content link', value=content_data['link'], inline=False)

        if 'initial_plays' in content_data:
            self.add_field(name='Initial plays', value=content_data['initial_plays'])
        if 'total_plays' in content_data:
            self.add_field(name='Views', value=content_data['total_plays'])
        if 'likes' in content_data:
            self.add_field(name='Likes', value=content_data['likes'])
        if 'replays' in content_data:
            self.add_field(name='Replay', value=content_data['replays'])
        if 'saves' in content_data:
            self.add_field(name='Saves', value=content_data['saves'])
        if 'shares' in content_data:
            self.add_field(name='Shares', value=content_data['shares'])
        if 'comments' in content_data:
            self.add_field(name='Comments', value=content_data['comments'])
        if 'account_reach' in content_data:
            self.add_field(name='Account reached', value=content_data['account_reach'])
        if 'total_interactions' in content_data:
            self.add_field(name='Total interaction', value=content_data['total_interactions'])
        if 'engagement' in content_data:
            self.add_field(name='Engagements', value=content_data['engagement'])
        if 'engagement_rate' in content_data:
            self.add_field(name='Engagement Rate', value=content_data['engagement_rate'])
        if 'active' in content_data:
            self.add_field(name='Active', value=content_data['active'])
        if 'points' in content_data:
            self.add_field(name='Total Points', value=content_data['points'], inline=False)

class JobEmbed(Embed):
    def __init__(self, job_data, contents):
        color = None
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
            title=job_data['server_name'],
            description=job_data['description'],
            color=color
        )

        self.add_field(name="Job name", value=job_data['name'], inline=False)
        self.add_field(name="Start date", value=job_data['start_date'])
        self.add_field(name="Duration", value=f"{job_data['duration']} days")
        self.add_field(name="End date", value=job_data['end_date'])
        self.add_field(name="Participation date", value=job_data['participation_date'])
        self.add_field(name="Job files", value=f"[Click Here]({job_data['upload_link']})")
        self.add_field(name="Roles", value=job_data['roles'].replace(',', ' '), inline=False)

        for idx, content in enumerate(contents):
            self.add_field(name=f'content-{idx}', value=f"[Click Here]({content['link']})", inline=False)

class ApproveEmbed(Embed):
    def __init__(self, data):
        self.user = f'<@{data["user_id"]}>'
        self.user_roles = data['user_roles']
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
        
        self.add_field(name="User", value=self.user)
        self.add_field(name="Job name", value=self.job_name)
        self.add_field(name="Start date", value=self.start_date)
        self.add_field(name="Description", value=self.description)
        self.add_field(name="Job roles", value=self.job_roles.replace(',', ' '), inline=False)
        self.add_field(name="User roles", value=' '.join(self.user_roles), inline=False)