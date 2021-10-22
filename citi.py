# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2021
@name:   Citi Banking Accounts Download Application
@author: Jack Kirby Cook

"""

import sys
import os.path
import warnings
import logging

MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
MOD_DIR = os.path.abspath(os.path.join(MAIN_DIR, os.pardir))
ROOT_DIR = os.path.abspath(os.path.join(MOD_DIR, os.pardir))
SAVE_DIR = os.path.join(ROOT_DIR, "save")
RESOURCE_DIR = os.path.join(ROOT_DIR, "resources")
REPOSITORY_DIR = os.path.join(SAVE_DIR, "citi")
DRIVER_FILE = os.path.join(RESOURCE_DIR, "chromedriver.exe")
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utilities.input import InputParser
from webscraping.webtimers import WebDelayer
from webscraping.webdrivers import WebDriver
from webscraping.weburl import WebURL
from webscraping.webpages import WebBrowserPage
from webscraping.webpages import WebContents
from webscraping.webloaders import WebLoader
from webscraping.webdownloaders import WebDownloader, WebQuery, WebDataset
from webscraping.webdata import WebClickable, WebButton, WebInput, WebTexts, WebClickables, WebTables
from webscraping.webactions import WebMoveToClick, WebMoveToClickFill

__version__ = "1.0.0"
__author__ = "Jack Kirby Cook"
__all__ = ["Citi_WebDelayer", "Citi_WebDownloader"]
__copyright__ = "Copyright 2021, Jack Kirby Cook"
__license__ = ""
__project__ = {"website": "Citi", "project": "Accounts"}


LOGGER = logging.getLogger(__name__)
warnings.filterwarnings("ignore")


username_xpath = "//input[contains(@id, 'cds')]"
password_xpath = "//input[contains(@id, 'password')]"
login_xpath = "//button[contains(@id, 'signInBtn')]"
accounts_xpath = "//li[contains(@id, 'accounts')]//li[@role='listitem']/a"
activity_xpath = "//div[contains(@id, 'timePeriod')]"
showing_xpath = "//citi-options2"
transactions_xpath = ""


username_webloader = WebLoader(xpath=username_xpath)
password_webloader = WebLoader(xpath=password_xpath)
login_webloader = WebLoader(xpath=login_xpath)
accounts_webloader = WebLoader(xpath=accounts_xpath)
activity_webloader = WebLoader(xpath=activity_xpath)
showing_webloader = WebLoader(xpath=showing_xpath)
transactions_webloader = WebLoader(xpath=transactions_xpath)


def transactions_parser(dataframes, *args, **kwargs):
    pass


class Citi_Username(WebInput, webloader=username_webloader): pass
class Citi_Password(WebInput, webloader=password_webloader): pass
class Citi_LogIn(WebButton, webloader=login_webloader): pass
class Citi_Names(WebTexts, webloader=accounts_webloader): pass
class Citi_Accounts(WebClickables, webloader=accounts_webloader): pass
class Citi_Activity(WebClickable, webloader=activity_webloader): pass
class Citi_Showing(WebClickables, webloader=showing_webloader): pass
class Citi_Transactions(WebTables, webloader=transactions_webloader, parsers={"table": transactions_parser}, headerrow=0, indexcolumn=None): pass


class Citi_Username_WebMoveToClickFill(WebMoveToClickFill, on=Citi_Username): pass
class Citi_Password_WebMoveToClickFill(WebMoveToClickFill, on=Citi_Password): pass
class Citi_LogIn_WebMoveToClick(WebMoveToClick, on=Citi_LogIn): pass
class Citi_Accounts_WebMoveToClick(WebMoveToClick, on=Citi_Accounts): pass
class Citi_Activity_WebMoveToClick(WebMoveToClick, on=Citi_Activity): pass
class Citi_Showing_WebMoveToClick(WebMoveToClick, on=Citi_Showing): pass


class Citi_WebDelayer(WebDelayer): pass
class Citi_WebDriver(WebDriver, options={"headless": False, "images": True, "incognito": False}): pass
class Citi_WebURL(WebURL, protocol="https", domain="www.citi.com"): pass


class Citi_WebContents(WebContents):
    USERNAME = Citi_Username_WebMoveToClickFill
    PASSWORD = Citi_Password_WebMoveToClickFill
    LOGIN = Citi_LogIn_WebMoveToClick
    NAMES = Citi_Names
    ACCOUNTS = Citi_Accounts_WebMoveToClick
    ACTIVITY = Citi_Activity_WebMoveToClick
    SHOWING = Citi_Showing_WebMoveToClick
    TRANSACTIONS = Citi_Transactions


class Citi_WebPage(WebBrowserPage, contents=Citi_WebContents):
    def setup(self, *args, **kwargs):
        pass

    def execute(self, *args, **kwargs):
        pass


class Citi_WebDownloader(WebDownloader):
    @staticmethod
    def execute(*args, delayer, **kwargs):
        pass


def main(*args, **kwargs):
    delayer = Citi_WebDelayer("random", wait=(5, 10))
    downloader = Citi_WebDownloader(*args, repository=REPOSITORY_DIR, **kwargs)
    downloader(*args, delayer=delayer, **kwargs)
    LOGGER.info(str(downloader))
    for query, results in downloader.results:
        LOGGER.info(str(query))
        LOGGER.info(str(results))
    if not bool(downloader):
        raise downloader.error


if __name__ == "__main__":
    sys.argv += []
    logging.basicConfig(level="INFO", format="[%(levelname)s, %(threadName)s]:  %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
    inputparser = InputParser(proxys={"assign": "=", "space": "_"}, parsers={}, default=str)
    inputparser(*sys.argv[1:])
    main(*inputparser.arguments, **inputparser.parameters)

