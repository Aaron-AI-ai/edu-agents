import json

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage

from agents.base import BaseAgent
from agents.state import AgentState


class QuizMasterAgent(BaseAgent):
    """Agent specialized in creating quizzes and assessments."""

    def __init__(self, llm: BaseChatModel):
        super().__init__(llm, "quiz_master")

    @property
    def system_prompt(self) -> str:
        return """You are a quiz master and assessment specialist.
Your role is to:
1. Create educational quizzes and assessments
2. Design questions that test understanding, not just memorization
3. Provide a mix of question types (multiple choice, short answer, etc.)
4. Include explanations for correct answers

When creating a quiz:
- Start with easier questions and progress to harder ones
- Cover key concepts from the topic
- Make wrong answers plausible but clearly incorrect
- Provide helpful feedback for each answer

Format your quiz clearly with numbered questions.
After each question, provide the correct answer and a brief explanation.

If context is available, base questions on that content.

Context: {context}"""

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
        """Create a quiz based on the conversation context."""
        context_str = state.context.get("research", "No additional context available.")

        prompt = self.prompt.invoke({
            "messages": state.messages,
            "context": context_str,
        })
        response = await self.llm.ainvoke(prompt)

        # Store generated quiz
        generated = state.generated_content.copy()
        generated["quiz"] = response.content

        return {
            "messages": [AIMessage(content=response.content, name=self.name)],
            "generated_content": generated,
            "final_response": response.content,
            "next_agent": "supervisor",
        }


def create_quiz_master(llm: BaseChatModel) -> QuizMasterAgent:
    """Factory function to create a quiz master agent."""
    return QuizMasterAgent(llm)
