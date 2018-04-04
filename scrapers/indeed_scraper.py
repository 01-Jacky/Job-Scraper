import time
import random
import os
import urllib
from datetime import datetime, timedelta

from tools.job import Job
import tools.downloader
import tools.parser
import tools.helpers

import boto3
import json         # for working with boto 3
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



def main():
    NUM_JOBS_CRAWLED = 1000           # 10 non-sponsored postings per page
    cumulative_cs_jobs = []
    cumulative_non_cs_jobs = []

    for k, i in enumerate(range(0,NUM_JOBS_CRAWLED, 10)):
        url = 'https://www.indeed.com/jobs?q=software+intern&l=United+States&sort=date&start=' + str(i)
        # url = 'https://www.indeed.com/jobs?q=computer+science+intern&l=United+States&sort=date&start=' + str(i)
        # url = 'https://www.indeed.com/joqqbs?q=software+intern&l=United+States&start=' + str(i)
        # url = 'https://www.indeed.com/jobs?q=computer+science+intern&l=United+States&start=' + str(i)
        # url = 'https://www.indeed.com/jobs?q=computer+science+intern&l=San+Francisco%2C+CA&radius=100&sort=date&start=' + str(i)

        print('Scraping page ' + str(k + 1))
        html = tools.downloader.get_html(url)
        cs_jobs, non_cs_jobs = tools.parser.parse_non_sponsored_jobs(html)
        cumulative_cs_jobs.extend(cs_jobs)
        cumulative_non_cs_jobs.extend(non_cs_jobs)
        time.sleep(random.uniform(0.5,1.5))

    for k, i in enumerate(range(0,NUM_JOBS_CRAWLED, 10)):
        url = 'https://www.indeed.com/jobs?q=computer+science+intern&l=United+States&sort=date&start=' + str(i)
        # url = 'https://www.indeed.com/jobs?q=software+intern&l=United+States&start=' + str(i)
        # url = 'https://www.indeed.com/jobs?q=computer+science+intern&l=United+States&start=' + str(i)
        # url = 'https://www.indeed.com/jobs?q=computer+science+intern&l=San+Francisco%2C+CA&radius=100&sort=date&start=' + str(i)

        print('Scraping page ' + str(k + 1))
        html = tools.downloader.get_html(url)
        cs_jobs, non_cs_jobs = tools.parser.parse_non_sponsored_jobs(html)
        cumulative_cs_jobs.extend(cs_jobs)
        cumulative_non_cs_jobs.extend(non_cs_jobs)
        time.sleep(random.uniform(0.5,1.5))

    # Save jobs to disc
    if not os.path.exists('data_dump'):
        os.makedirs('data_dump')

    picke_name = "data_dump/jobs_{}.p".format(datetime.today().strftime('%Y-%m-%d_%H%M'))
    # pickle.dump(cumulative_cs_jobs, open(picke_name, "wb" ))
    # print_jobs(cumulative_cs_jobs)


    # Save job to db TODO: put these away in a db layer
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="https://dynamodb.us-west-2.amazonaws.com")
    table = dynamodb.Table('JobInternships')
    exist_count = 0
    insert_count = 0
    inserted_jobs = []

    for job in cumulative_cs_jobs:
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
                today_plus_ttl = today_date_time + timedelta(days=14)

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
                        'expiration_epoch': int(today_plus_ttl.timestamp())     # this allow us to setup automatic TTL in dynamodb
                    }
                )

                inserted_jobs.append(job) # Keep track of what was inserted
            # print(json.dumps(response, indent=4, cls=DecimalEncoder))

    # print to console for summary

    print('filtered out non cs jobs...')
    print_jobs(cumulative_non_cs_jobs)

    print('\nJob inserted to db...')
    print_jobs(inserted_jobs)

    print("dups: {}".format(exist_count))
    print("inserted: {}".format(insert_count))


if __name__ == '__main__':
    try:
        main()
    except urllib.error.URLError as e:
        print('Error downloading: ' + e.message)
