from strands import tool

try:
    # Try new package name first
    from ddgs import DDGS
except ImportError:
    # Fall back to old package name for compatibility
    from duckduckgo_search import DDGS

@tool
def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web for information using DuckDuckGo.
    
    This tool allows the agent to search the internet and retrieve
    relevant information to answer user questions. It uses the official
    duckduckgo-search library for reliable and fast results.
    
    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 5, max: 10)
        
    Returns:
        Formatted search results as a string with titles, snippets, and URLs
        
    Example:
        result = web_search("Python programming tutorials", max_results=3)
        result = web_search("latest AI news")
    """
    try:
        # Limit max_results to reasonable range
        max_results = min(max(1, max_results), 10)
        
        # Initialize DuckDuckGo search
        with DDGS() as ddgs:
            # Perform text search
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return f"No results found for query: '{query}'"
        
        # Format results
        formatted_results = []
        for idx, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            body = result.get('body', 'No description available')
            url = result.get('href', '')
            
            result_text = f"{idx}. **{title}**\n"
            result_text += f"   {body}\n"
            if url:
                result_text += f"   URL: {url}\n"
            
            formatted_results.append(result_text)
        
        header = f"Found {len(results)} results for '{query}':\n\n"
        return header + "\n".join(formatted_results)
        
    except Exception as e:
        error_msg = str(e)
        # Provide helpful error messages
        if "ratelimit" in error_msg.lower():
            return f"Search rate limit reached. Please try again in a moment."
        elif "timeout" in error_msg.lower():
            return f"Search timed out for query: '{query}'. Please try again."
        else:
            return f"Error performing web search: {error_msg}"
