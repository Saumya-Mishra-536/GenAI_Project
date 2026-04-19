from agent.graph import build_graph


def run_planning_agent(df):
    """
    Entry point for the agentic planning pipeline.
    Accepts a processed DataFrame and returns the full agent state.
    """
    app = build_graph()
    initial_state = {
        "df_raw": df,
        "insights": {},
        "patterns": {},
        "retrieved_knowledge": [],
        "reasoning": {},
        "final_plan": {},
        "feedback": "",
        "iteration_count": 0,
        "simulated_impact": {}
    }

    result = app.invoke(initial_state)
    return result
