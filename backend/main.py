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
        # Instantly show the user that the system is alive
        yield f"**Initializing Institutional Analysis for {ticker}...**\n\n"
        
        try:
            # We are using stream_mode="updates" to stream the steps instead of tokens
            async for event in app_graph.astream(initial_state, stream_mode="updates"):
                
                # event.items() gives us the node that just finished
                for node_name, node_state in event.items():
                    # Stream the progress to the chat UI!
                    yield f"✅ Completed calculation step: **{node_name}**...\n"
                    
                    # Once the final node finishes, stream the complete markdown report!
                    if node_name == "report_analyst":
                        yield "\n\n---\n\n" # A nice line separator
                        yield node_state["report"]
                        
        except Exception as e:
            yield f"\n\n⚠️ SYSTEM ERROR: The backend crashed. Error: {str(e)}"

    return StreamingResponse(event_generator(), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)