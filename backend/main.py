from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from graph import app_graph
from fastapi.responses import StreamingResponse
import uvicorn

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
    
    initial_state = {
        "ticker": ticker,
        "financials": "",
        "news": [],
        "summary": "",
        "sentiment": "",
        "report": "",
        "messages": [HumanMessage(content=f"Analyze the stock {ticker} and provide a financial report.")]
    }
    
    
    async def event_generator():
        print(f"--- Starting analysis for: {ticker} ---")
        
        
        async for msg, metadata in app_graph.astream(initial_state, stream_mode="messages"):
            
            if metadata.get("langgraph_node") == "report_analyst":
                if msg.content:
                    
                    print(msg.content, end="", flush=True) 
                    yield str(msg.content)

    
    return StreamingResponse(event_generator(), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    