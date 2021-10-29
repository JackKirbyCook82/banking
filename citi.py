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
from webscraping.webpages import WebDatas, WebActions
from webscraping.webloaders import WebLoader
from webscraping.webdownloaders import WebDownloader, WebQuery, WebDataset
from webscraping.webdata import WebClickable, WebButton, WebInput, WebKeyedClickables, WebTables
from webscraping.webactions import WebUsernamePasswordSend, WebMoveToOpenChoose

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
account_open_xpath = "//a[contains(@id, 'accountsmain')]"
account_items_xpath = "//li[contains(@id, 'accounts')]//li[@role='listitem']/a"
activity_open_xpath = "//citi-dropdown2[contains(@labelid, 'timePeriod')]"
activity_items_xpath = "//citi-options2"
transactions_xpath = "//table[contains(@id, 'postedTransactionTable')]"
pendings_xpath = "//table[contains(@id, 'pendingTransactionTable')]"
download_open_xpath = "//button[@id='exportTransactionsLink']"
download_xpath = "//div[contains(@class, 'modal-footer')]//button[text()='Export']"

username_webloader = WebLoader(xpath=username_xpath)
password_webloader = WebLoader(xpath=password_xpath)
login_webloader = WebLoader(xpath=login_xpath)
accounts_open_webloader = WebLoader(xpath=account_open_xpath)
accounts_items_webloader = WebLoader(xpath=account_items_xpath)
activity_open_webloader = WebLoader(xpath=activity_open_xpath)
activity_items_webloader = WebLoader(xpath=activity_items_xpath)
transactions_webloader = WebLoader(xpath=transactions_xpath)
download_open_webloader = WebLoader(xpath=download_open_xpath)
download_webloader = WebLoader(xpath=download_xpath)


def table_parser(dataframes, *args, **kwargs):
    pass


class Citi_Username(WebInput, webloader=username_webloader): pass
class Citi_Password(WebInput, webloader=password_webloader): pass
class Citi_LogIn(WebButton, webloader=login_webloader): pass
class Citi_AccountOpen(WebClickable, webloader=accounts_open_webloader): pass
class Citi_AccountItems(WebKeyedClickables, webloader=accounts_items_webloader, parsers={"key": str}): pass
class Citi_ActivityOpen(WebClickable, webloader=activity_open_webloader): pass
class Citi_ActivityItems(WebKeyedClickables, webloader=activity_items_webloader, parsers={"key": str}): pass
class Citi_Transactions(WebTables, webloader=transactions_webloader, parsers={"table": table_parser}, headerrow=0, indexcolumn=None): pass
class Citi_Pendings(WebTables, webloader=transactions_webloader, parsers={"table": table_parser}, headerrow=0, indexcolumn=None): pass
class Citi_DownloadOpen(WebClickable, webloader=download_open_webloader): pass
class Citi_Download(WebButton, webloader=download_webloader): pass


class Citi_UserNamePassword_WebAction(WebUsernamePasswordSend, on=[Citi_Username, Citi_Password, Citi_LogIn]): pass
class Citi_AccountsSelect_WebAction(WebMoveToOpenChoose, on=[Citi_AccountOpen, {"items": Citi_AccountItems}]): pass
class Citi_ActivitySelect_WebAction(WebMoveToOpenChoose, on=[Citi_ActivityOpen, {"items": Citi_ActivityItems}]): pass
# class Citi_Download_WebAction(WebMoveToClickSeries, on=[Citi_DownloadOpen, Citi_Download]): pass


class Citi_WebDelayer(WebDelayer): pass
class Citi_WebDriver(WebDriver, options={"headless": False, "images": True, "incognito": False}): pass
class Citi_WebURL(WebURL, protocol="https", domain="www.citi.com"): pass


class Citi_WebDatas(WebDatas):
    TRANSACTIONS = Citi_Transactions
    PENDINGS = Citi_Pendings


class Citi_WebActions(WebActions):
    LOGIN = Citi_UserNamePassword_WebAction
    ACCOUNT = Citi_AccountsSelect_WebAction
    ACTIVITY = Citi_ActivitySelect_WebAction
    DOWNLOAD = Citi_Download_WebAction


class Citi_WebPage(WebBrowserPage, datas=WebDatas, actions=WebActions):
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

