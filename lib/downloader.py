import urllib.request


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
