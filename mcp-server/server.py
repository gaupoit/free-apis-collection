#!/usr/bin/env python3
"""
Free APIs MCP Server

An MCP server that provides AI agents access to 50+ free APIs.
Agents can discover APIs, get details, and call no-auth endpoints directly.
"""

import json
import httpx
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("free-apis")

# Load APIs data
APIS_FILE = Path(__file__).parent.parent / "apis.json"

def load_apis() -> dict:
    """Load APIs from JSON file."""
    with open(APIS_FILE) as f:
        return json.load(f)

def get_all_apis() -> list[dict]:
    """Get flat list of all APIs with category info."""
    data = load_apis()
    apis = []
    for category in data["categories"]:
        for api in category["apis"]:
            apis.append({
                **api,
                "category": category["name"],
                "categorySlug": category["slug"]
            })
    return apis


@mcp.tool()
def list_categories() -> str:
    """List all API categories available in the collection.

    Returns a list of categories with their names and API counts.
    Use this to discover what types of APIs are available.
    """
    data = load_apis()
    categories = []
    for cat in data["categories"]:
        categories.append({
            "name": cat["name"],
            "slug": cat["slug"],
            "apiCount": len(cat["apis"])
        })
    return json.dumps(categories, indent=2)


@mcp.tool()
def list_apis(category: str = None, auth_required: bool = None) -> str:
    """List APIs, optionally filtered by category or auth requirement.

    Args:
        category: Filter by category slug (e.g., 'weather', 'finance', 'fun')
        auth_required: If False, only show APIs that don't require authentication

    Returns a list of APIs with their details.
    """
    apis = get_all_apis()

    if category:
        apis = [a for a in apis if a["categorySlug"] == category.lower()]

    if auth_required is not None:
        if auth_required:
            apis = [a for a in apis if a["auth"] != "none"]
        else:
            apis = [a for a in apis if a["auth"] == "none"]

    # Simplify output
    result = []
    for api in apis:
        result.append({
            "name": api["name"],
            "description": api["description"],
            "category": api["category"],
            "auth": api["auth"],
            "testUrl": api.get("testUrl"),
            "url": api["url"]
        })

    return json.dumps(result, indent=2)


@mcp.tool()
def get_api(name: str) -> str:
    """Get detailed information about a specific API.

    Args:
        name: The name of the API (case-insensitive)

    Returns full details including URL, auth type, and test URL if available.
    """
    apis = get_all_apis()

    for api in apis:
        if api["name"].lower() == name.lower():
            return json.dumps(api, indent=2)

    return json.dumps({"error": f"API '{name}' not found"})


@mcp.tool()
def call_api(url: str, method: str = "GET") -> str:
    """Call a free API endpoint and return the response.

    Only works with APIs that don't require authentication.
    Use list_apis(auth_required=False) to find callable APIs.

    Args:
        url: The API endpoint URL to call
        method: HTTP method (GET, POST). Defaults to GET.

    Returns the API response as JSON or text.
    """
    try:
        with httpx.Client(timeout=10.0) as client:
            if method.upper() == "GET":
                response = client.get(url)
            elif method.upper() == "POST":
                response = client.post(url)
            else:
                return json.dumps({"error": f"Unsupported method: {method}"})

            response.raise_for_status()

            # Try to parse as JSON
            try:
                return json.dumps(response.json(), indent=2)
            except json.JSONDecodeError:
                return response.text[:5000]  # Limit text response

    except httpx.TimeoutException:
        return json.dumps({"error": "Request timed out"})
    except httpx.HTTPStatusError as e:
        return json.dumps({"error": f"HTTP {e.response.status_code}: {e.response.text[:500]}"})
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def search_apis(query: str) -> str:
    """Search for APIs by name or description.

    Args:
        query: Search term to find in API names or descriptions

    Returns matching APIs.
    """
    apis = get_all_apis()
    query_lower = query.lower()

    matches = []
    for api in apis:
        if (query_lower in api["name"].lower() or
            query_lower in api["description"].lower()):
            matches.append({
                "name": api["name"],
                "description": api["description"],
                "category": api["category"],
                "auth": api["auth"],
                "testUrl": api.get("testUrl")
            })

    return json.dumps(matches, indent=2)


@mcp.tool()
def get_random_api(no_auth_only: bool = True) -> str:
    """Get a random API from the collection.

    Great for discovering new APIs or testing.

    Args:
        no_auth_only: If True, only return APIs that don't require auth

    Returns a random API with its details.
    """
    import random

    apis = get_all_apis()

    if no_auth_only:
        apis = [a for a in apis if a["auth"] == "none"]

    if not apis:
        return json.dumps({"error": "No APIs match the criteria"})

    api = random.choice(apis)
    return json.dumps({
        "name": api["name"],
        "description": api["description"],
        "category": api["category"],
        "auth": api["auth"],
        "url": api["url"],
        "testUrl": api.get("testUrl")
    }, indent=2)


@mcp.tool()
def quick_test(api_name: str) -> str:
    """Quickly test an API by calling its test URL.

    Only works for APIs with a testUrl defined (no-auth APIs).

    Args:
        api_name: Name of the API to test

    Returns the API response.
    """
    apis = get_all_apis()

    for api in apis:
        if api["name"].lower() == api_name.lower():
            test_url = api.get("testUrl")
            if not test_url:
                return json.dumps({
                    "error": f"No test URL available for {api['name']}",
                    "hint": "This API may require authentication. Check the main URL."
                })

            return call_api(test_url)

    return json.dumps({"error": f"API '{api_name}' not found"})


if __name__ == "__main__":
    mcp.run()
