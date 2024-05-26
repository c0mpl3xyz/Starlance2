from datetime import datetime

def convert_date(date: str) -> str:
    format_string = '%a, %d %b %Y %H:%M:%S %Z'
    date_time = datetime.strptime(date, format_string)

    return date_time.strftime('%Y/%m/%d')

def job_mapping_with_type(data: list) -> dict:
    job_dict = {
        'job_id': data[0],
        'server_id': data[1],
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
        'type': data[12]
    }

    return job_dict

def job_mapping(data: list) -> dict:
    job_dict = {
        'job_id': data[0],
        'server_id': data[1],
        'name': data[2],
        'roles': data[3],
        'budget': data[4],
        'start_date': convert_date(data[5]),
        'duration': data[6],
        'end_date': convert_date(data[7]),
        'participation_date': convert_date(data[8]),
        'description': data[9],
        'upload_link': data[10],
        'requirements': data[11]
    }

    return job_dict