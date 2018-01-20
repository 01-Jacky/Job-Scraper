# from bs4 import BeautifulSoup
# import logging
# from lib.job import Job
#
#
# def _get_job(node):
#     """
#     Returns a Job object given the html node representing the record
#     """
#     job_title = node.find('a', {'class': 'turnstileLink'}).text
#     job_title = ' '.join(job_title.split())
#
#     url = node.find('a', {'class': 'turnstileLink'})['href']
#
#     company = node.find('span', {'class': 'company'}).text
#     company = ' '.join(company.split())
#
#     location = node.find('span', {'class': 'location'}).text
#     location = ' '.join(location.split())
#
#     date = node.find('span', {'class': 'date'}).text
#     date = ' '.join(date.split())
#
#     return Job(job_title, company, location, date, url)
#
#
# def parse_non_sponsored_jobs(html):
#     """ Return a list of Job object ecluding sponsored jobs """
#     soup = BeautifulSoup(html, 'html.parser')
#     soup.prettify()
#
#     non_sponsored_result = []
#     for r in soup.find_all('div', {'class': ['row', 'result']}):
#         if r.find('span', {'class': 'sponsoredGray'}) is None:
#             non_sponsored_result.append(r)
#
#     jobs = []
#     keywords = set(['software','developer','engineer','engineering'])
#     for result in non_sponsored_result:
#         try:
#             job = _get_job(result)
#         except Exception as e:
#             logging.exception(e)
#             continue
#
#         found = False
#         for keyword in keywords:
#             if not found and 'intern' in job.title.lower() and keyword in job.title.lower():
#                 jobs.append(job)
#                 found = True
#     return jobs

import logging
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from lib.job import Job


JOB_TITLE_KEYWORDS = [
    'software','developer','engineer','engineering','technical', 'technology'
]


def _convert_to_date(date_string):
    """
    Returns the date based on today and the 'x days ago' string
    e.g. if today is 2017-12-20, then _convert_to_date('1 days ago') returns the datetime 12-15-2017
    """

    DATE_FORMAT = '%Y-%m-%d'
    if date_string.lower() in ['just posted', 'today']:
        return datetime.today().strftime(DATE_FORMAT)
    elif date_string.lower() == '30+ days ago':
        return date_string.lower()
    else:
        # else we need to convert 'x days ago' ago into a date
        days_ago = date_string.split(" ")[0]
        d = datetime.today() - timedelta(days=int(days_ago))
        return d.strftime(DATE_FORMAT)

def _get_job(node):
    """
    Returns a Job object given the html node representing the record
    """
    job_title = node.find('a', {'class': 'turnstileLink'}).text
    job_title = ' '.join(job_title.split())

    url = node.find('a', {'class': 'turnstileLink'})['href']

    company = node.find('span', {'class': 'company'}).text
    company = ' '.join(company.split())

    location = node.find('span', {'class': 'location'}).text
    location = ' '.join(location.split())

    date = node.find('span', {'class': 'date'}).text
    date = ' '.join(date.split())
    date = _convert_to_date(date)

    return Job(job_title, company, location, date, url)


def parse_non_sponsored_jobs(html):
    """ Return a list of Job object ecluding sponsored jobs """
    soup = BeautifulSoup(html, 'html.parser')
    soup.prettify()

    # Get non-sponsor results
    divs_non_sponsored_result = []
    for r in soup.find_all('div', {'class': ['row', 'result']}):
        if r.find('span', {'class': 'sponsoredGray'}) is None:
            divs_non_sponsored_result.append(r)

    jobs = []
    keywords = set(JOB_TITLE_KEYWORDS)                  # Only return jobs with title containing one of these keywords
    for result_div in divs_non_sponsored_result:
        try:
            job = _get_job(result_div)
        except Exception as e:
            logging.exception(e)
            continue

        if job.date == '30+ days ago':
            continue

        found = False
        for keyword in keywords:
            if not found and 'intern' in job.title.lower() and keyword in job.title.lower():
                jobs.append(job)
                found = True
    return jobs

if __name__ == '__main__':
    print(_convert_to_date('today'))