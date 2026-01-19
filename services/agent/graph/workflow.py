from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

from agents import (
    AgentState,
    create_quiz_master,
    create_researcher,
    create_supervisor,
    create_tutor,
)
from config.llm import get_llm
from config.settings import get_settings


def create_workflow(llm: BaseChatModel | None = None) -> StateGraph:
    """Create the multi-agent workflow graph.

    Args:
        llm: Optional LLM instance. If not provided, uses default from settings.

    Returns:
        Compiled workflow graph.
    """
    if llm is None:
        llm = get_llm()

    settings = get_settings()

    # Create agents
    supervisor = create_supervisor(llm)
    researcher = create_researcher(llm)
    tutor = create_tutor(llm)
    quiz_master = create_quiz_master(llm)

    # Build the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("supervisor", supervisor.invoke)
    workflow.add_node("researcher", researcher.invoke)
    workflow.add_node("tutor", tutor.invoke)
    workflow.add_node("quiz_master", quiz_master.invoke)

    # Define routing logic
    def route_supervisor(state: AgentState) -> str:
        """Route based on supervisor's decision."""
        next_agent = state.next_agent.lower()

        # Check for completion
        if next_agent == "finish":
            return END

        # Check iteration limit
        if state.iteration >= settings.max_iterations:
            return END

        # Route to appropriate agent
        if next_agent in ["researcher", "tutor", "quiz_master"]:
            return next_agent

        # Default to tutor
        return "tutor"

    # Add edges
    workflow.set_entry_point("supervisor")

    workflow.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {
            "researcher": "researcher",
            "tutor": "tutor",
            "quiz_master": "quiz_master",
            END: END,
        },
    )

    # All agents return to supervisor for next decision
    workflow.add_edge("researcher", "supervisor")
    workflow.add_edge("tutor", "supervisor")
    workflow.add_edge("quiz_master", "supervisor")

    return workflow.compile()


async def run_workflow(
    message: str,
    conversation_history: list | None = None,
    llm: BaseChatModel | None = None,
) -> dict:
    """Run the multi-agent workflow with a user message.

    Args:
        message: User's input message.
        conversation_history: Optional list of previous messages.
        llm: Optional LLM instance.

    Returns:
        Dictionary containing the response and updated state.
    """
    workflow = create_workflow(llm)

    # Build initial messages
    messages = []
    if conversation_history:
        messages.extend(conversation_history)
    messages.append(HumanMessage(content=message))

    # Create initial state
    initial_state = AgentState(
        messages=messages,
        current_task=message,
    )

    # Run the workflow
    config = {"recursion_limit": get_settings().recursion_limit}
    final_state = await workflow.ainvoke(initial_state, config=config)

    return {
        "response": final_state.get("final_response", ""),
        "messages": final_state.get("messages", []),
        "context": final_state.get("context", {}),
        "generated_content": final_state.get("generated_content", {}),
    }
