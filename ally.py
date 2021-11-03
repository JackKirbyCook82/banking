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
from webscraping.webpages import WebDatas, WebActions
from webscraping.webloaders import WebLoader
from webscraping.webdownloaders import WebDownloader, WebQuery, WebDataset
from webscraping.webdata import WebClickable, WebButton, WebSelect, WebInput, WebTexts, WebClickables, WebTables, WebKeyedClickables
from webscraping.webactions import WebMoveToClick, WebMoveToSelect, WebUsernamePasswordSend, WebMoveToOpenChoose

__version__ = "1.0.0"
__author__ = "Jack Kirby Cook"
__all__ = ["Ally_WebDelayer", "Ally_WebDownloader"]
__copyright__ = "Copyright 2021, Jack Kirby Cook"
__license__ = ""
__project__ = {"website": "Ally", "project": "Accounts"}


LOGGER = logging.getLogger(__name__)
warnings.filterwarnings("ignore")


login_start_xpath = "//button[@id='login-btn']"
accounttype_xpath = "//select[contains(@name, 'account')]"
username_xpath = "//input[contains(@id, 'username')]"
password_xpath = "//input[contains(@id, 'password')]"
login_xpath = "//button[contains(@class, 'submit')]"
account_open_xpath = "//div[./span[@aria-label='Open Accounts menu']]"
account_items_xpath = "//main[@id='main']//a"
account_values_xpath = "//div[./span[@aria-label='Open Accounts menu']]//div[@role='menu']//div[contains(@data-testid, 'account-dropdown')]/a"
account_keys_xpath = "(//div[./span[@aria-label='Open Accounts menu']]//div[@role='menu']//div[contains(@data-testid, 'account-dropdown')]/a//p)[2]"
containers_xpath = "//table/caption"
transactions_xpath = "//section[contains(@class, 'transactions-history')]//table"
pendings_xpath = "//div[contains(@class, 'upcoming')]//table"
download_start_xpath = "//a[@aria-label='Download']"
download_fileformat_xpath = "//select[@id='select-file-format']"
download_activity_xpath = "//select[@id='select-date-range']"
download_xpath = "//button[@data-track-name='Download']"


login_start_webloader = WebLoader(xpath=login_start_xpath)
accounttype_webloader = WebLoader(xpath=accounttype_xpath)
username_webloader = WebLoader(xpath=username_xpath)
password_webloader = WebLoader(xpath=password_xpath)
login_webloader = WebLoader(xpath=login_xpath)
account_open_webloader = WebLoader(xpath=account_open_xpath)
account_items_webloader = WebLoader(xpath=account_items_xpath)
account_values_webloader = WebLoader(xpath=account_values_xpath)
account_keys_webloader = WebLoader(xpath=account_keys_xpath)
containers_webloader = WebLoader(xpath=containers_xpath)
transactions_webloader = WebLoader(xpath=transactions_xpath)
pendings_webloader = WebLoader(xpath=pendings_xpath)
download_start_webloader = WebLoader(xpath=download_start_xpath)
download_fileformat_webloader = WebLoader(xpath=download_fileformat_xpath)
download_activity_webloader = WebLoader(xpath=download_activity_xpath)
download_webloader = WebLoader(xpath=download_xpath)


def table_parser(dataframes, *args, **kwargs):
    pass


class Ally_LoginStart(WebButton, webloader=login_start_webloader): pass
class Ally_AccountType(WebSelect, webloader=accounttype_webloader, mapping={"bank": "aob", "auto": "aaos"}): pass
class Ally_Username(WebInput, webloader=username_webloader): pass
class Ally_Password(WebInput, webloader=password_webloader): pass
class Ally_Login(WebButton, webloader=login_webloader): pass
class Ally_AccountOpen(WebClickable, webloader=account_open_webloader): pass
class Ally_AccountKeys(WebTexts, webloader=account_keys_webloader): pass
class Ally_AccountValues(WebClickables, webloader=account_values_xpath): pass
class Ally_AccountItems(WebKeyedClickables, webloader=account_items_webloader, parsers={"key": str}): pass
class Ally_Containers(WebClickables, webloader=containers_xpath): pass
class Ally_Transactions(WebTables, webloader=transactions_webloader, parsers={"table": table_parser}, headerrow=0, indexcolumn=None): pass
class Ally_Pendings(WebTables, webloader=pendings_webloader, parsers={"table": table_parser}, headerrow=0, indexcolumn=None): pass
class Ally_DownloadStart(WebClickable, webloader=download_start_webloader): pass
class Ally_DownloadFileFormat(WebSelect, webloader=download_fileformat_webloader): pass
class Ally_DownloadActivity(WebSelect, webloader=download_activity_webloader): pass
class Ally_Download(WebButton, webloader=download_webloader): pass


class Ally_LoginStart_WebAction(WebMoveToClick, on=Ally_LoginStart): pass
class Ally_AccountType_WebAction(WebMoveToSelect, on=Ally_AccountType): pass
class Ally_UserNamePassword_WebAction(WebUsernamePasswordSend, on=[Ally_Username, Ally_Password, Ally_Login]): pass
class Ally_AccountSelect_WebAction(WebMoveToOpenChoose, on=[Ally_AccountOpen, {"keys": Ally_AccountKeys, "values": Ally_AccountValues, "items": Ally_AccountItems}]): pass
class Ally_OpenTables_WebAction(WebMoveToClick, on=Ally_Containers): pass
class Ally_DownloadStart_WebAction(WebMoveToClick, on=Ally_DownloadStart): pass
class Ally_FileFormatSelect_WebAction(WebMoveToSelect, on=Ally_DownloadFileFormat): pass
class Ally_ActivitySelect_WebAction(WebMoveToSelect, on=Ally_DownloadActivity): pass
class Ally_Download_WebAction(WebMoveToClick, on=Ally_Download): pass


class Ally_WebDelayer(WebDelayer): pass
class Ally_WebDriver(WebDriver, options={"headless": False, "images": True, "incognito": False}): pass
class Ally_WebURL(WebURL, protocol="https", domain="www.ally.com"): pass


class Ally_WebDatas(WebDatas):
    TRANSACTIONS = Ally_Transactions
    PENDINGS = Ally_Pendings


class Ally_WebActions(WebActions):
    START_LOGIN = Ally_LoginStart_WebAction
    ACCOUNTTYPE = Ally_AccountType_WebAction
    LOGIN = Ally_UserNamePassword_WebAction
    ACCOUNT = Ally_AccountSelect_WebAction
    OPEN = Ally_OpenTables_WebAction
    START_DOWNLOAD = Ally_DownloadStart_WebAction
    FILETYPE = Ally_FileFormatSelect_WebAction
    ACTIVITY = Ally_ActivitySelect_WebAction
    DOWNLOAD = Ally_Download_WebAction


class Ally_WebPage(WebBrowserPage, datas=Ally_WebDatas, actions=Ally_WebActions):
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













