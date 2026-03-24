from typing import Annotated, List, Any, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


def merge_news(old: List[str], new: List[str]) -> List[str]:
    return list(set(old + new))

class Fin_State(TypedDict):
    ticker: str
    financials: str
    news: Annotated[List[str], merge_news]
    summary: str
    sentiment: str
    report: str
    messages: Annotated[List[BaseMessage], add_messages]