# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 2021
@name:   Ally Banking Accounts Download Application
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
REPOSITORY_DIR = os.path.join(SAVE_DIR, "ally")
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
from webscraping.webdata import WebButton, WebSelect, WebInput, WebTexts, WebClickables, WebTables, WebExtenders
from webscraping.webactions import WebMoveToClick, WebMoveToClickFill, WebMoveToClickSelect

__version__ = "1.0.0"
__author__ = "Jack Kirby Cook"
__all__ = ["Ally_WebDelayer", "Ally_WebDownloader"]
__copyright__ = "Copyright 2021, Jack Kirby Cook"
__license__ = ""
__project__ = {"website": "Ally", "project": "Accounts"}


LOGGER = logging.getLogger(__name__)
warnings.filterwarnings("ignore")


login_xpath = "//button[@id='login-btn']"
accounttype_xpath = "//select[contains(@name, 'account')]"
username_xpath = "//input[contains(@id, 'username')]"
password_xpath = "//input[contains(@id, 'password')]"
submit_xpath = "//button[contains(@class, 'submit')]"
accounts_xpath = "//div[@data-testid='account-card']//a"
extends_xpath = "//table/caption"
transactions_xpath = "//section[contains(@class, 'transactions-history')]//table"


login_webloader = WebLoader(xpath=login_xpath)
accounttype_webloader = WebLoader(xpath=accounttype_xpath)
username_webloader = WebLoader(xpath=username_xpath)
password_webloader = WebLoader(xpath=password_xpath)
submit_webloader = WebLoader(xpath=submit_xpath)
accounts_webloader = WebLoader(xpath=accounts_xpath)
extends_webloader = WebLoader(xpath=extends_xpath)
transactions_webloader = WebLoader(xpath=transactions_xpath)


def transactions_parser(dataframes, *args, **kwargs):
    pass


class Ally_LogIn(WebButton, webloader=login_webloader): pass
class Ally_AccountType(WebSelect, webloader=accounttype_webloader): pass
class Ally_Username(WebInput, webloader=username_webloader): pass
class Ally_Password(WebInput, webloader=password_webloader): pass
class Ally_Submit(WebButton, webloader=submit_webloader): pass
class Ally_Names(WebTexts, webloader=accounts_webloader): pass
class Ally_Accounts(WebClickables, webloader=accounts_webloader): pass
class Ally_Extends(WebExtenders, webloader=extends_webloader): pass
class Ally_Transactions(WebTables, webloader=transactions_webloader, parsers={"table": transactions_parser}, headerrow=0, indexcolumn=None): pass


class Ally_LogIn_WebMoveToClick(WebMoveToClick, on=Ally_LogIn): pass
class Ally_WebMoveToClickSelect(WebMoveToClickSelect, on=Ally_AccountType): pass
class Ally_Username_WebMoveToClickFill(WebMoveToClickFill, on=Ally_Username): pass
class Ally_Password_WebMoveToClickFill(WebMoveToClickFill, on=Ally_Password): pass
class Ally_Submit_WebMoveToClick(WebMoveToClick, on=Ally_Submit): pass
class Ally_Extends_WebMoveToClick(WebMoveToClick, on=Ally_Extends): pass
class Ally_Accounts_WebMoveToClick(WebMoveToClick, on=Ally_Accounts): pass


class Ally_WebDelayer(WebDelayer): pass
class Ally_WebDriver(WebDriver, options={"headless": False, "images": True, "incognito": False}): pass
class Ally_WebURL(WebURL, protocol="https", domain="www.ally.com"): pass


class Ally_WebContents(WebContents):
    LOGIN = Ally_LogIn_WebMoveToClick
    TYPE = Ally_WebMoveToClickSelect
    USERNAME = Ally_Username_WebMoveToClickFill
    PASSWORD = Ally_Password_WebMoveToClickFill
    SUBMIT = Ally_Submit_WebMoveToClick
    NAMES = Ally_Names
    ACCOUNTS = Ally_Accounts_WebMoveToClick
    EXTENDS = Ally_Extends_WebMoveToClick
    TRANSACTIONS = Ally_Transactions


class Ally_WebPage(WebBrowserPage, contents=Ally_WebContents):
    def setup(self, *args, **kwargs):
        pass

    def execute(self, *args, **kwargs):
        pass


class Ally_WebDownloader(WebDownloader):
    @staticmethod
    def execute(*args, delayer, **kwargs):
        pass


def main(*args, **kwargs):
    delayer = Ally_WebDelayer("random", wait=(5, 10))
    downloader = Ally_WebDownloader(*args, repository=REPOSITORY_DIR, **kwargs)
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













