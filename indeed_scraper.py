import time
import pickle
import random
import os
from datetime import datetime, timedelta

from lib.job import Job
import lib.downloader
import lib.parser
import lib.helpers

# boto3
import boto3
import json
import decimal
from botocore.exceptions import ClientError

# TODO - log out scrapped from which keyword.

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def print_jobs(jobs):
    jobs = sorted(jobs, key=lambda job : job.company.lower())
    jobs = sorted(jobs, key=lambda job : job.date.lower())
    jobs = sorted(jobs, key=lambda job : job.location.lower())

    for k, job in enumerate(jobs):
        print('{:<2}: {}'.format(k, job))
    print()


# Parse the soup
if __name__ == '__main__':
    NUM_JOBS_CRAWLED = 30           # 10 non-sponsored postings per page
    for k, i in enumerate(range(0,NUM_JOBS_CRAWLED, 10)):
        url = 'https://www.indeed.com/jobs?q=software+intern&l=United+States&sort=date&start=' + str(i)
        # url = 'https://www.indeed.com/jobs?q=computer+science+intern&l=United+States&sort=date&start=' + str(i)
        # url = 'https://www.indeed.com/joqqbs?q=software+intern&l=United+States&start=' + str(i)
        # url = 'https://www.indeed.com/jobs?q=computer+science+intern&l=United+States&start=' + str(i)
        # url = 'https://www.indeed.com/jobs?q=computer+science+intern&l=San+Francisco%2C+CA&radius=100&sort=date&start=' + str(i)

        print('Scraping page ' + str(k + 1))
        html = lib.downloader.get_html(url)
        jobs.extend(lib.parser.parse_non_sponsored_jobs(html))
        time.sleep(random.uniform(0.5,1.5))

    for k, i in enumerate(range(0,NUM_JOBS_CRAWLED, 10)):
        # url = 'https://www.indeed.com/jobs?q=software+intern&l=United+States&sort=date&start=' + str(i)
        url = 'https://www.indeed.com/jobs?q=computer+science+intern&l=United+States&sort=date&start=' + str(i)
        # url = 'https://www.indeed.com/jobs?q=software+intern&l=United+States&start=' + str(i)
        # url = 'https://www.indeed.com/jobs?q=computer+science+intern&l=United+States&start=' + str(i)
        # url = 'https://www.indeed.com/jobs?q=computer+science+intern&l=San+Francisco%2C+CA&radius=100&sort=date&start=' + str(i)

        print('Scraping page ' + str(k + 1))
        html = lib.downloader.get_html(url)
        jobs.extend(lib.parser.parse_non_sponsored_jobs(html))
        time.sleep(random.uniform(0.5,1.5))

    # Save jobs to disc
    if not os.path.exists('data_dump'):
        os.makedirs('data_dump')

    picke_name = "data_dump/jobs_{}.p".format(datetime.today().strftime('%Y-%m-%d_%H%M'))
    pickle.dump(jobs, open(picke_name, "wb" ))
    print_jobs(jobs)


    # Save job to db TODO: put these away in a db layer
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")
    table = dynamodb.Table('JobInternships')
    exist_count = 0
    insert_count = 0
    inserted_jobs = []

    for job in jobs:
        jobid = job.company.replace(' ', '') + '_' + job.title.replace(' ','')

        try:
            response = table.get_item(
                Key={
                    'date': job.date,
                    'jobID': jobid,
                }
            )

            DATE_FORMAT = '%Y-%m-%d'
            base_date = datetime.strptime(job.date, DATE_FORMAT)
            date_1_before = base_date - timedelta(days=int(1))
            date_1_before = date_1_before.strftime(DATE_FORMAT)

            response2 = table.get_item(
                Key={
                    'date': date_1_before,
                    'jobID': jobid,
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            if 'Item' in response or 'Item' in response2:                       # If item exist
                exist_count += 1
            else:                                                               # If not insert it
                insert_count += 1

                today_date_time = datetime.today()                     # Setup creation/expiration times
                today_plus_30 = today_date_time + timedelta(days=30)

                response = table.put_item(
                    Item={
                        'date': job.date,
                        'jobID': jobid,
                        'company': job.company,
                        'title': job.title,
                        'location': job.location,
                        'url': job.url,
                        'source': 'Indeed',
                        'creation_epoch': int(today_date_time.timestamp()),
                        'expiration_epoch': int(today_plus_30.timestamp())     # this allow us to setup automatic TTL in dynamodb
                    }
                )

                inserted_jobs.append(job) # Keep track of what was inserted
            # print(json.dumps(response, indent=4, cls=DecimalEncoder))

    for job in sorted(inserted_jobs, key= lambda job: job.date):
        print(job)

    print("dups: {}".format(exist_count))
    print("inserted: {}".format(insert_count))




