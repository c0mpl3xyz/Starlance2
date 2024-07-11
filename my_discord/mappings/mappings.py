from datetime import datetime

def convert_date(date: str) -> str:
    format_string = '%a, %d %b %Y %H:%M:%S %Z'
    date_time = datetime.strptime(date, format_string)

    return date_time.strftime('%Y/%m/%d')

def job_mapping_with_type(data: list) -> dict:
    job_dict = {
        'job_id': data[0],
        'discord_server_id': data[1],
        'name': data[2],
        'server_name': data[3],
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
        'point': data[15],
        'type': data[16],
    }

    return job_dict

def job_mapping(data: list) -> dict:
    job_dict = {
        'job_id': data[0],
        'discord_server_id': data[1],
        'name': data[2],
        'server_name': data[3],
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
        'point': data[15],
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

def user_mappings(data: list):
    user_dict = {
        'user_id': data[0],
        'total_points': data[1],
        'points': data[2],
        'bank_name': data[3],
        'bank_number': data[4],
        'register': data[5]
    }

    return user_dict

def review_mapping(data: list):
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

def content_mapping(data: list):
    content_dict = {
        'id': data[0],
        'job_register_id': data[1],
        'job_id': data[2],
        'user_id': data[3],
        'server_id': data[4],
        'review_id': data[5],
        'link': data[6],
        'type': data[7],

        'initial_plays': data[8],
        'total_plays': data[9],
        'likes': data[10],
        'replays': data[11],
        'saves': data[12],
        'shares': data[13],
        'comments': data[14],
        'account_reach': data[15],
        'total_interactions': data[16],
        'points': data[17],
        'engagement': data[18],
        'engagement_rate': data[19],
        'active': data[20]
    }

    return content_dict

def collect_mapping(data: list):
    collect_dict = {
        'collect_id': data[0],
        'user_id': data[1],
        'points': data[2],
        'point_100': data[3],
        'type': data[4],
    }

    return collect_dict