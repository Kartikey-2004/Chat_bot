import json

from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults

search = DuckDuckGoSearchResults(output_format="list")


@tool
def web_search(query: str) -> str:
    """Search the web for recent information."""
    if not query.strip():
        return json.dumps({"error": "Empty query"})

    try:
        results = search.invoke(query)
        formatted = [
            {
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
            }
            for item in results[:5]
        ]
        return json.dumps(formatted)
    except Exception as e:
        return json.dumps({"error": str(e)})
