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
from webscraping.webdata import WebClickable, WebButton, WebInput, WebSelect, WebTables, WebKeyedClickables
from webscraping.webactions import WebMoveToClick, WebMoveToSelect, WebUsernamePasswordSend, WebMoveToChoose, WebDateRangeSend

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
activity_select_xpath = "//li[@class='option dropdown-option']/a"
activity_fromdate_xpath = "//input[contains(@name, 'FromDate')]"
activity_todate_xpath = "//input[contains(@name, 'ToDate')]"
activity_xpath = "//mds-button[@id='activitySearchFilter']"
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
activity_select_webloader = WebLoader(xpath=activity_select_xpath)
activity_fromdate_webloader = WebLoader(xpath=activity_fromdate_xpath)
activity_todate_webloader = WebLoader(xpath=activity_todate_xpath)
activity_webloader = WebLoader(xpath=activity_xpath)
transactions_webloader = WebLoader(xpath=transactions_xpath)
pendings_webloader = WebLoader(xpath=pendings_xpath)
download_start_webloader = WebLoader(xpath=download_start_xpath)
download_accounts_webloader = WebLoader(xpath=download_accounts_xpath)
download_filetype_webloader = WebLoader(xpath=download_filetype_xpath)
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


class Chase_Username(WebInput, webloader=username_webloader): pass
class Chase_Password(WebInput, webloader=password_webloader): pass
class Chase_LogIn(WebButton, webloader=login_webloader): pass
class Chase_Accounts(WebKeyedClickables, webloader=accounts_webloader): pass
class Chase_ActivitySelect(WebKeyedClickables, webloader=activity_select_webloader): pass
class Chase_ActivityFromDate(WebInput, webloader=activity_fromdate_webloader): pass
class Chase_ActivityToDate(WebInput, webloader=activity_todate_webloader): pass
class Chase_Activity(WebButton, webloader=activity_webloader): pass
class Chase_Transactions(WebTables, webloader=transactions_webloader, parsers={"table": table_parser}, reduction=table_reduction, headerrow=0, indexcolumn=None): pass
class Chase_Pendings(WebTables, webloader=pendings_webloader, parsers={"table": table_parser}, reduction=table_reduction, headerrow=0, indexcolumn=None): pass
class Chase_DownloadStart(WebButton, webloader=download_start_webloader): pass
class Chase_DownloadAccount(WebSelect, webloader=download_accounts_webloader): pass
class Chase_DownloadFiletype(WebSelect, webloader=download_filetype_webloader): pass
class Chase_DownloadActivity(WebSelect, webloader=download_activity_webloader): pass
class Chase_Download(WebClickable, webloader=download_webloader): pass


class Chase_UserNamePassword_WebAction(WebUsernamePasswordSend, on=[Chase_Username, Chase_Password, Chase_LogIn]): pass
class Chase_AccountSelect_WebAction(WebMoveToChoose, on={"items": Chase_Accounts}): pass
class Chase_ActivitySelect_WebAction(WebMoveToSelect, on={"items": Chase_ActivitySelect}): pass
class Chase_ActivityGet_WebAction(WebDateRangeSend, on=[Chase_ActivityFromDate, Chase_ActivityToDate, Chase_Activity]): pass
class Chase_DownloadStart_WebAction(WebMoveToClick, on=Chase_DownloadStart): pass
class Chase_DownloadAccountSelect_WebAction(WebMoveToSelect, on=Chase_DownloadAccount): pass
class Chase_DownloadFileFormatSelect_WebAction(WebMoveToSelect, on=Chase_DownloadFiletype): pass
class Chase_DownloadActivitySelect_WebAction(WebMoveToSelect, on=Chase_DownloadActivity): pass
class Chase_Download_WebAction(WebMoveToClick, on=Chase_Download): pass


class Chase_WebDelayer(WebDelayer): pass
class Chase_WebDriver(WebDriver, options={"headless": False, "images": True, "incognito": False}): pass
class Chase_WebURL(WebURL, protocol="https", domain="www.chase.com"): pass
class Chase_WebQuery(WebQuery, fields=["bank", "name", "type"], **__project__): pass
class Chase_WebDataset(WebDataset, fields=["transactions"], **__project__): pass


class Chase_WebDatas(WebDatas):
    TRANSACTIONS = Chase_Transactions
    PENDINGS = Chase_Pendings


class Chase_WebActions(WebActions):
    LOGIN = Chase_UserNamePassword_WebAction
    ACCOUNT = Chase_AccountSelect_WebAction
    SELECT_ACTIVITY = Chase_ActivitySelect_WebAction
    GET_ACTIVITY = Chase_ActivityGet_WebAction
    START_DOWNLOAD = Chase_DownloadStart_WebAction
    ACCOUNT_DOWNLOAD = Chase_DownloadAccountSelect_WebAction
    FILETYPE_DOWNLOAD = Chase_DownloadFileFormatSelect_WebAction
    ACTIVITY_DOWNLOAD = Chase_DownloadActivitySelect_WebAction
    DOWNLOAD = Chase_Download_WebAction


class Chase_WebPage(WebBrowserPage, datas=Chase_WebActions, actions=Chase_WebActions):
    def setup(self, *args, account, username, password, days=90, **kwargs):
        todate = Datetime.now()
        fromdate = todate - Timedelta(days=days)
        self[WebActions.LOGIN](username=username, password=password)
        self[WebActions.ACCOUNT](choice=account)
        self[WebActions.SELECT_ACTIVITY](choice="Search")
        self[WebActions.ACTIVITY](fromdate=fromdate.strftime("%m/%d/%Y"), todate=todate.strftime("%m/%d/%Y"))

    def execute(self, *args, **kwargs):
        data = self[WebDatas.TRANSACTIONS](*args, **kwargs)
        query = Chase_WebQuery({key: kwargs[key] for key in ("bank", "name", "type")})
        dataset = Chase_WebDataset({"transactions": data})
        yield query, dataset


class Chase_WebDownloader(WebDownloader):
    @staticmethod
    def execute(*args, delayer, **kwargs):
        with Chase_WebDriver(DRIVER_EXE, browser="chrome", loadtime=50) as driver:
            page = Chase_WebPage(driver, delayer=delayer)
            url = Chase_WebURL()
            page.load(url)
            page.setup(*args, **kwargs)
            yield from page(*args, **kwargs)


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
    sys.argv += ["bank=", "name=", "type=", "account=", "username=", "password="]
    logging.basicConfig(level="INFO", format="[%(levelname)s, %(threadName)s]:  %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
    inputparser = InputParser(proxys={"assign": "=", "space": "_"}, parsers={}, default=str)
    inputparser(*sys.argv[1:])
    main(*inputparser.arguments, **inputparser.parameters)







