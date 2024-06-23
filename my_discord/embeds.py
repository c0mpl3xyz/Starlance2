import discord
from discord import Embed

class LoginEmbed(Embed):
     def __init__(self, server_name):
        super().__init__(
            title='Login with Facebook',
            color = discord.Color.random()
            )
        
        self.add_field(name=f'Login to Facebook with discord server: <{server_name}>', value=server_name, inline=False)

class MessageEmbed(Embed):
     def __init__(self, message_title, message):
        super().__init__(
            title=message_title,
            color = discord.Color.random()
            )
        
        self.add_field(name='Mesasage', value=message)

class UserEmbed(Embed):
     def __init__(self, user_data):
        super().__init__(
            title='User Status',
            color = discord.Color.random()
            )
        
        tugrik = user_data['points'] * 10
        self.add_field(name='User', value=f'<@{user_data["user_id"]}>', inline=False)
        self.add_field(name="Total Points Of Lifetime", value=user_data['total_points'])
        self.add_field(name="Available Points", value=user_data['points'])
        self.add_field(name="Available Points in MNT", value=f'{tugrik} MNT')
        self.add_field(name="Register Number", value=user_data['register'])
        self.add_field(name="Bank Name", value=user_data['bank_name'])
        self.add_field(name="Bank Number", value=user_data['bank_number'])

class CollectEmbed(Embed):
     def __init__(self, user_data, points):
        super().__init__(
            title='User Status',
            color = discord.Color.random()
            )
        
        tugrik = points * 10
        self.add_field(name='User', value=f'<@{user_data["user_id"]}>', inline=False)
        self.add_field(name="Register Number", value=user_data['register'])
        self.add_field(name="Bank Name", value=user_data['bank_name'])
        self.add_field(name="Bank Number", value=user_data['bank_number'])
        self.add_field(name="Collect points", value=points)
        self.add_field(name="Collect points in MNT", value=f'{tugrik} MNT')

class ReviewEmbed(Embed):
     def __init__(self, data: dict):
        self.data = data
        super().__init__(
            title=data['server_name'],
            # description=data['job_description'],
            color = discord.Color.random()
            )
        self.add_field(name='Job Name', value=data['job_name'], inline=False)
        self.add_field(name='Job Description', value=f'{data["job_description"][:300]}', inline=False)
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
        self.add_field(name='User', value=f'<@{content_data["user_id"]}>')
        self.add_field(name='Content link', value=content_data['link'], inline=False)
        if 'total_plays' in content_data:
            self.add_field(name='Total Views', value=content_data['total_plays'])
        if 'initial_plays' in content_data:
            self.add_field(name='Initial plays', value=content_data['initial_plays'])
        if 'replays' in content_data:
            self.add_field(name='Replay', value=content_data['replays'])
        if 'likes' in content_data:
            self.add_field(name='Likes', value=content_data['likes'])
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
        if 'engagement_rate' in content_data:
            self.add_field(name='Engagement Rate', value=content_data['engagement_rate'])
        if 'active' in content_data:
            self.add_field(name='Active', value=content_data['active'])
        if 'points' in content_data:
            self.add_field(name='Total Points', value=content_data['points'], inline=False)

class JobEmbed(Embed):
    def __init__(self, job_data, contents, company):
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
            description=f'{job_data["description"]}',
            color=color
        )

        self.add_field(name="Job name", value=job_data['name'], inline=False)
        self.add_field(name="Start date", value=job_data['start_date'])
        self.add_field(name="Duration", value=f"{job_data['duration']} days")
        self.add_field(name="End date", value=job_data['end_date'])
        self.add_field(name="Participation date", value=job_data['participation_date'])
        self.add_field(name="Total Budget", value=str(job_data['budget']) + ' MNT')
        self.add_field(name="Job files", value=f"[Click Here]({job_data['upload_link']})")
        self.add_field(name="1 view point", value=job_data['point'])
        self.add_field(name="Roles", value=job_data['roles'].replace(',', ' '), inline=False)

        if company:
            if not len(contents):
                self.add_field(name="Job Report", value='There is no contents yet!', inline=False)
            else:
                self.add_field(name="Job Report", value='Report of this Job!', inline=False)
                self.add_field(name="Content Count", value=len(contents), inline=False)
                content_data = self.get_status(contents)
                self.add_field(name="Total Views", value=content_data['views'])
                self.add_field(name="Total Initial Plays", value=content_data['initial_plays'])
                self.add_field(name="Total Replays ", value=content_data['replays'])
                self.add_field(name="Total Likes", value=content_data['likes'])
                self.add_field(name="Total Saves", value=content_data['saves'])
                self.add_field(name="Total Shares", value=content_data['shares'])
                self.add_field(name="Total Comments", value=content_data['comments'])
                self.add_field(name="Total Account Reach", value=content_data['account_reach'])
                self.add_field(name="Average Engagement Rate", value=content_data['engagement_rate'])
                self.add_field(name="Total Points", value=content_data['points'])
                self.add_field(name="Total Points", value=content_data['points'])
        
    def get_status(self, contents):
        if not len(contents):
            return []
        
        data = {
            'views': 0,
            'initial_plays': 0,
            'replays': 0,
            'likes': 0,
            'saves': 0,
            'shares': 0,
            'comments': 0,
            'account_reach': 0,
            'engagement_rate': 0.0,
            'points': 0,
        }

        for content in contents:
            data['views'] += content['total_plays']
            data['initial_plays'] += content['initial_plays']
            data['replays'] += content['replays']
            data['likes'] += content['likes']
            data['saves'] += content['saves']
            data['shares'] += content['shares']
            data['comments'] += content['comments']
            data['account_reach'] += content['account_reach']
            data['engagement_rate'] += content['engagement_rate']
            data['points'] += content['points']

        data['engagement_rate'] = data['engagement_rate'] / len(contents)

        return data
    
class ApproveEmbed(Embed):
    def __init__(self, data):
        self.user = f'<@{data["user_id"]}>'
        self.user_roles = data['user_roles']
        self.job_name = data['job_name']
        self.job_roles = data['job_roles']
        self.start_date = data['start_date']
        self.data = data
        job_type = data['type']

        if job_type is not None and job_type == 'Rejected':
            color = discord.Color.red()
        
        if job_type is not None and job_type == 'Pending':
            color = discord.Color.green()

        if job_type is not None and job_type == 'Approved':
            color = discord.Color.dark_grey()

        super().__init__(
            title=self.job_name,
            # description=self.description,
            color=color
        )
        
        user_roles = [f"**{str(role).replace('@', '')}**" if '@' not in f'**{role}**' else role for role in self.user_roles]
        job_roles = [f"**{str(role).replace('@', '')}**" if '@' not in f'**{role}**' else role for role in self.job_roles.split(',')]
        self.add_field(name="User", value=self.user)
        self.add_field(name="Job name", value=self.job_name)
        self.add_field(name="Start date", value=self.start_date)
        self.add_field(name="Job roles", value=', '.join(job_roles), inline=False)
        self.add_field(name="User roles", value=', '.join(user_roles), inline=False)
        
        self.add_field(name="Description", value=f"{self.data['description'][:300]}")