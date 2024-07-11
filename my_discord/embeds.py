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

class CollectedMessageEmbed(Embed):
    def __init__(self, points, bank_name, bank_number):
        super().__init__(
            title='Collect request approved',
            color = discord.Color.green()
            )
        
        tax = round(points * 0.25, 2)
        income = round(points - tax, 2)
        self.add_field(name="Message", value='**Please check your bank account!**', inline=False)
        self.add_field(name="Collected Points", value=points)
        self.add_field(name="Total ₮", value=f'{format(points * 10, ",")} ₮')
        self.add_field(name="Tax ₮", value=f'{format(tax * 10, ",")} ₮')
        self.add_field(name="Income ₮", value=f'{format(income * 10, ",")} ₮')

        if bank_number is not None:
            bank_number = '-'.join([bank_number[i:i+3] for i in range(0, len(bank_number), 3)])
        self.add_field(name="Bank name", value=bank_name)
        self.add_field(name="Bank account", value=bank_number)

class UserEmbed(Embed):
     def __init__(self, user_data):
        super().__init__(
            title='User Status',
            color = discord.Color.random()
            )
        points = user_data['points']
        col_points = 0

        if (points - 20000) * 0.75 // 10000 * 10000:
            col_points = (points - 20000) * 0.75 // 10000 * 10000

        tugrik = col_points * 10
        tax = round(tugrik * 0.25, 2)
        collectable = tugrik - tax
        self.add_field(name='User', value=f'<@{user_data["user_id"]}>', inline=False)
        self.add_field(name="Total Points Of Lifetime", value=user_data['total_points'])
        self.add_field(name="Available Points", value=format(user_data['points'], ','))
        self.add_field(name="Collectable Points", value=f'{format(points - 20000, ",")} ₮')
        self.add_field(name="Total ₮", value=f'{format(tugrik, ",")} ₮')
        self.add_field(name="Tax ₮", value=f'{format(tax, ",")} ₮')
        self.add_field(name="Income ₮", value=f'{format(collectable, ",")} ₮')
        self.add_field(name="Register Number", value=user_data['register'])
        self.add_field(name="Bank Name", value=user_data['bank_name'])
        bank_number = None
        if user_data['bank_number'] is not None:
            bank_number = '-'.join([user_data['bank_number'][i:i+3] for i in range(0, len(user_data['bank_number']), 3)])
        self.add_field(name="Bank Number", value=bank_number)

class CollectEmbed(Embed):
     def __init__(self, user_data, points):
        super().__init__(
            title='User Status',
            color = discord.Color.random()
            )
        
        tugrik = round(points * 10, 2)
        tax = round(tugrik * 0.25, 1)
        collectable = round(tugrik - tax)
        bank_number = None
        if user_data['bank_number'] is not None:
            bank_number = '-'.join([user_data['bank_number'][i:i+3] for i in range(0, len(user_data['bank_number']), 3)])

        self.add_field(name='User', value=f'<@{user_data["user_id"]}>', inline=False)
        self.add_field(name="Register Number", value=user_data['register'])
        self.add_field(name="Bank Name", value=user_data['bank_name'])
        self.add_field(name="Bank Number", value=bank_number)
        self.add_field(name="Collect points", value=format(points, ','))
        self.add_field(name="Total ₮", value=f'{format(tugrik, ",")} ₮')
        self.add_field(name="Tax ₮", value=f'{format(tax, ",")} ₮')
        self.add_field(name="Collectable ₮", value=f'{format(collectable, ",")} ₮') 

