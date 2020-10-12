from googlesearch import search
from src.utils import soupify


def wiki_summariser(search_term=None, num_lines=5, randomise=False):
    """Displays first 5 lines of a wikipedia page

    Args:
        search_term (str): Key word to search.
        num_lines (int): Number of lines to display.
        randomise (bool): Gets random wikipedia article

    Returns:
        Prints output.
    """

    if randomise is True:
        soup = soupify("https://en.wikipedia.org/wiki/Special:Random")
        link = soup.find("link", rel="canonical")
        link = link["href"]

    else:
        wiki_page = list(search(query=search_term, domains=['https://en.wikipedia.org/'], tld="com", num=10, stop=3, pause=1))
        link = wiki_page[0]
        soup = soupify(link)

    article = []
    for x in (soup.select('p')):
        article.append(x.text)

    result = ''.join(article[:num_lines])

    return result + "\n" + link


if __name__ == '__main__':
    print(wiki_summariser(randomise=True))