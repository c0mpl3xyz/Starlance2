from datetime import datetime

def convert_date(date: str) -> str:
    format_string = '%a, %d %b %Y %H:%M:%S %Z'
    date_time = datetime.strptime(date, format_string)

    return date_time.strftime('%Y/%m/%d')

def job_mapping_with_type(data: list) -> dict:
    job_dict = {
        'job_id': data[0],
        'discord_server_id': data[1],
        'server_name': data[2],
        'name': data[3],
        'roles': data[4],
        'budget': data[5],
        'start_date': convert_date(data[6]),
        'duration': data[7],
        'end_date': convert_date(data[8]),
        'participation_date': convert_date(data[9]),
        'description': data[10],
        'upload_link': data[11],
        'requirements': data[12],
        'job_type': data[13],
        'user_count': data[14],
        'type': data[15],
    }

    return job_dict

def job_mapping(data: list) -> dict:
    job_dict = {
        'job_id': data[0],
        'discord_server_id': data[1],
        'server_name': data[2],
        'name': data[3],
        'roles': data[4],
        'budget': data[5],
        'start_date': convert_date(data[6]),
        'duration': data[7],
        'end_date': convert_date(data[8]),
        'participation_date': convert_date(data[9]),
        'description': data[10],
        'upload_link': data[11],
        'requirements': data[12],
        'job_type': data[13],
        'user_count': data[14]
    }

    return job_dict

def job_register_mapping(data: list):
    job_register_dict = {
        'id': data[0],
        'user_id': data[1],
        'job_id': data[2],
        'type': data[3]
    }

    return job_register_dict

def review_mappings(data: list):
    review_dict = {
        'id': data[0],
        'job_register_id': data[1],
        'job_id': data[2],
        'job_name': data[3],
        'job_description': data[4],
        'user_id': data[5],
        'server_id': data[6],
        'server_name': data[7],
        'link': data[8],
        'description': data[9],
        'type': data[10]
    }

    return review_dict

def content_mappings(data: list):
    content_dict = {
        'id': data[0],
        'job_register_id': data[1],
        'job_id': data[2],
        'user_id': data[3],
        'server_id': data[4],
        'review_id': data[5],
        'link': data[6],
        'type': data[7],
        'point': data[8],
        'initial_plays': data[9],
        'plays': data[10],
        'likes': data[11],
        'replays': data[12],
        'saves': data[13],
        'shares': data[14],
        'comments': data[15],
        'percent_followers': data[16],
        'percent_non_followers': data[17],
        'active': data[18],

    }

    return content_dict