class ReviewEmbed(Embed):
     def __init__(self, data: dict):
        self.data = data
        super().__init__(
            title=data['server_name'],
            # description=data['job_description'],
            color = discord.Color.random()
            )
        self.add_field(name='Job Name', value=data['job_name'])
        self.add_field(name='User', value=f'<@{data["user_id"]}>')
        self.add_field(name='Job Description', value=f'{data["job_description"][:300]}', inline=False)
        self.add_field(name="Message", value=data['description'][:1000], inline=False)
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
            title=f"{review_data['server_name']} - {str(content_data['type']).capitalize()} Content",
            color = color
            )
        
        removed_replays = content_data['total_plays'] - content_data['initial_plays'] - content_data['replays']
        self.add_field(name='Job Name', value=review_data['job_name'], inline=False)
        self.add_field(name='User', value=f'<@{content_data["user_id"]}>')
        self.add_field(name='Content Link', value=content_data['link'], inline=False)
        self.add_field(name='Total Views', value=format(content_data['total_plays'], ','))
        self.add_field(name='Initial Plays', value=format(content_data['initial_plays'], ','))
        self.add_field(name='Replays', value=format(content_data['replays'], ','))
        self.add_field(name='Removed Replays', value=format(removed_replays, ','))
        self.add_field(name='Likes', value=format(content_data['likes'], ','))
        self.add_field(name='Saves', value=format(content_data['saves'], ','))
        self.add_field(name='Shares', value=format(content_data['shares'], ','))
        self.add_field(name='Comments', value=format(content_data['comments'], ','))
        self.add_field(name='Account Reached', value=format(content_data['account_reach'], ','))
        self.add_field(name='Total Interaction', value=format(content_data['total_interactions'], ','))
        self.add_field(name='Engagement Rate', value=content_data['engagement_rate'])
        self.add_field(name='Active', value=content_data['active'])
        self.add_field(name='Total Points', value=format(content_data['points'], ','))

class JobEmbed(Embed):
    def __init__(self, job_data, contents, company):
        color = None
        if 'job_type' not in job_data:
            job_data['job_type'] = 'Open'

        if job_data['job_type'] == 'Open':
            color = discord.Color.green()
        elif job_data['job_type'] == 'Closed':
            color = discord.Color.yellow()
        elif job_data['job_type'] == 'Ended':
            color = discord.Color.red()

        super().__init__(
            title=job_data['server_name'],
            description=f'{job_data["description"]}',
            color=color
        )

        self.add_field(name="Job name", value=job_data['name'], inline=False)
        self.add_field(name="Roles", value=job_data['roles'].replace(',', ' '), inline=False)
        self.add_field(name="Start date", value=f"{job_data['start_date']} Days")
        self.add_field(name="Duration", value=f"{job_data['duration']} days")
        self.add_field(name="End date", value=job_data['end_date'])
        self.add_field(name="Participation date", value=job_data['participation_date'])
        self.add_field(name="Total Budget", value=str(format(job_data['budget'], ',')) + ' ₮')
        self.add_field(name="Job files", value=f"[Click Here]({job_data['upload_link']})")
        self.add_field(name="1 View Point", value=job_data['point'])
        self.add_field(name="Points of Job", value=str(format(job_data['budget'] / job_data['point'], ',')))
        self.add_field(name="\u200B", value="__\u200B__")

        if company and len(contents):
                self.add_field(name="\u200B", value="__\u200B__", inline=False)
                self.add_field(name="Content Count", value=len(contents))
                content_data = self.get_status(contents)
                removed_replays = content_data['views'] - content_data['initial_plays'] - content_data['replays']
                self.add_field(name="Views", value=format(content_data['views'], ','))
                self.add_field(name="Initial Plays", value=format(content_data['initial_plays'], ','))
                self.add_field(name="Replays ", value=format(content_data['replays'], ','))
                self.add_field(name='Removed Replays', value=format(removed_replays, ','))
                self.add_field(name="Likes", value=format(content_data['likes'], ','))
                self.add_field(name="Saves", value=format(content_data['saves'], ','))
                self.add_field(name="Shares", value=format(content_data['shares'], ','))
                self.add_field(name="Comments", value=format(content_data['comments'], ','))
                self.add_field(name="Account Reach", value=format(content_data['account_reach'], ','))
                self.add_field(name="Average Engagement Rate", value=round(content_data['engagement_rate'], 2))
                self.add_field(name="Points", value=format(content_data['points'], ','))
        
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

        data['engagement_rate'] = round(data['engagement_rate'] / len(contents), 2)

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