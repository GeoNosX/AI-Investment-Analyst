from langgraph.graph import StateGraph, START, END
from .nodes import data_fetch, process_tool_results, sum_fin_report, sentiment_analysis, report_analyst
from .state import Fin_State
from .tools import tools, tools_condition
from langgraph.prebuilt import ToolNode


builder = StateGraph(Fin_State)

builder.add_node('data_fetch', data_fetch)
builder.add_node('tools', ToolNode(tools=tools))
builder.add_node('process_tools', process_tool_results)
builder.add_node('sum_fin_report', sum_fin_report)
builder.add_node('sentiment_analysis', sentiment_analysis)
builder.add_node('report_analyst', report_analyst)

builder.add_edge(START, 'data_fetch')


builder.add_conditional_edges(
    'data_fetch',
    tools_condition,
    {
        "tools": "tools",
        END: "sum_fin_report"
    }
)


builder.add_edge('tools', 'process_tools')
builder.add_edge('process_tools', 'sum_fin_report')

builder.add_edge('sum_fin_report', 'sentiment_analysis')
builder.add_edge('sentiment_analysis', 'report_analyst')
builder.add_edge('report_analyst', END)

graph = builder.compile()