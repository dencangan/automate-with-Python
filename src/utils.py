"""
Generic utils for emails, parsing, etc.
"""

import json, csv
import os
import glob
import pandas as pd
import numpy as np
import smtplib
import string
from os.path import basename
import re
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src import get_config_path


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

            self.email_text = css + '<p>' + email_text + '</p>'

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


def read_json_config(cfg_file):
    """Function to quickly read json from config directory"""
    # Read config
    config_path = get_config_path(cfg_file)
    cfg = open(config_path)
    return json.load(cfg)


def get_latest_modified_file(folder_dir, file_type=''):

    """
    Parameters
    ----------
        folder_dir: str
            Folder directory
        file_type
            Specify file format if needed, defaults to empty string.
            Examples of acceptable types: .csv, .xlsx, etc.

    Returns
    -------
        latest_file: str
            Gets name of latest file in directory
    """

    list_of_files = glob.glob(folder_dir + '/*' + file_type)
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


def csv_to_json(csv_crypto_dir, json_crypto_dir):
    """Converts csv to json files for mongoDB storage

    """

    data = {}
    with open(csv_crypto_dir) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for rows in csv_reader:
            date = rows['Date']
            data[date] = rows

    with open(json_crypto_dir, 'w') as json_file:
        json_file.write(json.dumps(data, indent=4))
