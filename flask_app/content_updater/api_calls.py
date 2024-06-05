import requests, os, time
from dotenv import load_dotenv
load_dotenv()
URL = os.getenv('URL')
def get_jobs():
    result = requests.get(URL + 'job/open_jobs')
    # print(result.text)
    return result.json()

def get_contents_by_job_ids(job_ids):
    data = {
        'job_ids': job_ids
    }

    print(f'{URL=}')
    result = requests.get(URL + 'content/job_ids', json=data)
    print(f'{result.text}')
    return result.json()

def update_content(content_dict: dict):
    for k, v in content_dict.items():
        data = {
            'content_id': k,
            
        }
        requests.post(URL + '/content', json=data)

def content_updater():
    while True:
        try:
            jobs = get_jobs()
            job_ids = [job[0] for job in jobs]
            contents = get_contents_by_job_ids(job_ids)
            contents = [list((content[0], content[6])) for content in contents]

            if not len(contents):
                time.sleep()
            else:
                pass
        except Exception:
            pass


if __name__ == '__main__':
    print(URL)
    content_updater()