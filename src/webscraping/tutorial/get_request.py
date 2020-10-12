"""Basic GET request function to receive html content"""

import requests


def get_resp(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.

    Parameter
        url: str
            Link to url to scrape information
    Returns
        HTML raw content to be parsed with BeautifulSoup for readable HTML structure.
    """
    # We want to send a GET request which in turn will return a response of 200, which means the response is correct
    website_response = requests.get(url)

    # Inspect status code
    response_code = website_response.status_code
    print(response_code)

    # .content returns the GET request's HTML content
    website_html = website_response.content

    # It will look nonsensical for now as we need to parse it with BeautifulSoup
    return website_html