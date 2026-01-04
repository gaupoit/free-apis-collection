# AI Agent Instructions

This document provides instructions for AI agents (Claude, GPT, Copilot, etc.) to effectively use this free APIs collection.

## Quick Start for Agents

You have access to **52 free APIs** across 10 categories. Many require no authentication and can be called directly.

### Categories Available
- `weather` - Weather data
- `finance` - Crypto prices, exchange rates
- `entertainment` - Movies, jokes, trivia, quotes
- `data` - Countries, demographics, fake users
- `fun` - Random facts, advice, yes/no
- `development` - Testing APIs, IP lookup
- `science` - NASA, SpaceX, books, dictionary
- `location` - Postal codes, flight tracking
- `food` - Recipes, cocktails, nutrition
- `animals` - Dog/cat/fox images

## Using the MCP Server

If the MCP server is configured, use these tools:

### Discovery Tools
```
list_categories()          # See all categories
list_apis(category="fun")  # APIs in a category
list_apis(auth_required=False)  # No-auth APIs only
search_apis("weather")     # Search by keyword
get_api("CoinDesk")        # Get API details
get_random_api()           # Discover something new
```

### Calling APIs
```
quick_test("Dog CEO")      # Test an API instantly
call_api("https://api.ipify.org?format=json")  # Call any URL
```

## Direct Usage (No MCP)

If you don't have MCP access, use these URLs directly:

### Instant Test URLs (No Auth Required)

```bash
# Random dog image
GET https://dog.ceo/api/breeds/image/random

# Random joke
GET https://official-joke-api.appspot.com/random_joke

# Bitcoin price
GET https://api.coindesk.com/v1/bpi/currentprice.json

# Random activity suggestion
GET https://www.boredapi.com/api/activity

# Get IP address
GET https://api.ipify.org?format=json

# Random user data
GET https://randomuser.me/api/

# Country information
GET https://restcountries.com/v3.1/name/canada

# Age prediction from name
GET https://api.agify.io?name=michael

# Random fox image
GET https://randomfox.ca/floof/

# Yes/No with GIF
GET https://yesno.wtf/api

# Random quote
GET https://api.quotable.io/random

# Postal code lookup
GET https://api.zippopotam.us/us/90210
```

## Common Agent Tasks

### "Get me a random image"
```
Use: Dog CEO, RandomFox, or Shibe.online
URL: https://dog.ceo/api/breeds/image/random
```

### "Tell me a joke"
```
Use: Official Joke API or JokeAPI
URL: https://official-joke-api.appspot.com/random_joke
```

### "What's the Bitcoin price?"
```
Use: CoinDesk
URL: https://api.coindesk.com/v1/bpi/currentprice.json
```

### "Generate fake user data"
```
Use: RandomUser
URL: https://randomuser.me/api/
```

### "I'm bored, suggest something"
```
Use: Bored API
URL: https://www.boredapi.com/api/activity
```

### "Look up country information"
```
Use: REST Countries
URL: https://restcountries.com/v3.1/name/{country}
```

### "Get trivia questions"
```
Use: Open Trivia DB
URL: https://opentdb.com/api.php?amount=5
```

## Response Handling Tips

1. **JSON Responses**: Most APIs return JSON. Parse and extract relevant fields.
2. **Rate Limits**: Be respectful. Don't spam requests.
3. **Error Handling**: Check for HTTP errors before parsing.
4. **CORS**: All listed APIs support CORS for browser use.

## Data File Location

Full API data available at: `apis.json`

```json
{
  "meta": { "totalApis": 52, "lastUpdated": "..." },
  "categories": [
    {
      "name": "Category",
      "slug": "category-slug",
      "apis": [{ "name", "url", "description", "auth", "testUrl" }]
    }
  ]
}
```

## Example Agent Workflow

```
User: "Show me something fun"

Agent thinking:
1. Check fun/entertainment categories
2. Pick a no-auth API (Bored API, Joke API, etc.)
3. Call the API
4. Present results to user

Agent action:
GET https://www.boredapi.com/api/activity

Response:
{
  "activity": "Learn a new programming language",
  "type": "education",
  "participants": 1
}

Agent response:
"Here's a fun suggestion: Learn a new programming language!
It's an educational activity you can do solo."
```

## Adding to Your Agent

### Claude Code MCP Setup
```bash
claude mcp add free-apis -- python /path/to/mcp-server/server.py
```

### Generic MCP Config
```json
{
  "mcpServers": {
    "free-apis": {
      "command": "python",
      "args": ["/path/to/mcp-server/server.py"]
    }
  }
}
```
