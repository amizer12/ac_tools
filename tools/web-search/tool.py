from strands import tool
import requests
from bs4 import BeautifulSoup

@tool
def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web for information using DuckDuckGo.
    
    This tool allows the agent to search the internet and retrieve
    relevant information to answer user questions.
    
    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 5)
        
    Returns:
        Formatted search results as a string
        
    Example:
        result = web_search("Python programming tutorials", max_results=3)
    """
    try:
        # Use DuckDuckGo HTML search (no API key required)
        search_url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML results
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # Find result divs
        result_divs = soup.find_all('div', class_='result')[:max_results]
        
        for idx, result_div in enumerate(result_divs, 1):
            # Extract title
            title_elem = result_div.find('a', class_='result__a')
            # Extract snippet
            snippet_elem = result_div.find('a', class_='result__snippet')
            
            if title_elem and snippet_elem:
                title = title_elem.get_text(strip=True)
                snippet = snippet_elem.get_text(strip=True)
                url = title_elem.get('href', '')
                
                # Format result
                result_text = f"{idx}. **{title}**\n"
                result_text += f"   {snippet}\n"
                result_text += f"   URL: {url}\n"
                results.append(result_text)
        
        if results:
            header = f"Found {len(results)} results for '{query}':\n\n"
            return header + "\n".join(results)
        else:
            return f"No results found for query: '{query}'"
            
    except requests.exceptions.Timeout:
        return f"Search timed out for query: '{query}'. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error performing web search: {str(e)}"
    except Exception as e:
        return f"Unexpected error during web search: {str(e)}"
