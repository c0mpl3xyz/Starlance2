from enum import Enum
from dotenv import load_dotenv
import os
load_dotenv()

class Enums(Enum):
    BANK_NAMES = ['Golomt', 'Khaan', 'Turiin', 'TDB', 'Khas']
    # SOCIAL_ACCOUNTS = ['Instagram', 'Facebook', 'TikTok', 'Youtube']
    SOCIAL_ACCOUNTS = ['Instagram']
    APPROVE_GUILD = 'approve-influencer'
    NOTIFICATION = 'notification'
    CONTENT = 'contents'
    COLLECT = 'collect-points'
    REVIEW = 'review-video'
    JOB = 'jobs'

    # TODO: change guild id
    GUILD_ID = 1212987222400307280
    # GUILD_ID = 617630064653238272