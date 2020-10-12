# projects-in-Python
Projects written in Python out of interest. Currently there are 2 main projects:
* [Webscraping](#Webscraping-Project)
* [Automation with Python](#Automation-with-Python)

# Webscraping Project
This project is centered around the use of Python web scraping packages such as BeautifulSoup and Selenium. The repository contains a basic comprehensive web scraping tutorial as well as some of my personal side projects!

<p align="center">
  <br>
  <img height="400" width="800" src="img/internet-image.jpg">
  <br>
  <i>The internet is full of information.</i>
</p>


## Prerequisites
To get the below scripts to work, install the below packages.
* [requests](https://pypi.org/project/requests/)
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
* [Selenium](https://www.selenium.dev/documentation/en/)
* [google-search](https://pypi.org/project/google-search/)

## Scripts
- covid19 - Scrapes and uploads UK COVID19 data to mongodb, sends email of daily cases summary.
- wiki_search.py - Scrapes first few sentences of a specified search term from its wikipedia page for a quick summary.
- trading_view.py - Scrapes financial asset data (cryptos, stocks, currencies and indices) from [tradingview](https://uk.tradingview.com/).
- amazon_deals.py - Scrapes specified amazon products and returns current and previous prices.
- quotes.py - Scrapes for randomised quotes from [goodreads](https://www.goodreads.com/quotes).
- crypto_scrape.py - Scrapes from cryptocurrency data from [coinmarketcap](https://coinmarketcap.com/)

## Tutorial
The below section provides an introduction and basic tutorial for beginners interested at learning how to web scrape.

## Table of Contents
* [Introduction](#introduction)
* [Rules and Practice](#important-rules-and-practice-of-web-scraping)
* [Documentation](#documentation)
* [Set Up](#set-up)
* [BeautifulSoup Parsing](#beautifulsoup-parsing)
* [Scraping Data](#scraping-data)
* [Closing Remarks](#closing-remarks)

## Introduction
> "Web scraping, web harvesting, or web data extraction is data scraping used for extracting information from websites. It is a form of copying, in which specific data is gathered and copied from the web for later retrieval or analysis" - Wikipedia on [web scraping](https://en.wikipedia.org/wiki/Web_scraping)

Web scraping itself is *not illegal*. However, it is important to note about how scraped data is used.

Many web scraping legal issues are associated around scraping content and assuming ownership of that content, or scraping non-public data behind security walls.

The [legality](https://www.quora.com/What-is-the-legality-of-web-scraping) of web scraping prompts discussions around the question of 'Who enforces the rules of the internet?'. Hence, it is important to follow a few important general rules to remain on the right side of the law when web scraping.

I do not condone the act of scraping websites to malicious and abusive ends. This repository was created solely for educational purposes only.

## Important Rules and Practice of Web Scraping
- When scraping websites, it is important to follow guidelines to treat websites and their owners with respect.
- Always check the Terms and Conditions of the website. It is important to acknowledge the website's statement and stance on the legal use of their data.
- Avoid overloading a website with a ton of requests. A large number of requests can increase level of traffic that a website may not be able to handle.
- As a general rule of good practice, one request should be made to one webpage per second.


## Documentation
* [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Article on using DevTools](https://www.codecademy.com/articles/use-devtools)
* [HTML Status Codes](https://www.restapitutorial.com/httpstatuscodes.html)
* [HTML tags](https://www.w3schools.com/tags/)

## Set Up
Import required modules requests and BeautifulSoup. These are necessary modules required to scrape websites using Python.
```python
import requests
from bs4 import BeautifulSoup
```
* 'requests' is a python module used to communicate with web servers. It simplifies the process of sending HTTP/1.1 requests automatically without the need for encoding complicated query strings, etc.

* 'BeautifulSoup' is a Python library for pulling data out of HTML and XML files. It works with your favorite parser to provide idiomatic ways of navigating, searching, and modifying the parse tree.

Below is a basic function using the requests module to communicate with a website's server to retrieve its content.
```python
def get_resp(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.

    :parameter
        url: str
            Link to url to scrape information
    :returns
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
```
*get_request.py*

HTTP methods determine which action you’re trying to perform when making an HTTP request. GET is an example of a HTTP method. The GET method makes a request to a website server to retrieve data. To make a GET request, use requests.get()

Once a GET request is sent, a Response will be returned. Responses are useful for inspecting the results of the request.
Response come in status codes. By using .status_code, a status code informs you of the status of the request.

For example, the most common responses are:
* 200 OK status means that your request was successful, whereas a
* 404 NOT FOUND status means that the resource you were looking for was not found.

There are many other possible status codes as well to give you specific insights into what happened with your request, and this is useful when handling errors. Here is a comprehensive list of [status codes](https://www.restapitutorial.com/httpstatuscodes.html).

## BeautifulSoup Parsing
When the returned response is 200, we are ready to parse or 'soupify' the html content into understandable format.

"html.parser" is one of many parsers available. Other options include "lxml" and "html5lib" that have different use cases, advantages and disadvantages. Full break down of parser information can be found in the BeautifulSoup documentation [here](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser).
```python
def bs_parse(parser):

    """
    Using BeautifulSoup to soupify (parse) html content received after successful GET request.

    :parameter
        parser: str
            Input parser type (ie. html.parser, lxml, lxml-xml, xml, html5lib).

    :returns
        Parsed html content to readable html structure and format.
    """

    html_raw = get_resp(url='https://www.bbc.co.uk/news')

    html_soup = BeautifulSoup(html_raw, parser)
    return html_soup

if __name__ == '__main__':
    soup = bs_parse(parser='html_parser')
```
*bs4_parsing.py*

The print statement will return the full parsed html code behind the webpage. You can also do this by right clicking and selecting 'View Page Source' to reveal html code or use web developer tools to navigate through the html code easily. An article on using the web developer [tool]((https://www.codecademy.com/articles/use-devtools).

## Scraping Data
When web scraping, we want to extract *specifics* from a website. Hence, we need to know how we can navigate through a website's html easily to get the information we want.

BeautifulSoup creates objects such as Tags and NavigableStrings.
* Tags are the same as html [tags](https://www.w3schools.com/tags/), example 'id', 'div', 'head', etc.
* NavigableStrings are the pieces of text that are in the HTML tags on the page.

Let's look at the below html snippet example:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello World</title>
</head>
<body>
    <h1>Data Science</h1>
        <div class="main">
          <h1>Skills</h1>
        </div>
    <ul>
      <li>Data Analysis</li>
      <li>Machine Learning</li>
    </ul>
</body>
</html>
```
*example.html*

From bs4_parsing.py, object 'soup' is used to navigate through the html code. Let's use tag 'div' as an example.
```python
soup.div # Returns first <div> tag
soup.div.name # Returns 'div'
soup.div.attrs # Returns dictionary representing attributes of the tag
soup.div.string # Returns string inside of tag
```

Html is structured like branches on a tree, so navigating around it is important at selecting the data we are interested in. Using .parent and .children tags are useful to go 'up' or 'down' the html tree.
```python
for child in soup.ul.children:
    print(child)

<li>Data Analysis</li>
<li>Machine Learning</li>

for parent in soup.li.parents:
    print(parent)

<ul>
  <li>Data Analysis</li>
  <li>Machine Learning</li>
</ul>
```

Instead of returning the first tag, we can find all occurrences of a tag using .find_all(). This function takes in just the name of a tag and returns a list of all occurrences of that tag.
```python
print(soup.find_all("li"))

# Returns
# ['<li>Data Analysis</li>', '<li>Machine Learning</li>']
```
With .find_all(), we can use lists, regexes, attributes, or even functions to select HTML elements more intelligently.

### Using Lists
We can specify all of the elements we want to find with a list of the tag names we are looking for:
```python
soup.find_all(['ul', 'li', 'h1'])
```
### Using Regex
If we want every 'ul' and every 'il' that the page contains, we can select both of these types of elements with a re.compile in our .find_all():
```python
soup.find_all(re.compile("[ou]l"))
```
### Using Attributes
We can pass a dictionary to the attrs parameter of find_all with the desired attributes of the elements we’re looking for. If we want to find all of the elements with the "banner" class, for example, we could use the command:
```python
soup.find_all(attrs={'class':'banner'})

# We can also specify multiple different attributes:
soup.find_all(attrs={'class':'banner', 'id':'jumbotron'})
```
### Using Functions
We can use a function by modifying our selection of tags:
```python
def attributes_and_string(tag):
    output = tag.attr('class') == "banner" and tag.string == "Hello world"
    return output

soup.find_all(has_banner_class_and_hello_world)

# Returns
# '<div class="banner">Hello world</div>'
```

## Closing Remarks
That's it, we have covered the fundamentals of web scraping as well as some basic functions to work around html files to extract data from a website! This is enough for anyone to extract specific data from websites easily.

Web scraping is an incredibly powerful tool, and should not be taken lightly! The ability to harvest data en masse, perform analyses, can help guide us to make wiser decisions or uncover new stories from the underlying data.

As a final note, remember to follow the best practices and rules when scraping data as mentioned above, and stay out of trouble!

# Automation with Python
This repository contains useful tools to equip the user when automating processes with Python. The tools in the repository relies heavily on the use of NumPy and Pandas when dealing with data. The readme can be split into three parts: general introduction, module breakdowns and conclusion.
<p align="center">
  <br>
  <img src="img/automation-robot.png">
  <br>
  <i>Why automation is important.</i>
</p>

## Module Breakdowns
Below you will find a short summary of each module and its specific use case.

### excel.py
Quick and easy automation with the use of some excel functions. With the use of pandas we can read excel files and output them into dictionary with the keys as the sheet name and values as 2D dataframes. There is also a function that helps with running inbuilt excel macros automatically.

### files.py
Generic functions to read, write, copy, or arrange your local files. The class object 'Files' contains class instances for path of folder directory (folder_directory) and name of the file (file_name). 

### decorators.py
Decorators: 'timer' to time function run time in seconds and 'deprecated' to warn users of a deprecated function.

### mongodb.py
MongoDB is a popular noSQL database for modern apps using cloud technologies. In this module you will find generic functions to assist the set up and use of modules PyMongo and Arctic library.

[PyMongo](https://pymongo.readthedocs.io/en/stable/), the python package for MongoDB.  
[Arctic](https://arctic.readthedocs.io/en/latest/), a high performance database that sits atop MongoDB. This is catered to the storage of time series and dataframe data.

Main function 'db_connect' expects your databases to be categorised as 'arctic' or 'non_arctic'(default mongodb). It returns an 'arctic connection' or 'pymongo collection' based on the defined parameters. The 2 parameters are 'is_arctic' to specify arctic/non arctic database and 'lib_name', which is the name of the library to connect to.

The function is passed onto other functions to manipulate the libraries such as creation/deletion of a library, append or write to a library or list the keys and symbols.
