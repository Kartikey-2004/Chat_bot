from typing import List, Dict
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults

search = DuckDuckGoSearchResults(output_format="list")


@tool
def web_search(query: str) -> list[dict]:
    """
    Search the web for recent information.
    """
    if not query.strip():
        return [{"error": "Empty query"}]

    try:
        results = search.invoke(query)
        formatted_results = []
        for item in results[:5]:
            formatted_results.append(
                {
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet"),
                }
            )
        return formatted_results
    except Exception as e:
        return [{"error": str(e)}]
