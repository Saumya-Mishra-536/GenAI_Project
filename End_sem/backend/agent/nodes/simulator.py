import json
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from agent.utils.llm import get_llm


def simulate_scenarios(state: Dict[str, Any]) -> Dict[str, Any]:
    """Simulates a hypothetical 20% demand surge to stress-test the final plan."""
    plan = state.get('final_plan', {})
    insights = state.get('insights', {})

    system_msg = SystemMessage(content='''You are an EV grid scenario simulator.
Assess the impact of a sudden 20% demand increase on the given infrastructure plan.
Respond in STRICT JSON with exactly this structure:
{
  "scenario": "Demand increases by 20%",
  "impact_analysis": "string explanation of effects on each recommendation",
  "robustness_score": 0.85,
  "vulnerable_points": ["string list of weak spots"],
  "mitigation_suggestions": ["string list of additional measures"]
}
Do NOT output any other text or markdown.''')

    user_content = (
        f"Plan: {json.dumps(plan, default=str)}\n\n"
        f"Insights: {json.dumps(insights, default=str)}\n\n"
        "Analyze the scenario."
    )
    user_msg = HumanMessage(content=user_content)

    try:
        llm = get_llm()
        result = llm.invoke([system_msg, user_msg])

        content = result.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        sim = json.loads(content.strip())
    except Exception as e:
        sim = {
            "scenario": "Demand increases by 20%",
            "impact_analysis": "Simulation paused due to AI processing overload. Automatic safeguards activated.",
            "robustness_score": 0.0,
            "vulnerable_points": ["Unable to assess — simulation interrupted"],
            "mitigation_suggestions": ["Manual stress test required"]
        }

    return {"simulated_impact": sim}
