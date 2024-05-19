registerd_jobs = [[4, None], [5, None], [6, None], [7, None], [18, 'Pending']]


jobs = []
for job_id, type in registerd_jobs:
    raw_job = []
    if raw_job is not None:
        job = list(raw_job)
        job.append(type)
        jobs.append(job)

print(jobs)