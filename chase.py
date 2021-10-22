# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2021
@name:   Chase Banking Accounts Download Application
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
REPOSITORY_DIR = os.path.join(SAVE_DIR, "chase")
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
__all__ = ["Chase_WebDelayer", "Chase_WebDownloader"]
__copyright__ = "Copyright 2021, Jack Kirby Cook"
__license__ = ""
__project__ = {"website": "Chase", "project": "Accounts"}


LOGGER = logging.getLogger(__name__)
warnings.filterwarnings("ignore")


username_xpath = "//input[contains(@id, 'userID')]"
password_xpath = "//input[contains(@id, 'password')]"
login_xpath = "//section/a[contains(@data-pt-name, 'signin')]"
accounts_xpath = "//div[contains(@class, 'accounts-blade')]//mds-button[contains(@id, 'account')]"
activity_xpath = "//a[contains(@id, 'header-transaction')]"
showing_xpath = "//ul[contains(@id, 'transaction')]/li/a"
extend_xpath = "//mds-button[@id='seeMore']"
transactions_xpath = "//table[contains(@aria-label, 'Transaction activity')]"


username_webloader = WebLoader(xpath=username_xpath)
password_webloader = WebLoader(xpath=password_xpath)
login_webloader = WebLoader(xpath=login_xpath)
accounts_webloader = WebLoader(xpath=accounts_xpath)
activity_webloader = WebLoader(xpath=activity_xpath)
showing_webloader = WebLoader(xpath=showing_xpath)
extend_webloader = WebLoader(xpath=extend_xpath)
transactions_webloader = WebLoader(xpath=transactions_xpath)


def transactions_parser(dataframes, *args, **kwargs):
    pass


class Chase_Username(WebInput, webloader=username_webloader): pass
class Chase_Password(WebInput, webloader=password_webloader): pass
class Chase_LogIn(WebButton, webloader=login_webloader): pass
class Chase_Names(WebTexts, webloader=accounts_webloader): pass
class Chase_Accounts(WebClickables, webloader=accounts_webloader): pass
class Chase_Activity(WebClickable, webloader=activity_webloader): pass
class Chase_Showing(WebClickables, webloader=showing_webloader): pass
class Chase_Extend(WebButton, webloader=extend_webloader): pass
class Chase_Transactions(WebTables, webloader=transactions_webloader, parsers={"table": transactions_parser}, headerrow=0, indexcolumn=None): pass


class Chase_Username_WebMoveToClickFill(WebMoveToClickFill, on=Chase_Username): pass
class Chase_Password_WebMoveToClickFill(WebMoveToClickFill, on=Chase_Password): pass
class Chase_LogIn_WebMoveToClick(WebMoveToClick, on=Chase_LogIn): pass
class Chase_Accounts_WebMoveToClick(WebMoveToClick, on=Chase_Accounts): pass
class Chase_Activity_WebMoveToClick(WebMoveToClick, on=Chase_Activity): pass
class Chase_Showing_WebMoveToClick(WebMoveToClick, on=Chase_Showing): pass
class Chase_Extend_WebMoveToClick(WebMoveToClick, on=Chase_Extend): pass


class Chase_WebDelayer(WebDelayer): pass
class Chase_WebDriver(WebDriver, options={"headless": False, "images": True, "incognito": False}): pass
class Chase_WebURL(WebURL, protocol="https", domain="www.chase.com"): pass


class Chase_WebContents(WebContents):
    USERNAME = Chase_Username_WebMoveToClickFill
    PASSWORD = Chase_Password_WebMoveToClickFill
    LOGIN = Chase_LogIn_WebMoveToClick
    NAMES = Chase_Names
    ACCOUNTS = Chase_Accounts_WebMoveToClick
    ACTIVITY = Chase_Activity_WebMoveToClick
    SHOWING = Chase_Showing_WebMoveToClick
    EXTEND = Chase_Extend_WebMoveToClick
    TRANSACTIONS = Chase_Transactions


class Chase_WebPage(WebBrowserPage, contents=Chase_WebContents):
    def setup(self, *args, **kwargs):
        pass

    def execute(self, *args, **kwargs):
        pass


class Chase_WebDownloader(WebDownloader):
    @staticmethod
    def execute(*args, delayer, **kwargs):
        pass


def main(*args, **kwargs):
    delayer = Chase_WebDelayer("random", wait=(5, 10))
    downloader = Chase_WebDownloader(*args, repository=REPOSITORY_DIR, **kwargs)
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







