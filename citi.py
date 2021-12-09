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

from utilities.iostream import InputParser
from utilities.dataframes import dataframe_parser
from webscraping.webtimers import WebDelayer
from webscraping.webdrivers import WebDriver
from webscraping.weburl import WebURL
from webscraping.webpages import WebBrowserPage
from webscraping.webpages import WebDatas, WebActions
from webscraping.webloaders import WebLoader
from webscraping.webdownloaders import WebDownloader, WebQuery, WebDataset
from webscraping.webdata import WebClickable, WebButton, WebInput, WebKeyedClickables, WebTables
from webscraping.webactions import WebMoveToClick, WebMoveToSelect, WebUsernamePasswordSend, WebMoveToOpenChoose, WebDateRangeSend

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
activity_select_xpath = "//citi-options2"
activity_fromdate_xpath = "//input[@id='fromDatePicker']"
activity_todate_xpath = "//input[@id='toDatePicker']"
activity_xpath = "//button[@id='dateRangeApplyButton']"
transactions_xpath = "//table[contains(@id, 'postedTransactionTable')]"
pendings_xpath = "//table[contains(@id, 'pendingTransactionTable')]"
download_open_xpath = "//button[@id='exportTransactionsLink']"
download_xpath = "//div[contains(@class, 'modal-footer')]//button[text()='Export']"


username_webloader = WebLoader(xpath=username_xpath)
password_webloader = WebLoader(xpath=password_xpath)
login_webloader = WebLoader(xpath=login_xpath)
accounts_open_webloader = WebLoader(xpath=account_open_xpath)
accounts_items_webloader = WebLoader(xpath=account_items_xpath)
activity_select_webloader = WebLoader(xpath=activity_select_xpath)
activity_fromdate_webloader = WebLoader(xpath=activity_fromdate_xpath)
activity_todate_webloader = WebLoader(xpath=activity_todate_xpath)
activity_webloader = WebLoader(xpath=activity_xpath)
transactions_webloader = WebLoader(xpath=transactions_xpath)
download_open_webloader = WebLoader(xpath=download_open_xpath)
download_webloader = WebLoader(xpath=download_xpath)


date_parser = lambda x: Datetime.strptime(x, "%b %d,%Y").date()
currency_parser = lambda x: float(str(x).replace("$", "").replace(",", ""))


def table_parser(dataframe, *args, **kwargs):
    dataframe.columns = [column.lower() for column in dataframe.columns]
    dataframe.rename({"running balance": "balance"})
    dataframe["bank"] = str(kwargs["bank"])
    dataframe["type"] = str(kwargs["type"])
    dataframe["name"] = str(kwargs["name"])
    dataframe = dataframe_parser(dataframe, parsers={"date": date_parser, "amount": currency_parser}, defaultparser=str)
    return dataframe


def table_reduction(dataframes):
    dataframe = pd.concat(dataframes, axis=0, ignore_index=True)
    return dataframe


class Citi_Username(WebInput, webloader=username_webloader): pass
class Citi_Password(WebInput, webloader=password_webloader): pass
class Citi_LogIn(WebButton, webloader=login_webloader): pass
class Citi_AccountOpen(WebClickable, webloader=accounts_open_webloader): pass
class Citi_AccountItems(WebKeyedClickables, webloader=accounts_items_webloader, parsers={"key": str}): pass
class Citi_ActivitySelect(WebKeyedClickables, webloader={"items": activity_select_webloader}): pass
class Citi_ActivityFromDate(WebInput, webloader=activity_fromdate_webloader): pass
class Citi_ActivityToDate(WebInput, webloader=activity_todate_webloader): pass
class Citi_Activity(WebClickable, webloader=activity_webloader): pass
class Citi_Transactions(WebTables, webloader=transactions_webloader, parsers={"table": table_parser}, reduction=table_reduction, headerrow=0, indexcolumn=None): pass
class Citi_Pendings(WebTables, webloader=transactions_webloader, parsers={"table": table_parser}, reduction=table_reduction, headerrow=0, indexcolumn=None): pass
class Citi_DownloadOpen(WebClickable, webloader=download_open_webloader): pass
class Citi_Download(WebButton, webloader=download_webloader): pass


class Citi_UserNamePassword_WebAction(WebUsernamePasswordSend, on=[Citi_Username, Citi_Password, Citi_LogIn]): pass
class Citi_AccountsSelect_WebAction(WebMoveToOpenChoose, on=[Citi_AccountOpen, {"items": Citi_AccountItems}]): pass
class Citi_ActivitySelect_WebAction(WebMoveToSelect, on=Citi_ActivitySelect): pass
class Citi_ActivityGet_WebAction(WebDateRangeSend, on=[Citi_ActivityFromDate, Citi_ActivityToDate, Citi_Activity]): pass
class Citi_DownloadOpen_WebAction(WebMoveToClick, on=Citi_DownloadOpen): pass
class Citi_Download_WebAction(WebMoveToClick, on=Citi_Download): pass


class Citi_WebDelayer(WebDelayer): pass
class Citi_WebDriver(WebDriver, options={"headless": False, "images": True, "incognito": False}): pass
class Citi_WebURL(WebURL, protocol="https", domain="www.citi.com"): pass
class Citi_WebQuery(WebQuery, fields=["bank", "name", "type"], **__project__): pass
class Citi_WebDataset(WebDataset, fields=["transactions"], **__project__): pass


class Citi_WebDatas(WebDatas):
    TRANSACTIONS = Citi_Transactions
    PENDINGS = Citi_Pendings


class Citi_WebActions(WebActions):
    LOGIN = Citi_UserNamePassword_WebAction
    ACCOUNT = Citi_AccountsSelect_WebAction
    SELECT_ACTIVITY = Citi_ActivitySelect_WebAction
    GET_ACTIVITY = Citi_ActivityGet_WebAction
    START = Citi_DownloadOpen_WebAction
    DOWNLOAD = Citi_Download_WebAction


class Citi_WebPage(WebBrowserPage, datas=Citi_WebDatas, actions=Citi_WebActions):
    def setup(self, *args, account, username, password, days=90, **kwargs):
        todate = Datetime.now()
        fromdate = todate - Timedelta(days=days)
        self[WebActions.LOGIN](username=username, password=password)
        self[WebActions.ACCOUNT](choice=account)
        self[WebActions.START_ACTIVITY](choice="Date range")
        self[WebActions.ACTIVITY](fromDate=fromdate.strftime("%m/%d/%Y"), toDate=todate.strftime("%m/%d/%Y"))

    def execute(self, *args, **kwargs):
        data = self[WebDatas.TRANSACTIONS](*args, **kwargs)
        query = Citi_WebQuery({key: kwargs[key] for key in ("bank", "name", "type")})
        dataset = Citi_WebDataset({"transactions": data})
        yield query, dataset


class Citi_WebDownloader(WebDownloader):
    @staticmethod
    def execute(*args, delayer, **kwargs):
        with Citi_WebDriver(DRIVER_EXE, browser="chrome", loadtime=50) as driver:
            page = Citi_WebPage(driver, delayer=delayer)
            url = Citi_WebURL()
            page.load(url)
            page.setup(*args, **kwargs)
            yield from page(*args, **kwargs)


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
    sys.argv += ["bank=", "name=", "type=", "account", "username=", "password="]
    logging.basicConfig(level="INFO", format="[%(levelname)s, %(threadName)s]:  %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
    inputparser = InputParser(proxys={"assign": "=", "space": "_"}, parsers={}, default=str)
    inputparser(*sys.argv[1:])
    main(*inputparser.arguments, **inputparser.parameters)

