from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid
from langchain_core.messages import HumanMessage

app = FastAPI(title="AI Investment Analyst API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/analyze/{ticker}')
async def analyze_stock(ticker: str):
    initial_state = {"ticker": ticker,
                     "messages":
                     [HumanMessage(content=f"Analyze the stock {ticker} and provide a financial report.")]}
    
    