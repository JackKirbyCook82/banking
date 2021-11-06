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
import pandas as pd
from datetime import datetime as Datetime
from datetime import timedelta as Timedelta

MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
MOD_DIR = os.path.abspath(os.path.join(MAIN_DIR, os.pardir))
ROOT_DIR = os.path.abspath(os.path.join(MOD_DIR, os.pardir))
SAVE_DIR = os.path.join(ROOT_DIR, "save")
RESOURCE_DIR = os.path.join(ROOT_DIR, "resources")
REPOSITORY_DIR = os.path.join(SAVE_DIR, "banking")
DRIVER_EXE = os.path.join(RESOURCE_DIR, "chromedriver.exe")
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utilities.input import InputParser
from utilities.dataframes import dataframe_parser
from webscraping.webtimers import WebDelayer
from webscraping.webdrivers import WebDriver
from webscraping.weburl import WebURL
from webscraping.webpages import WebBrowserPage
from webscraping.webpages import WebDatas, WebActions
from webscraping.webloaders import WebLoader
from webscraping.webdownloaders import WebDownloader, WebQuery, WebDataset
from webscraping.webdata import WebClickable, WebButton, WebSelect, WebInput, WebTexts, WebClickables, WebTables, WebKeyedClickables
from webscraping.webactions import WebMoveToClick, WebMoveToSelect, WebUsernamePasswordSend, WebMoveToOpenChoose, WebDateRangeSend

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
activity_open_xpath = "//a[@aria-label='Search']"
activity_select_xpath = "//select[@aria-label='Select a date range']"
activity_fromdate_xpath = "//input[@id='searchStartDate']"
activity_todate_xpath = "//input[@id='searchEndDate']"
activity_xpath = "//button[@allytmfn='Search']"
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
activity_open_webloader = WebLoader(xpath=activity_open_xpath)
activity_select_webloader = WebLoader(xpath=activity_select_xpath)
activity_fromdate_webloader = WebLoader(xpath=activity_fromdate_xpath)
activity_todate_webloader = WebLoader(xpath=activity_todate_xpath)
activity_webloader = WebLoader(xpath=activity_xpath)
transactions_webloader = WebLoader(xpath=transactions_xpath)
pendings_webloader = WebLoader(xpath=pendings_xpath)
download_start_webloader = WebLoader(xpath=download_start_xpath)
download_fileformat_webloader = WebLoader(xpath=download_fileformat_xpath)
download_activity_webloader = WebLoader(xpath=download_activity_xpath)
download_webloader = WebLoader(xpath=download_xpath)


date_parser = lambda x: Datetime.strptime(x, "%b %d,%Y").date()
currency_parser = lambda x: float(str(x).replace("$", "").replace(",", ""))


def table_parser(dataframe, *args, **kwargs):
    dataframe.columns = [column.lower() for column in dataframe.columns]
    dataframe["bank"] = str(kwargs["bank"])
    dataframe["type"] = str(kwargs["type"])
    dataframe["name"] = str(kwargs["name"])
    dataframe = dataframe_parser(dataframe, parsers={"date": date_parser, "amount": currency_parser}, defaultparser=str)
    return dataframe


def table_reduction(dataframes):
    dataframe = pd.concat(dataframes, axis=0, ignore_index=True)
    return dataframe


class Ally_LoginStart(WebButton, webloader=login_start_webloader): pass
class Ally_AccountType(WebSelect, webloader=accounttype_webloader): pass
class Ally_Username(WebInput, webloader=username_webloader): pass
class Ally_Password(WebInput, webloader=password_webloader): pass
class Ally_Login(WebButton, webloader=login_webloader): pass
class Ally_AccountOpen(WebClickable, webloader=account_open_webloader): pass
class Ally_AccountKeys(WebTexts, webloader=account_keys_webloader): pass
class Ally_AccountValues(WebClickables, webloader=account_values_xpath): pass
class Ally_AccountItems(WebKeyedClickables, webloader=account_items_webloader, parsers={"key": str}): pass
class Ally_ActivityOpen(WebClickable, webloader=activity_open_webloader): pass
class Ally_ActivitySelect(WebSelect, webloader=activity_select_webloader): pass
class Ally_ActivityFromDate(WebInput, webloader=activity_fromdate_webloader): pass
class Ally_ActivityToDate(WebInput, webloader=activity_todate_webloader): pass
class Ally_Activity(WebClickable, webloader=activity_webloader): pass
class Ally_Transactions(WebTables, webloader=transactions_webloader, parsers={"table": table_parser}, reduction=table_reduction, headerrow=0, indexcolumn=None): pass
class Ally_Pendings(WebTables, webloader=pendings_webloader, parsers={"table": table_parser}, reduction=table_reduction, headerrow=0, indexcolumn=None): pass
class Ally_DownloadStart(WebClickable, webloader=download_start_webloader): pass
class Ally_DownloadFileFormat(WebSelect, webloader=download_fileformat_webloader): pass
class Ally_DownloadActivity(WebSelect, webloader=download_activity_webloader): pass
class Ally_Download(WebButton, webloader=download_webloader): pass


