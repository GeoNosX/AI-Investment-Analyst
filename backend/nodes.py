from .state import Fin_State
from .tools import tools
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, ToolMessage
from .llm import llm


            

llm_with_tools = llm.bind_tools(tools)
def data_fetch(state: Fin_State):
    """
    Decides which tools to call.
    Removed FetcherOutput and with_structured_output.
    Now simply returns the AI message with tool_calls.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an AI financial analyst. You MUST use the available tools to gather:
        - Financial statements (balance sheet, cash flow) for {ticker} using the 'get_fin_data' tool.
        - Latest news for {ticker} using 'serper_search' or 'news_yh_search'.

        Return the tool calls necessary to get this information. Do not output the final report yet."""),
        ("human", "Gather complete financial data and latest news for {ticker} stock.")
    ])

    chain = prompt | llm_with_tools
    response = chain.invoke({"ticker": state["ticker"]})

    return {"messages": [response]}

def process_tool_results(state: Fin_State) -> Fin_State:
    """
    Extracts data from ToolMessages and updates the specific state keys
    (financials, news) so the summarizer can use them easier.
    """
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

def sum_fin_report(state: Fin_State) -> Fin_State:

    fin_data = state.get('financials', 'No financial data available.')

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a financial analyst that summarizes financial data."),
        ('user', f"Make a summary about this company's financial data:\n\n{fin_data}")
    ])

    chain = prompt | llm
    summary = chain.invoke(state).content
    return {"summary": summary}

def sentiment_analysis(state: Fin_State) -> Fin_State:
    news_list = state.get('news', [])
    news_text = '\n'.join(news_list) if news_list else "No recent news found."

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a news sentiment analyst. Classify news as positive, neutral, or negative."),
        ("user", "Analyze sentiment of the following news articles:\n\n{news}")
    ])

    chain = prompt | llm
    sentiment = chain.invoke({'news': news_text}).content
    return {"sentiment": sentiment}

def report_analyst(state: Fin_State) -> Fin_State:

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Senior Investment Analyst (CFA) at a top-tier hedge fund.
        Your goal is to produce a deep-dive, institutional-grade investment memorandum.

        ### Tone & Style Guidelines:
        - **Professional:** Use Wall Street terminology (e.g., "YOY growth," "margin expansion," "solvency ratios").
        - **Data-Driven:** Avoid vague adjectives. Back every claim with a specific number or percentage.
        - **Visuals:** You MUST use Markdown tables to present financial data. Text should analyze the tables, not repeat them.

        ### Required Structure:

        1. **Executive Summary**: A high-level synthesis of the investment thesis (Bull/Bear/Neutral).

        2. **Financial Matrices (Markdown Tables)**:
           - **Income Statement Highlights**: Revenue, Gross Profit, Net Income, EPS (Last 3 periods if available).
           - **Balance Sheet Health**: Cash, Total Assets, Total Liabilities, Debt-to-Equity Ratio.
           - **Cash Flow Analysis**: Operating Cash Flow, CapEx, Free Cash Flow.

        3. **Sentiment & Market Context**: Analyze the provided news sentiment. Are market expectations aligned with fundamentals?

        4. **Key Risks & Catalysts**:
           - **Downside Risks**: What could break the thesis?
           - **Upside Catalysts**: What could drive the stock higher?

        5. **Final Verdict**: Clear Buy/Hold/Sell recommendation with a price target justification (based on P/E or growth).
        """),
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
    report = chain.invoke(state).content
    return {"report": report}