from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage

from agents.base import BaseAgent
from agents.state import AgentState


class TutorAgent(BaseAgent):
    """Agent specialized in teaching and explaining concepts."""

    def __init__(self, llm: BaseChatModel):
        super().__init__(llm, "tutor")

    @property
    def system_prompt(self) -> str:
        return """You are an expert tutor and educator.
Your role is to:
1. Explain concepts clearly and thoroughly
2. Use analogies and examples to aid understanding
3. Break down complex topics into digestible parts
4. Adapt explanations to the student's level
5. Encourage questions and curiosity

Teaching style:
- Start with the big picture, then dive into details
- Use real-world examples when possible
- Highlight common misconceptions
- Provide practice opportunities when appropriate

If research context is available, incorporate it into your explanation.

Research context: {context}"""

    @property
    def prompt(self):
        """Override to include context in prompt."""
        from langchain_core.prompts import ChatPromptTemplate

        if self._prompt is None:
            self._prompt = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("placeholder", "{messages}"),
            ])
        return self._prompt

    async def process(self, state: AgentState) -> dict:
        """Provide tutoring and explanations."""
        # Include research context if available
        context_str = state.context.get("research", "No additional context available.")

        prompt = self.prompt.invoke({
            "messages": state.messages,
            "context": context_str,
        })
        response = await self.llm.ainvoke(prompt)

        return {
            "messages": [AIMessage(content=response.content, name=self.name)],
            "final_response": response.content,
            "next_agent": "supervisor",
        }


def create_tutor(llm: BaseChatModel) -> TutorAgent:
    """Factory function to create a tutor agent."""
    return TutorAgent(llm)
