import urllib.request
import time
import pickle
import datetime
import random
from bs4 import BeautifulSoup


class Job:
    def __init__(self, title, company, location, date, url):
        self.title = title
        self.company = company
        self.location = location
        self.date = date
        self.url = 'https://www.indeed.com' + url

    def __str__(self):
        return '{:<40} {:<50} {:<40} {}'.format(self.company, self.title, self.location, self.date)


def get_html(url):
    """
    Returns the html of url or None if status code is not 200
    """
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Python Learning Program',
            'From': 'hklee310@gmail.com'
        }
    )
    resp = urllib.request.urlopen(req)

    if resp.code == 200:
        return resp.read()  # returns the html document
    else:
        return None


def get_job(node):
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

    return Job(job_title, company, location, date, url)

def get_non_sponsored_jobs(url):
    """ Return a list of Job object ecluding sponsored jobs """
    soup = BeautifulSoup(get_html(url), 'html.parser')
    soup.prettify()

    non_sponsored_result = []
    for r in soup.find_all('div', {'class': ['row', 'result']}):
        if r.find('span', {'class': 'sponsoredGray'}) is None:
            non_sponsored_result.append(r)

    jobs = []
    keywords = set(['software','developer','engineer','engineering'])
    for result in non_sponsored_result:
        job = get_job(result)

        found = False
        for keyword in keywords:
            if not found and 'intern' in job.title.lower() and keyword in job.title.lower():
                jobs.append(job)
                found = True

    return jobs


def print_jobs(jobs):
    jobs = sorted(jobs, key=lambda job : job.company.lower())
    jobs = sorted(jobs, key=lambda job : job.date.lower())
    jobs = sorted(jobs, key=lambda job : job.location.lower())

    for k, job in enumerate(jobs):
        print('{:<2}: {}'.format(k, job))
    print()


# Parse the soup
jobs = []
for k, i in enumerate(range(0,500, 10)):
    # url = 'https://www.indeed.com/jobs?q=software+intern&l=United+States&sort=date&start=' + str(i)
    url = 'https://www.indeed.com/jobs?q=computer+science+intern&l=United+States&sort=date&start=' + str(i)
    # url = 'https://www.indeed.com/jobs?q=computer+science+intern&l=San+Francisco%2C+CA&radius=100&sort=date&start=' + str(i)
    jobs.extend(get_non_sponsored_jobs(url))
    time.sleep(random.uniform(0.5,1.5))
    print('Parsing page ' + str(k+1))

picke_name = "data_dump/jobs_{}.p".format(datetime.datetime.today().strftime('%Y-%m-%d_%H%M'))
pickle.dump(jobs, open(picke_name, "wb" ))
print_jobs(jobs)

