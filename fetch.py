import openai
import requests
import datetime
import pandas as pd
from privtoken import OPEN_AI_API_KEY
from privtoken import ALPHA_VANTAGE_API_KEY

def fetch_cfs(symbol):
    api_url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    r = requests.get(api_url)
    data = r.json()
    df = pd.DataFrame.from_dict(data['quarterlyReports'])
    return df


def fetch_bs(symbol):
    api_url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    r = requests.get(api_url)
    data = r.json()
    df = pd.DataFrame.from_dict(data['quarterlyReports'])
    return df


def fetch_is(symbol):
    api_url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    r = requests.get(api_url)
    data = r.json()
    df = pd.DataFrame.from_dict(data['quarterlyReports'])
    return df