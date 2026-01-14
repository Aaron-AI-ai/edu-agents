from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Agent service starting...")
    yield
    # Shutdown
    print("Agent service shutting down...")


app = FastAPI(
    title="Edu Agents - Agent Service",
    description="AI Agent API Service",
    version="0.1.0",
    lifespan=lifespan,
)


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # TODO: Implement agent logic
    return ChatResponse(
        response=f"Echo: {request.message}",
        conversation_id=request.conversation_id or "new-conversation",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
