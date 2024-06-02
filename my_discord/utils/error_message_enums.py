from enum import Enum

class ErrorMessageEnum(Enum):
    NOT_INFLUENCER = 'You are not influencer, Permission denied'
    NOT_COMPANY = 'You are not a company, Permission denied'
    NOT_DM = 'Use this command from Discord server'
    NO_JOB =  'You have no jobs registered'
    NO_REVIEWS =  'You have no reviews registered'
    NO_JOB_ROLES = 'There is no new jobs on your roles yet'
    NO_CONTENT = 'There is no contents'

class MessageEnum(Enum):
    SUCCESS = 'Command successfully executed'