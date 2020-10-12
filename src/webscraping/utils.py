"""
Initial webscraping functions.
GET request and BeautifulSoup parsing.
"""
import json
import numpy as np
import smtplib
import re
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string
from os.path import basename

from contextlib import closing
from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pandas as pd


def soupify(url):
    """Attempts to get the content at `url` by making an HTTP GET request. Then uses BeautifulSoup to parse the html.

    Arg:
        url: str
            Link to url to scrape information
        parser: str
            Bs4 parser type, see documentation for parser types. Defaults to 'html.parser'.
            https://www.crummy.com/software/BeautifulSoup/bs4/doc/
            
    Returns:
    If parsed html content, otherwise return None.
    
    The closing() function ensures that any network resources are freed when they go out of scope in that with block.
    Using closing() like that is good practice and helps to prevent fatal errors and network timeouts.
    """

    try:
        # Sending GET
        with closing(get(url, stream=True)) as resp:
            if check_response(resp):
                content = resp.content
                print('Successfully received {u}'.format(u=url))

                # Using BeautifulSoup to parse
                bs4_parse = BeautifulSoup(content, features="lxml")
                return bs4_parse

            else:
                print('Failed to receive {u}'.format(u=url))
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def check_response(resp):
    """Checks if the response is correct. Returns True if the response seems to be HTML, False otherwise.
    """
    # 'text/html;charset=utf-8' should be expected
    content_type = resp.headers['Content-Type'].lower()

    # Status_code == 200 means http status is OK
    return resp.status_code == 200 and content_type is not None and content_type.find('html') > -1


def convert_object_to_datetime(s):
    """Turning date from object to np.datetime64

    Arg:
        s (pd.Dataframe or pd.Series): Pass in dataframe if multi column process is needed

    Returns:
        pd.Series
        pd.DataFrame: All columns containing "date" (case in-sensitive) will be amended

    Note:
        This method can handle EITHER "/" or "-" date separators but not a combination of both.
        Users should check that there are no mixtures of separators if s is an array
    """

    def find_format(series):

        # Default separator
        sep = "/"

        if pd.Series(series).str.contains("-").all():
            sep = "-"

        x = pd.Series(series).str.split("/|-", expand=True).values

        try:
            x = x.astype(int)
            month_pattern = "%m"

        except ValueError:
            month_pattern = "%b"

        year_col, month_col, date_col = None, None, None

        for i in range(x.shape[-1]):
            if x[:, i].dtype != object:
                if all(x[:, i].astype(int) > 1000):
                    year_col = i
                elif all(x[:, i].astype(int) <= 12):
                    month_col = i
                elif all(x[:, i].astype(int) <= 31):
                    date_col = i
            else:
                # Only month can be string and must be in the middle
                date_col, month_col, year_col = 0, 1, 2
                break

        assert year_col is not None, "Cannot find year in date string"

        try:
            year_pattern = "%Y" if (x[:, year_col].astype(int) > 1000).all() else "%y"
        except (ValueError, TypeError, IndexError):
            # Last resort couldn't figure format out, let pandas do it
            return None

        def month_and_date(current_sep, m, d, mp):
            if m > d:
                return current_sep.join(["%d", f"{mp}"])
            else:
                return current_sep.join([f"{mp}", "%d"])

        if year_col == 0:
            if month_col is not None and date_col is not None:
                fmt = sep.join((year_pattern, month_and_date(sep, month_col, date_col, month_pattern)))
            else:
                fmt = sep.join([year_pattern, f"{month_pattern}", "%d"])  # default to non US style

        elif year_col == 2:
            if month_col is not None and date_col is not None:
                fmt = sep.join([month_and_date(sep, month_col, date_col, month_pattern), year_pattern])
            else:
                fmt = sep.join(["%d", f"{month_pattern, year_pattern}"])  # default to non US style

        else:
            raise ValueError("Year in the middle of date separators!")

        return fmt

    # This is an extremely fast approach to datetime parsing. Some dates are often repeated.
    # Rather than to re-parse these, we store all unique dates, parse them, and use a lookup to convert all dates.
    if isinstance(s, pd.DataFrame):
        out = s.copy(True)  # this is the bottleneck
        for column_name, column in out.iteritems():
            # Loop through all the columns passed in
            if "date" in column_name.lower():
                if column.dtype != "<M8[ns]" and ~column.isnull().all():
                    # If date is provided as a string then ignore and set to int
                    try:
                        col = column.astype(int)
                        out[column_name] = col
                    except:
                        # Find the date columns(case in-sensitive)
                        # If pandas cant find the format, ignore error and maintain input
                        u_dates = pd.to_datetime(column.unique(),
                                                 format=find_format(column.unique()),
                                                 errors="ignore")
                        dates = dict(zip(column.unique(), u_dates.tolist()))
                        out[column_name] = column.map(dates.get)
        return out

    else:
        if s.dtype == "<M8[ns]":
            return s
        # Get unique dates
        u_dates = pd.to_datetime(s.unique(), format=find_format(s.unique()))
        dates = dict(zip(s.unique(), u_dates.tolist()))
        return s.map(dates.get)


