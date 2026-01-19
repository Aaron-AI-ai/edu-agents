from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """Shared state for multi-agent workflow."""

    # Conversation messages with reducer for appending
    messages: Annotated[list[BaseMessage], add_messages] = Field(default_factory=list)

    # Current task/query being processed
    current_task: str = ""

    # Which agent should handle next (for routing)
    next_agent: str = ""

    # Collected context/research data
    context: dict = Field(default_factory=dict)

    # Generated content (quiz questions, explanations, etc.)
    generated_content: dict = Field(default_factory=dict)

    # Iteration count for loop control
    iteration: int = 0

    # Final response to user
    final_response: str = ""

    class Config:
        arbitrary_types_allowed = True
