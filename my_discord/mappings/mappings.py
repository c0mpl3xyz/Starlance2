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
        'roles': data[3],
        'budget': data[4],
        'start_date': convert_date(data[5]),
        'duration': data[6],
        'end_date': convert_date(data[7]),
        'participation_date': convert_date(data[8]),
        'description': data[9],
        'upload_link': data[10],
        'requirements': data[11],
        'job_type': data[12],
        'user_count': data[13],
        'type': data[14],
    }

    return job_dict

def job_mapping(data: list) -> dict:
    job_dict = {
        'job_id': data[0],
        'discord_server_id': data[1],
        'name': data[2],
        'roles': data[3],
        'budget': data[4],
        'start_date': convert_date(data[5]),
        'duration': data[6],
        'end_date': convert_date(data[7]),
        'participation_date': convert_date(data[8]),
        'description': data[9],
        'upload_link': data[10],
        'requirements': data[11],
        'job_type': data[12],
        'user_count': data[13]
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