import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from config import get_settings
from graph import run_workflow


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    settings = get_settings()
    print(f"Agent service starting... (LLM: {settings.default_llm_provider})")
    yield
    print("Agent service shutting down...")


app = FastAPI(
    title="Edu Agents - Multi-Agent Service",
    description="Educational AI Multi-Agent API powered by LangGraph",
    version="0.1.0",
    lifespan=lifespan,
)


class ChatRequest(BaseModel):
    """Chat request model."""

    message: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    """Chat response model."""

    response: str
    conversation_id: str
    context: dict | None = None


# Simple in-memory conversation store (replace with proper storage in production)
conversations: dict[str, list] = {}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "edu-agents-agent"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message through the multi-agent system."""
    try:
        # Get or create conversation
        conversation_id = request.conversation_id or str(uuid.uuid4())
        history = conversations.get(conversation_id, [])

        # Run the workflow
        result = await run_workflow(
            message=request.message,
            conversation_history=history,
        )

        # Update conversation history
        conversations[conversation_id] = result.get("messages", [])

        # Get response
        response_text = result.get("response", "")
        if not response_text:
            # Fallback to last assistant message
            messages = result.get("messages", [])
            for msg in reversed(messages):
                if hasattr(msg, "content") and getattr(msg, "type", None) == "ai":
                    response_text = msg.content
                    break

        return ChatResponse(
            response=response_text or "I couldn't generate a response. Please try again.",
            conversation_id=conversation_id,
            context=result.get("context"),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {e!s}")


@app.delete("/conversations/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """Clear a conversation's history."""
    if conversation_id in conversations:
        del conversations[conversation_id]
        return {"status": "cleared", "conversation_id": conversation_id}
    raise HTTPException(status_code=404, detail="Conversation not found")


@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history."""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = conversations[conversation_id]
    return {
        "conversation_id": conversation_id,
        "message_count": len(messages),
        "messages": [
            {"role": getattr(m, "type", "unknown"), "content": m.content}
            for m in messages
            if hasattr(m, "content")
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
