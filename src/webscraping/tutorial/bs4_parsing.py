"""Navigating through HTML with BeautifulSoup"""

from tutorial.get_request import get_resp
from bs4 import BeautifulSoup


def bs_parse(parser):

    """
    Using BeautifulSoup to soupify (parse) html content received after successful GET request.

    Parameter
    ---------
        parser: str
            Input parser type (ie. html.parser, lxml, lxml-xml, xml, html5lib). All parsers have their own advantages
            and disadvantages. See here: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser

    Return
    ------
        Parsed html content to readable html structure and format.
    """

    html_raw = get_resp(url='https://www.bbc.co.uk/news')

    # Enter Beautiful Soup parsing, parser defined
    html_soup = BeautifulSoup(html_raw, parser)
    return html_soup


if __name__ == '__main__':

    soup = bs_parse(parser='html_parser')
    print(soup)

    for child in soup.ul.children:
        print(child)

    for parent in soup.li.parents:
        print(parent)

    # You can get the name of a HTML tag by typing the tag as a method
    # Note this will only return the FIRST tag bs4 will find.
    find_div_tag = soup.div
    print(find_div_tag)

    # You can get the name of the tag using .name and a dictionary representing the attributes of the tag using .attrs:
    finding_div = soup.div.name
    print(finding_div)

    # Returns div attribute
    att_of_div = soup.div.attrs
    print(att_of_div)

    # NavigableStrings are the pieces of text that are within the HTML tags on the page.
    # You can get the string inside of the tag by calling .string
    str_div = soup.div.string
    print(str_div)
