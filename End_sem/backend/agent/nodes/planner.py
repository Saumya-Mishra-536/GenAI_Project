import json
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from agent.utils.llm import get_llm


def generate_plan(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Planner node with chain-of-thought prompting.
    Translates structured reasoning into an actionable infrastructure plan.
    """
    reasoning = state.get('reasoning', {})
    insights = state.get('insights', {})
    knowledge = state.get('retrieved_knowledge', [])

    system_msg = SystemMessage(content='''You are an elite EV Infrastructure Planner.
Translate the structured reasoning into a high-quality actionable plan.

THINK STEP BY STEP:
1. Review the observations and identify the most critical grid risks.
2. Cross-reference with the retrieved knowledge guidelines.
3. For each risk, formulate a specific, measurable recommendation.
4. Assign priorities based on severity and urgency.
5. Output the final plan.

You MUST output ONLY a valid JSON object with this EXACT schema:
{
  "high_load_locations": ["string"],
  "recommendations": [
    {
      "type": "charger_expansion | load_balancing | scheduling | battery_storage",
      "location": "string",
      "action": "clear specific step you are recommending",
      "justification": "explicit logical foundation",
      "priority": "high | medium | low"
    }
  ],
  "risk_level": "Low | Medium | High",
  "confidence_score": 0.95,
  "alternative_strategies": ["string"]
}

RULES:
- Provide at least 2 recommendations.
- Recommendations must be specific and actionable (include thresholds, times, hardware specs).
- No generic text like "optimize the grid" allowed.
- Must directly use reasoning outputs and knowledge context.
- DO NOT output any markdown tags or text outside of the JSON.''')

    user_content = (
        f"Reasoning Data:\n{json.dumps(reasoning, default=str)}\n\n"
        f"Demand Insights:\n{json.dumps(insights, default=str)}\n\n"
        f"Knowledge Context:\n{json.dumps(knowledge, default=str)}\n\n"
        "Generate the structured JSON plan."
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

        plan = json.loads(content.strip())

        if "confidence_score" not in plan:
            plan["confidence_score"] = float(reasoning.get("confidence", 0.5))

    except Exception as e:
        # Graceful fallback — no tracebacks leak to UI
        plan = {
            "high_load_locations": ["Station C — Primary Grid Node"],
            "recommendations": [
                {
                    "type": "load_balancing",
                    "location": "System Wide",
                    "action": "Halt automated deployment and initiate manual infrastructure review across all stations",
                    "justification": (
                        "AI architectural planning interrupted due to secure network timeout or "
                        "validation failure. Reserving final strategy to human override."
                    ),
                    "priority": "high"
                },
                {
                    "type": "battery_storage",
                    "location": "Highest-Load Station",
                    "action": "Pre-position 50kWh portable BESS to buffer peak demand until full analysis completes",
                    "justification": "Precautionary measure to prevent transformer overload during planning gap.",
                    "priority": "medium"
                }
            ],
            "risk_level": state.get("insights", {}).get("risk_level", "Unknown"),
            "confidence_score": 0.1,
            "alternative_strategies": [
                "Manual audit and human review",
                "Temporary dynamic pricing to shift load"
            ]
        }

    return {"final_plan": plan}
