from enum import Enum
from dotenv import load_dotenv
import os
load_dotenv()

UGC_ID = os.getenv('UGC_ID')
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
    GUILD_ID = UGC_ID
    # GUILD_ID = 617630064653238272