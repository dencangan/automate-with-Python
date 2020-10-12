from src.utils import EmailObject
from src.quotes import get_quote
from src.wiki_search import wiki_summariser
from datetime import datetime


def morning_email(quotes_to_scrape=5):
    quote = get_quote(num_of_quotes=quotes_to_scrape)
    wiki = wiki_summariser(randomise=True)
    body = f"Quote of the day:<br><br>{quote} <br><br><br>Wikipedia article of the day:<br><br>{wiki}"
    daily_email = EmailObject(email_text=body, add_css=True)
    daily_email.send_email(to_address="", email_subject= datetime.today().strftime("%A") + ", " +
                                                         datetime.today().strftime("%d %B %Y") + ": Hang in there!")