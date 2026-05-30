import asyncio
import requests
import yfinance as yf
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_community.utilities import GoogleSerperAPIWrapper

load_dotenv()

serper = GoogleSerperAPIWrapper()

safe_session = requests.Session()
safe_session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

@tool
def news_yh_search(ticker: str):
    """Find additional financial news about a stock."""
    try:
        tool_instance = YahooFinanceNewsTool()
        return tool_instance.run(f"{ticker}")
    except Exception as e:
        return "⚠️ Yahoo Finance news is currently unavailable due to rate limits. Please rely on the 'serper_search' tool for news."

def _fetch_yf_data(ticker):
    stock = yf.Ticker(ticker, session=safe_session)
    
    
    try:
        income = stock.quarterly_income_stmt.to_string()
        balance = stock.quarterly_balance_sheet.to_string()
        cashflow = stock.quarterly_cashflow.to_string()
        
        return f"--- INCOME STATEMENT ---\n{income}\n\n--- BALANCE SHEET ---\n{balance}\n\n--- CASH FLOW ---\n{cashflow}"
    except Exception:
        return None

@tool
async def get_fin_data(ticker: str):
    """Fetches comprehensive quarterly financial statements (Income statement, balance sheet, cash flow) for a given ticker."""
    try:
        
        data = await asyncio.to_thread(_fetch_yf_data, ticker)
        if not data:
            return f"⚠️ Yahoo Finance returned empty financial tables for {ticker}."
        return data
    except Exception as e:
        return f"⚠️ Error fetching financial tables: {str(e)}"

@tool
def serper_search(ticker: str):
    """Find general financial news about a stock using Google Search
    Args:
          ticker: The ticker of a company in order to find news about it """
    try:
        return serper.run(f"Find latest financial data, earnings, and news about {ticker} stock")
    except Exception as e:
        return f"⚠️ Google Search failed."


tools = [get_fin_data, serper_search, news_yh_search]