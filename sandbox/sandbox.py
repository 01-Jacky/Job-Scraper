jobs = ['civil engineer intern', 'mechanical intern', 'cs intern', 'electrical intern']

JOB_TITLE_KEYWORDS = [
    'software','developer','engineer','engineering','technical', 'technology'
]

JOB_TITLE_EXCLUDE_KEYWORDS = [
    'civil', 'electrical', 'mechanical'
]

cs_jobs = []
non_cs_jobs = []

for job in jobs:
    is_cs_job = True

    # If we found excluded keyword put it in a different list
    for exclude_keyword in JOB_TITLE_EXCLUDE_KEYWORDS:
        if exclude_keyword in job.lower():
            non_cs_jobs.append(job)
            is_cs_job = False
            break

    if is_cs_job:
        cs_jobs.append(job)  # didn't find exlucded keywords

print(cs_jobs)