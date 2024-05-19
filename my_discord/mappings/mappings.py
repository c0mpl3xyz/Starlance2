from datetime import datetime

def convert_date(date: str) -> str:
    format_string = '%a, %d %b %Y %H:%M:%S %Z'
    date_time = datetime.strptime(date, format_string)

    return date_time.strftime('%Y/%m/%d')

def job_mapping(data: list) -> dict:
    job_dict = {
        'name': data[2],
        'roles': data[3],
        'start_date': convert_date(data[4]),
        'duration': data[5],
        'end_date': convert_date(data[6]),
        'participation_date': convert_date(data[7]),
        'description': data[8],
        'upload_link': data[9],
        'requirements': data[10],
        'type': data[11]
    }

    return job_dict