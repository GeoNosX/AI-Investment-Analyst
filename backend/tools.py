from langchain_core.tools import tool
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_community.utilities import GoogleSerperAPIWrapper
import yfinance as yf
from dotenv import load_dotenv
load_dotenv()

serper = GoogleSerperAPIWrapper()


@tool
def news_yh_search(ticker: str):
    """Find additional financial news about a stock
    Args:
          ticker: The ticker of a company in order to find news about it """
    # YahooFinanceNewsTool wrapper
    tool_instance = YahooFinanceNewsTool()
    return tool_instance.run(f"{ticker}")

@tool
def get_fin_data(ticker: str):
    """Find financial data about a stock including financials, balance sheet and cashflow.
    Args:
          ticker: The ticker of a company you are looking for"""
    stock = yf.Ticker(ticker)

    try:
        fin_data = stock.financials.to_string()
        fin_data += "\n" + stock.balance_sheet.to_string()
        fin_data += "\n" + stock.cashflow.to_string()
        return fin_data
    except Exception as e:
        return f"Error fetching financial data: {e}"

@tool
def serper_search(ticker: str):
    """Find general financial news about a stock using Google Search
    Args:
          ticker: The ticker of a company in order to find news about it """
    return serper.run(f"Find financial data and news about {ticker}")

tools = [get_fin_data, serper_search, news_yh_search]
