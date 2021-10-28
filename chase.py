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
from webscraping.webpages import WebDatas, WebActions
from webscraping.webloaders import WebLoader
from webscraping.webdownloaders import WebDownloader, WebQuery, WebDataset
from webscraping.webdata import WebClickable, WebButton, WebInput, WebSelect, WebTables, WebKeyedClickables
from webscraping.webactions import *

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
accounts_xpath = "//span[contains(text(), '(...')]/parent::*"
activity_open_xpath = "//a[contains(@id, 'header-transaction')]"
activity_items_xpath = "//ul[contains(@id, 'transaction')]/li[contains(@class, 'option')]/a"
activity_more_xpath = "//mds-button[@id='seeMore']"
transactions_xpath = "//table[contains(@aria-label, 'Transaction activity')]"
pendings_xpath = "//table[contains(@aria-label, 'Pending transaction activity')]"
download_start_xpath = "//mds-button[contains(@class, 'download')]"
download_accounts_xpath = "//mds-select[@id='account-selector']"
download_filetype_xpath = "//mds-select[@id='downloadFileTypeOption']"
download_activity_xpath = "//mds-select[@id='downloadActivityOptionId']"
download_xpath = "//mds-button[@id='download']"


username_webloader = WebLoader(xpath=username_xpath)
password_webloader = WebLoader(xpath=password_xpath)
login_webloader = WebLoader(xpath=login_xpath)
accounts_webloader = WebLoader(xpath=accounts_xpath)
activity_open_webloader = WebLoader(xpath=activity_open_xpath)
activity_items_webloader = WebLoader(xpath=activity_items_xpath, rpath=activity_items_xpath + "//span[contains(@class, 'accessible')]")
activity_more_webloader = WebLoader(xpath=activity_more_xpath)
transactions_webloader = WebLoader(xpath=transactions_xpath)
pendings_webloader = WebLoader(xpath=pendings_xpath)
download_start_webloader = WebLoader(xpath=download_start_xpath)
download_accounts_webloader = WebLoader(xpath=download_accounts_xpath)
download_filetype_webloader = WebLoader(xpath=download_filetype_xpath)
download_activity_webloader = WebLoader(xpath=download_activity_xpath)
download_webloader = WebLoader(xpath=download_xpath)


def table_parser(dataframes, *args, **kwargs):
    pass


class Chase_Username(WebInput, webloader=username_webloader): pass
class Chase_Password(WebInput, webloader=password_webloader): pass
class Chase_LogIn(WebButton, webloader=login_webloader): pass
class Chase_AccountOpen(WebKeyedClickables, webloader=accounts_webloader): pass
class Chase_ActivityOpen(WebClickable, webloader=activity_open_webloader): pass
class Chase_ActivityItems(WebKeyedClickables, webloader=activity_items_webloader): pass
class Chase_ActivityMore(WebClickable, webloader=activity_more_webloader): pass
class Chase_Transactions(WebTables, webloader=transactions_webloader, parsers={"table": table_parser}, headerrow=0, indexcolumn=None): pass
class Chase_Pendings(WebTables, webloader=pendings_webloader, parsers={"table": table_parser}, headerrow=0, indexcolumn=None): pass
class Chase_DownloadStart(WebButton, webloader=download_start_webloader): pass
class Chase_DownloadAccount(WebSelect, webloader=download_accounts_webloader): pass
class Chase_DownloadFiletype(WebSelect, webloader=download_filetype_webloader): pass
class Chase_DownloadActivity(WebSelect, webloader=download_activity_webloader): pass
class Chase_Download(WebClickable, webloader=download_webloader): pass


""" WebActions """


class Chase_WebDelayer(WebDelayer): pass
class Chase_WebDriver(WebDriver, options={"headless": False, "images": True, "incognito": False}): pass
class Chase_WebURL(WebURL, protocol="https", domain="www.chase.com"): pass


class Chase_WebDatas(WebDatas):
    pass


class Chase_WebActions(WebActions):
    pass


class Chase_WebPage(WebBrowserPage, datas=Chase_WebActions, actions=Chase_WebActions):
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







