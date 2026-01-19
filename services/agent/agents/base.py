from abc import ABC, abstractmethod

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from agents.state import AgentState


class BaseAgent(ABC):
    """Base class for all agents in the multi-agent system."""

    def __init__(self, llm: BaseChatModel, name: str):
        self.llm = llm
        self.name = name
        self._prompt: ChatPromptTemplate | None = None

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass

    @property
    def prompt(self) -> ChatPromptTemplate:
        """Get or create the chat prompt template."""
        if self._prompt is None:
            self._prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("placeholder", "{messages}"),
            ])
        return self._prompt

    @abstractmethod
    async def process(self, state: AgentState) -> dict:
        """Process the current state and return updates.

        Args:
            state: Current workflow state.

        Returns:
            Dictionary of state updates.
        """
        pass

    async def invoke(self, state: AgentState) -> dict:
        """Invoke the agent with error handling.

        Args:
            state: Current workflow state.

        Returns:
            Dictionary of state updates.
        """
        try:
            return await self.process(state)
        except Exception as e:
            return {
                "messages": [
                    {"role": "assistant", "content": f"Error in {self.name}: {e!s}"}
                ],
                "next_agent": "supervisor",
            }
