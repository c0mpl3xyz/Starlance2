from instagram.api_calls import *
from instagram.pro_ig_token import ProIGToken

def content_updater():
    try:
        jobs = get_jobs()
        job_ids = [job[0] for job in jobs]
        contents = get_contents_by_job_ids(job_ids)
        contents_dict = {get_shortcode(content[6]): content[0] for content in contents if get_shortcode(content[6]) is not None}

        print(f'{contents_dict=}')
        ig_token = ProIGToken()
        result = ig_token.filter_by_shortcodes(contents_dict)
        for k, v in result.items():
            v['content_id'] = k
            update_content(v)
            pass
        
    except Exception as e:
        raise e


if __name__ == '__main__':
    print(content_updater())