class Fin_State(TypedDict):
    ticker: str
    financials: Annotated[str, LastValue]
    news: Annotated[List[str], "merge_list_handler"]
    summary: Annotated[str, LastValue]
    sentiment: Annotated[str, LastValue]
    report: Annotated[str, LastValue]
    messages: Annotated[List[Any], add_messages]