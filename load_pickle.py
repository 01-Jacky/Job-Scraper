# Load the dictionary back from the pickle file.
import pickle

jobs = pickle.load( open( "data_dump/jobs_2017-12-19_2258.p", "rb" ) )
jobs = sorted(jobs, key=lambda job : job.location.lower())
jobs = sorted(jobs, key=lambda job : job.company.lower())
# jobs = sorted(jobs, key=lambda job : job.date.lower())

i = 1
for job in jobs:
    if job.date != '30+ days ago':
        print('{:<2}: {}'.format(i, job))
        i += 1
print()