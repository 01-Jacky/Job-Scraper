import urllib.request
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
    for result in non_sponsored_result:
        job = get_job(result)
        if 'intern' in job.title.lower():
            jobs.append(job)

    return jobs


def print_jobs(jobs):
    for k, job in enumerate(jobs):
        print('{}: {}'.format(k, job))
    print()

    for k, job in enumerate(jobs):
        print('{}: {}'.format(k, job.url))


# Parse the soup
i = 0
url = 'https://www.indeed.com/jobs?q=intern+computer+science&l=United+States&sort=date&start=' + str(i)

jobs = get_non_sponsored_jobs(url)
print_jobs(jobs)
