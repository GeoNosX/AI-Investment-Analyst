from state import Fin_State
from tools import tools
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, ToolMessage
from llm import llm
from prompts import report_analyst_system_prompt

llm_with_tools = llm.bind_tools(tools)


async def data_fetch(state: Fin_State):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an AI financial analyst. You MUST use the available tools to gather:
        - Financial statements (balance sheet, cash flow) for {ticker} using the 'get_fin_data' tool.
        - Latest news and market sentiment for {ticker} using 'serper_search' or 'news_yh_search'.
        
        Return the tool calls necessary to get this information. Do not output the final report yet."""),
        ("human", "Gather complete financial data and latest news for {ticker} stock.")
    ])

    chain = prompt | llm_with_tools
    response = await chain.ainvoke({"ticker": state["ticker"]})

    return {"messages": [response]}


async def process_tool_results(state: Fin_State) -> Fin_State:
    messages = state["messages"]
    new_fin = state.get("financials", "")
    new_news = state.get("news", [])

    for m in reversed(messages):
        if isinstance(m, ToolMessage):
            if m.name == 'get_fin_data':
                new_fin = m.content
            elif m.name in ['news_yh_search', 'serper_search']:
                if m.content not in new_news:
                    new_news.append(m.content)
        elif isinstance(m, AIMessage):
            break
            
    return {"financials": new_fin, "news": new_news}


async def sum_fin_report(state: Fin_State) -> Fin_State:
    fin_data = state.get('financials', 'No financial data available.')

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a financial analyst that summarizes financial data."),
        ('user', "Make a summary about this company's financial data:\n\n{fin_data}")
    ])

    chain = prompt | llm
    response = await chain.ainvoke({"fin_data": fin_data})
    return {"summary": response.content}


async def sentiment_analysis(state: Fin_State) -> Fin_State:
    news_list = state.get('news', [])
    news_text = '\n'.join(news_list) if news_list else "No recent news found."

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a news sentiment analyst. Classify news as positive, neutral, or negative."),
        ("user", "Analyze sentiment of the following news articles:\n\n{news}")
    ])

    chain = prompt | llm
    response = await chain.ainvoke({'news': news_text})
    return {"sentiment": response.content}

async def report_analyst(state: Fin_State) -> Fin_State:
    prompt = ChatPromptTemplate.from_messages([
        ("system", report_analyst_system_prompt),
        ("user", """DATA CONTEXT:

        --- RAW FINANCIALS ---
        {financials}

        --- NEWS SENTIMENT ---
        {sentiment}

        --- SUMMARY NOTES ---
        {summary}

        Create the final Institutional Investment Report now.""")
    ])

    chain = prompt | llm
    response = await chain.ainvoke(state)
    return {"report": response.content, "messages": [response]}