class Ally_LoginStart_WebAction(WebMoveToClick, on=Ally_LoginStart): pass
class Ally_AccountType_WebAction(WebMoveToSelect, on=Ally_AccountType): pass
class Ally_UserNamePassword_WebAction(WebUsernamePasswordSend, on=[Ally_Username, Ally_Password, Ally_Login]): pass
class Ally_AccountSelect_WebAction(WebMoveToOpenChoose, on=[Ally_AccountOpen, {"keys": Ally_AccountKeys, "values": Ally_AccountValues, "items": Ally_AccountItems}]): pass
class Ally_ActivityOpen_WebAction(WebMoveToClick, on=Ally_ActivityOpen): pass
class Ally_ActivitySelect_WebAction(WebMoveToSelect, on=Ally_ActivitySelect): pass
class Ally_ActivityGet_WebAction(WebDateRangeSend, on=[Ally_ActivityFromDate, Ally_ActivityToDate, Ally_Activity]): pass
class Ally_DownloadStart_WebAction(WebMoveToClick, on=Ally_DownloadStart): pass
class Ally_DownloadFileFormatSelect_WebAction(WebMoveToSelect, on=Ally_DownloadFileFormat): pass
class Ally_DownloadActivitySelect_WebAction(WebMoveToSelect, on=Ally_DownloadActivity): pass
class Ally_Download_WebAction(WebMoveToClick, on=Ally_Download): pass


class Ally_WebDelayer(WebDelayer): pass
class Ally_WebDriver(WebDriver, options={"headless": False, "images": True, "incognito": False}): pass
class Ally_WebURL(WebURL, protocol="https", domain="www.ally.com"): pass
class Ally_WebQuery(WebQuery, fields=["bank", "name", "type"], **__project__): pass
class Ally_WebDataset(WebDataset, fields=["transactions"], **__project__): pass


class Ally_WebDatas(WebDatas):
    TRANSACTIONS = Ally_Transactions
    PENDINGS = Ally_Pendings


class Ally_WebActions(WebActions):
    START_LOGIN = Ally_LoginStart_WebAction
    ACCOUNTTYPE = Ally_AccountType_WebAction
    LOGIN = Ally_UserNamePassword_WebAction
    ACCOUNT = Ally_AccountSelect_WebAction
    OPEN_ACTIVITY = Ally_ActivityOpen_WebAction
    SELECT_ACTIVITY = Ally_ActivitySelect_WebAction
    GET_ACTIVITY = Ally_ActivityGet_WebAction
    START_DOWNLOAD = Ally_DownloadStart_WebAction
    FILETYPE_DOWNLOAD = Ally_DownloadFileFormatSelect_WebAction
    ACTIVITY_DOWNLOAD = Ally_DownloadActivitySelect_WebAction
    DOWNLOAD = Ally_Download_WebAction


class Ally_WebPage(WebBrowserPage, datas=Ally_WebDatas, actions=Ally_WebActions):
    def setup(self, *args, account, username, password, days=90, **kwargs):
        todate = Datetime.now()
        fromdate = todate - Timedelta(days=days)
        self[WebActions.START_LOGIN]()
        self[WebActions.ACCOUNTTYPE](choice="aob")
        self[WebActions.LOGIN](username=username, password=password)
        self[WebActions.ACCOUNT](choice=account)
        self[WebActions.OPEN_ACTIVITY]()
        self[WebActions.SELECT_ACTIVITY](choice="Custom")
        self[WebActions.GET_ACTIVITY](fromDate=fromdate.strftime("%b %d, %Y"), toDate=todate.strftime("%b %d, %Y"))

    def execute(self, *args, **kwargs):
        data = self[WebDatas.TRANSACTIONS](*args, **kwargs)
        query = Ally_WebQuery({key: kwargs[key] for key in ("bank", "name", "type")})
        dataset = Ally_WebDataset({"transactions": data})
        yield query, dataset


class Ally_WebDownloader(WebDownloader):
    @staticmethod
    def execute(*args, delayer, **kwargs):
        with Ally_WebDriver(DRIVER_EXE, browser="chrome", loadtime=50) as driver:
            page = Ally_WebPage(driver, delayer=delayer)
            url = Ally_WebURL()
            page.load(url)
            page.setup(*args, **kwargs)
            yield from page(*args, **kwargs)


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
    sys.argv += ["bank=", "name=", "type=", "account=", "username=", "password="]
    logging.basicConfig(level="INFO", format="[%(levelname)s, %(threadName)s]:  %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
    inputparser = InputParser(proxys={"assign": "=", "space": "_"}, parsers={}, default=str)
    inputparser(*sys.argv[1:])
    main(*inputparser.arguments, **inputparser.parameters)













