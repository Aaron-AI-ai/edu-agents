from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage

from agents.base import BaseAgent
from agents.state import AgentState


class ResearcherAgent(BaseAgent):
    """Agent specialized in researching and gathering information."""

    def __init__(self, llm: BaseChatModel):
        super().__init__(llm, "researcher")

    @property
    def system_prompt(self) -> str:
        return """You are a research specialist for educational content.
Your role is to:
1. Analyze the user's question or topic
2. Provide well-researched, accurate information
3. Include relevant facts, definitions, and context
4. Cite concepts and explain their origins when relevant

Be thorough but concise. Focus on educational value.
Structure your response clearly with key points.

After providing research, summarize the key findings that other agents can use."""

    async def process(self, state: AgentState) -> dict:
        """Research the topic and provide information."""
        prompt = self.prompt.invoke({"messages": state.messages})
        response = await self.llm.ainvoke(prompt)

        # Store research in context
        context = state.context.copy()
        context["research"] = response.content

        return {
            "messages": [AIMessage(content=response.content, name=self.name)],
            "context": context,
            "next_agent": "supervisor",
        }


def create_researcher(llm: BaseChatModel) -> ResearcherAgent:
    """Factory function to create a researcher agent."""
    return ResearcherAgent(llm)
