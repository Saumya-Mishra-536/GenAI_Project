from agent.utils.vector_store import get_retriever
from typing import Dict, Any

def retrieve_knowledge(state: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieves relevant knowledge from the FAISS vector store using RAG."""
    insights = state.get('insights', {})
    patterns = state.get('patterns', {})

    query = (
        f"Risk Level: {insights.get('risk_level', 'Unknown')}. "
        f"Peak Hours: {insights.get('peak_hours', [])}. "
        f"Repeated Congestion: {patterns.get('repeated_congestion', 'Unknown')}. "
        f"Grid Impact: {patterns.get('grid_stability_impact', 'Unknown')}. "
        f"Max Demand: {insights.get('max_demand', 'Unknown')} kW. "
    )

    try:
        retriever = get_retriever()
        docs = retriever.invoke(query)
        retrieved_content = [
            doc.page_content.replace("\\n", " ").strip()
            for doc in docs
        ]
        if not retrieved_content:
            retrieved_content = ["Core knowledge unavailable. Processing via LLM generalization defaults."]
    except Exception as e:
        retrieved_content = [
            "Knowledge retrieval interrupted. Establishing generic safe operational baseline for grid planning."
        ]

    return {"retrieved_knowledge": retrieved_content}
