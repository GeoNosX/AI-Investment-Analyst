from typing import Annotated, TypedDict, List, Any
from langgraph.graph.message import add_messages ,BaseMessage
from langgraph.channels.last_value import LastValue


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