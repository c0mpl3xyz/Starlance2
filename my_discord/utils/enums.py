from enum import Enum
from dotenv import load_dotenv
import os
load_dotenv()

UGC_ID = os.getenv('UGC_ID')
ALL_ROLES = os.getenv('ALL_ROLES')
class Enums(Enum):
    BANK_NAMES = ['Golomt', 'Khaan', 'Turiin', 'TDB', 'Khas']
    # SOCIAL_ACCOUNTS = ['Instagram', 'Facebook', 'TikTok', 'Youtube']
    SOCIAL_ACCOUNTS = ['Instagram', 'Youtube']
    APPROVE_GUILD = 'approve-influencer'
    NOTIFICATION = 'notification'
    CONTENT = 'contents'
    COLLECT = 'collect-points'
    REVIEW = 'review-video'
    JOB = 'jobs'

    MESSAGE_ROLES = ["Support staff", "Server booster", "Beginner", "Intermediate", "Advanced", "Premium", "Entertainment premium", "Education premium", "Other's premium", "Gaming premium", "Influencer premium", "Video edit premium", "Influencer", "Facebook influencer", "Instagram influencer", "Tiktok influencer", "Youtube influencer", "1-1k followers", "1k-5k followers", "5-10k followers", "10-50k followers", "Audience"]
    #TODO: add rejected message to influencer change guild id
    GUILD_ID = int(UGC_ID)
    ROLES = ALL_ROLES
    ADMIN = 'ADMIN'
    OUR_COMPANY = 1240963394467790938