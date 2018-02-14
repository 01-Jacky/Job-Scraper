import logging
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from tools.job import Job

JOB_TITLE_KEYWORDS = [
    'software','developer','engineer','engineering','technical', 'technology'
]

JOB_TITLE_EXCLUDE_KEYWORDS = [
    'civil', 'electrical', 'mechanical', 'manufacturing'
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

    job_count_with_keyword = 0

    for result_div in divs_non_sponsored_result:
        try:
            job = _get_job(result_div)
        except Exception as e:
            logging.exception(e)
            continue

        # ignore job if...
        if job.date == '30+ days ago':
            continue

        # include only if it has keywords...
        found = False
        for keyword in keywords:
            if not found and 'intern' in job.title.lower() and keyword in job.title.lower():
                jobs.append(job)
                job_count_with_keyword += 1
                found = True

    # ignore certain keywords
    cs_jobs = []
    non_cs_jobs = []
    for job in jobs:
        is_cs_job = True

        # If we found excluded keyword put it in a different list
        for exclude_keyword in JOB_TITLE_EXCLUDE_KEYWORDS:
            if exclude_keyword in job.title.lower():
                non_cs_jobs.append(job)
                is_cs_job = False
                break

        if is_cs_job:
            cs_jobs.append(job)     # didn't find exlucded keywords

    return cs_jobs, non_cs_jobs

if __name__ == '__main__':
    print(_convert_to_date('today'))