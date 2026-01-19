from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage

from agents.base import BaseAgent
from agents.state import AgentState

AGENT_OPTIONS = ["researcher", "tutor", "quiz_master", "FINISH"]


class SupervisorAgent(BaseAgent):
    """Supervisor agent that routes tasks to specialized agents."""

    def __init__(self, llm: BaseChatModel):
        super().__init__(llm, "supervisor")

    @property
    def system_prompt(self) -> str:
        return """You are a supervisor managing a team of educational AI agents.
Your role is to analyze user requests and delegate tasks to the appropriate specialist.

Available agents:
- researcher: Gathers information and researches topics. Use for questions requiring factual information or research.
- tutor: Explains concepts and teaches. Use for learning requests, explanations, or understanding concepts.
- quiz_master: Creates quizzes and assessments. Use for testing knowledge or creating practice questions.
- FINISH: Use when the task is complete and ready to respond to the user.

Based on the conversation, decide which agent should handle the next step.
Respond with ONLY the agent name, nothing else."""

    async def process(self, state: AgentState) -> dict:
        """Route to the appropriate agent based on the conversation."""
        messages = state.messages

        # Build routing prompt
        prompt = self.prompt.invoke({"messages": messages})
        response = await self.llm.ainvoke(prompt)

        # Parse the response to get next agent
        next_agent = response.content.strip().lower()

        # Validate agent selection
        if next_agent not in [a.lower() for a in AGENT_OPTIONS]:
            next_agent = "tutor"  # Default to tutor

        return {
            "next_agent": next_agent,
            "iteration": state.iteration + 1,
        }


def create_supervisor(llm: BaseChatModel) -> SupervisorAgent:
    """Factory function to create a supervisor agent."""
    return SupervisorAgent(llm)
