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

        print(f'{self.review_data=}')
        print(f'{self.content_data=}')
        super().__init__(
            title=review_data['server_name'],
            color = color
            )
        
        self.add_field(name='Job Name', value=review_data['job_name'], inline=False)
        self.add_field(name='Job Description', value=review_data['job_description'], inline=False)
        self.add_field(name='Content link', value=content_data['link'], inline=False)

        if 'initial_plays' in content_data:
            self.add_field(name='Initial plays', value=content_data['initial_plays'])
        if 'plays' in content_data:
            self.add_field(name='Plays', value=content_data['plays'])
        if 'likes' in content_data:
            self.add_field(name='Likes', value=content_data['likes'])
        if 'replays' in content_data:
            self.add_field(name='Replays', value=content_data['replays'])
        if 'saves' in content_data:
            self.add_field(name='Saves', value=content_data['saves'])
        if 'shares' in content_data:
            self.add_field(name='Shares', value=content_data['shares'])
        if 'comments' in content_data:
            self.add_field(name='Comments', value=content_data['comments'])
        if 'percent_followers' in content_data:
            self.add_field(name='Percent of followers', value=content_data['percent_followers'])
        if 'percent_non_followers' in content_data:
            self.add_field(name='Percent of followers', value=content_data['percent_non_followers'])

class JobEmbed(Embed):
    def __init__(self, job_data):
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

        if 'instagram_link' in job_data:
            self.add_field(name='Instagram link', value=f"[Click Here]({job_data['instagram_link']})")
        if 'facebook_link' in job_data:
            self.add_field(name='Facebook link', value=f"[Click Here]({job_data['facebook_link']})")
        if 'tiktok_link' in job_data:
            self.add_field(name='Tiktok link', value=f"[Click Here]({job_data['tiktok_link']})")
        if 'youtube_link' in job_data:
            self.add_field(name='Youtube link', value=f"[Click Here]({job_data['youtube_link']})")

class ApproveEmbed(Embed):
    def __init__(self, data):
        self.user = f'<@{data["user_id"]}>'
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
        self.add_field(name="User", value=self.user_name)
        self.add_field(name="Job name", value=self.job_name)
        self.add_field(name="Start date", value=self.start_date)
        self.add_field(name="Job roles", value=self.job_roles.replace(',', ' '), inline=False)
        # self.add_field(name="User roles", value=self.user_roles.replace(',', ' '), inline=False)