import requests
from langchain_core.tools import tool
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_community.utilities import GoogleSerperAPIWrapper
import yfinance as yf
from dotenv import load_dotenv

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
        # THE SAFETY NET
        return "⚠️ Yahoo Finance news is currently unavailable due to rate limits. Please rely on the 'serper_search' tool for news."

@tool
def get_fin_data(ticker: str):
    """Fetches financial data for a given ticker."""
    try:
        # We pass the 'safe_session' disguise into the Ticker!
        stock = yf.Ticker(ticker, session=safe_session)
        
        data = stock.info 
        
        # Sometimes Yahoo soft-blocks by returning empty data instead of an error
        if not data or len(data) <= 1:
            return f"⚠️ Yahoo Finance returned empty data for {ticker}. Please rely on general knowledge and serper_search."
            
        return str(data)
    except Exception as e:
        # THE SAFETY NET
        return "⚠️ Yahoo Finance is currently rate-limiting us. Please skip the detailed financials and write the report based on general knowledge."

@tool
def serper_search(ticker: str):
    """Find general financial news about a stock using Google Search
    Args:
          ticker: The ticker of a company in order to find news about it """
    try:
        return serper.run(f"Find latest financial data, earnings, and news about {ticker} stock")
    except Exception as e:
        return f"⚠️ Google Search failed."

tools = [serper_search]