class EmailObject(object):
    """Initialise class with objects to be contained within email"""

    credentials = open(r"C:\Users\Dencan Gan\Credentials\credentials.json")
    email_config = json.load(credentials)["email"]

    def __init__(self, email_text=None, email_table=None, email_image=None, add_css=False):
        """
        Parameters
        ----------
        email_text: str
            Email text, include line break as "\n"
        email_table: np.array, pd.DataFrame, [list]
            tabled data to be included in email after text.
        email_image: str, [list]
            path to jpg files.
        add_css: bool
            Specify to add default css template over email, defaults to False

        """

        if email_table is None:
            pass
        # Multiple tables/data frames
        elif isinstance(email_table, list):
            pass
        elif isinstance(email_table, np.ndarray):
            email_table = [self._format_table(email_table)]
        elif isinstance(email_table, pd.DataFrame):
            email_table = [email_table]
        else:
            raise TypeError("Table must be numpy array or pandas data frame")

        if email_image is None:
            pass
        elif isinstance(email_image, str):
            pass
        elif isinstance(email_image, list):
            pass
        else:
            raise TypeError("email_image must be a path str or list of path strings")

        if add_css is True:
            # Default standard css (used from a27)
            css = '<style>p {font:13px arial; margin-bottom:4px}\
                    table {border-collapse:collapse; width: 850}\
                    table, td {text-align: right; border: 1px solid black; font:13px arial; padding-right:5px} \
                    th { text-align: middle; }</style>'

            self.email_text = css + '<body>{' + email_text + '}</body>'

        else:
            self.email_text = email_text

        self.email_table = email_table
        self.email_image = email_image

    @staticmethod
    def _format_table(tbl):
        """Test email tables and format into dataframes for html conversion"""
        if isinstance(tbl, np.ndarray):
            column_names = string.ascii_letters
            if tbl.shape[1] > column_names:
                raise ValueError("number of columns in array > 26, consider placing into DF with named columns")
            else:
                return pd.DataFrame(tbl, columns=string.ascii_letters[:tbl.shape[1]])

    def send_email(self, to_address, from_address=email_config["email_address"],
                   email_subject=None,
                   password=email_config["email_password"],
                   server=email_config["email_server"],
                   port=587,
                   content_type="html",
                   attach=None):
        """
        Parameters
        ----------
        to_address: str or list
            Recipient email address, can be multiple (list).
        from_address: str
            Sender, only one allowed.
        email_subject: str
            Self explanatory.
        password: str
            Self explanatory.
        server: str
            SMTP server.
        port: int
            SMTP port, defaults to 25.
        content_type: str
            Specify content type as html or plain, defaults to html.
        attach: str or list
            Path to attach files to email.

        Notes
        ------
        https://stackoverflow.com/questions/8856117/how-to-send-email-to-multiple-recipients-using-python-smtplib/2820386
        """

        # Join addresses if multiple
        if isinstance(to_address, list):
            to_address_msg = ", ".join(to_address)
        else:
            to_address_msg = to_address

        msg = MIMEMultipart()
        msg["Subject"] = email_subject
        msg["From"] = from_address
        msg["To"] = to_address_msg

        # --------------
        # Text and Table
        # --------------

        if self.email_table is None:
            msg_with_text = MIMEText(self.email_text, content_type)
            msg.attach(msg_with_text)

        else:
            email_text_append = self.email_text

            # Adding table after text
            for tbl in self.email_table:
                email_text_append += "<br>" + tbl.to_html()

            msg_with_text_and_table = MIMEText(email_text_append, content_type)
            msg.attach(msg_with_text_and_table)

        # -----
        # Image
        # -----

        if self.email_image is not None:
            for i, file in enumerate(self.email_image):
                fp = open(file, "rb")
                msg_image = MIMEImage(fp.read())
                fp.close()
                msg_image.add_header("Content-ID", "<image" + str(i) + ">")
                msg.attach(msg_image)

        # -----------
        # Attachment
        # -----------

        if attach is not None:
            if isinstance(attach, str):
                attach = list(attach)
            elif isinstance(attach, list):
                pass

            for file in attach:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(open(file, "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="' + basename(file) + '"')
                msg.attach(part)

        # Initialising server and logging in
        server = smtplib.SMTP(server, port)
        server.ehlo()
        server.starttls()

        try:
            server.login(from_address, password)

        except smtplib.SMTPException as e:
            if "No suitable authentication method found" in str(e):
                print("Authentication not required....")
            else:
                raise smtplib.SMTPException(str(e))

        # Sending email
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()
        print("Email sent to " + to_address_msg)

    @staticmethod
    def hyperlink(link):
        """Generating html string to hyperlink"""
        html_string = "<p><a href='" + link.replace("/", "\\") + "'>"
        html_string += link.replace("/", "\\") + "</a></p>"
        return html_string

    @staticmethod
    def strip_html_tags(x):
        return re.sub("<[^<]+?>", "", x)