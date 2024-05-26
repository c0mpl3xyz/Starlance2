import discord
from discord import Embed

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
            print(job_data['roles'])
            self.add_field(name="Start date", value=job_data['start_date'])
            self.add_field(name="Duration", value=f"{job_data['duration']} days")
            self.add_field(name="End date", value=job_data['end_date'])
            self.add_field(name="Participation date", value=job_data['participation_date'])
            self.add_field(name="Job files", value=f"[Click Here]({job_data['upload_link']})")
            self.add_field(name="Roles", value=job_data['roles'].replace(',', ' '), inline=False)