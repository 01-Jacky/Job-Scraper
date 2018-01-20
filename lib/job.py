class Job:
    def __init__(self, title, company, location, date, url):
        self.title = title
        self.company = company
        self.location = location
        self.date = date
        self.url = 'https://www.indeed.com' + url

    def __str__(self):
        google_link = 'https://www.google.com/search?q={}'.format('+'.join(self.company.split() + ["intern", "salary"]))
        return '{:<35} {:<50} {:<35} {:<15} {:<70} {}'.format(
            self.company, self.title[:45], self.location[:30], self.date, google_link, self.url)
