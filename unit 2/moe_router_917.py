"""
Unit 2 Assignment: Mixture of Experts (MoE) Router
Topic: Advanced Architecture using Groq API
Student ID: PES2UG23CS917
"""

import os
import sys
import getpass
from typing import Tuple, Any
from groq import Groq
from dotenv import load_dotenv

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------
BASE_MODEL = "llama-3.3-70b-versatile"

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key or api_key.strip() == "your_groq_api_key_here":
    try:
        api_key = getpass.getpass("Enter your Groq API Key: ")
    except:
        pass

if not api_key or not api_key.strip():
    print("Error: Groq API key is required.")
    sys.exit(1)

client = Groq(api_key=api_key.strip())

# ---------------------------------------------------
# Expert Configurations
# ---------------------------------------------------
MODEL_CONFIG = {
    "technical": {
        "system_prompt": """You are a highly skilled Technical Support Expert.
Analyze code errors precisely and provide:
- Root cause
- Working solution with code
- Prevention tips""",
        "temperature": 0.7
    },
    "billing": {
        "system_prompt": """You are an empathetic Billing Support Expert.
Always:
- Acknowledge concern
- Explain billing clearly
- Provide resolution within policy""",
        "temperature": 0.7
    },
    "sales": {
        "system_prompt": """You are an enthusiastic Sales Expert.
Always:
- Highlight product benefits
- Guide customer toward best plan
- Encourage conversion""",
        "temperature": 0.7
    },
    "general": {
        "system_prompt": """You are a helpful and friendly assistant.
Handle casual conversation and general questions politely.""",
        "temperature": 0.7
    }
}

# ---------------------------------------------------
# BONUS TOOL FUNCTION
# ---------------------------------------------------
def fetch_bitcoin_price() -> dict:
    """Mock Bitcoin price fetcher"""
    return {"price": "$45,230", "currency": "USD", "source": "mock_exchange"}


TOOL_CONFIG = {
    "crypto_expert": {
        "keywords": ["bitcoin", "ethereum", "crypto", "price", "cryptocurrency"],
        "function": fetch_bitcoin_price,
        "system_prompt": """You are a Cryptocurrency Expert.
Use the provided tool data to give accurate insights."""
    }
}

# ---------------------------------------------------
# ROUTER (temperature = 0)
# ---------------------------------------------------
def route_prompt(user_input: str) -> str:

    routing_prompt = f"""
Classify this customer query into ONE category:
- technical
- billing
- sales
- general

Query: {user_input}

Return ONLY one word.
"""

    response = client.chat.completions.create(
        model=BASE_MODEL,
        messages=[{"role": "user", "content": routing_prompt}],
        temperature=0,
        max_tokens=5
    )

    category = response.choices[0].message.content.strip().lower()

    valid = ["technical", "billing", "sales", "general"]
    if category in valid:
        return category

    return "general"

# ---------------------------------------------------
# TOOL DETECTION
# ---------------------------------------------------
def check_for_tool_use(user_input: str) -> Tuple[bool, str, Any]:
    user_lower = user_input.lower()

    for keyword in TOOL_CONFIG["crypto_expert"]["keywords"]:
        if keyword in user_lower:
            result = TOOL_CONFIG["crypto_expert"]["function"]()
            return True, "crypto_expert", result

    return False, "", None

# ---------------------------------------------------
# ORCHESTRATOR
# ---------------------------------------------------
def process_request(user_input: str) -> dict:

    requires_tool, tool_name, tool_result = check_for_tool_use(user_input)

    if requires_tool:
        category = tool_name
        system_prompt = TOOL_CONFIG[tool_name]["system_prompt"]
        final_prompt = f"{user_input}\n\nTool Data: {tool_result}"
        temperature = 0.7
    else:
        category = route_prompt(user_input)
        expert_config = MODEL_CONFIG.get(category, MODEL_CONFIG["general"])
        system_prompt = expert_config["system_prompt"]
        final_prompt = user_input
        temperature = expert_config["temperature"]

    response = client.chat.completions.create(
        model=BASE_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": final_prompt}
        ],
        temperature=temperature,
        max_tokens=1024
    )

    expert_response = response.choices[0].message.content

    return {
        "user_input": user_input,
        "category": category,
        "tool_used": requires_tool,
        "tool_name": tool_name if requires_tool else None,
        "tool_result": tool_result if requires_tool else None,
        "expert_response": expert_response
    }

# ---------------------------------------------------
# DEMO
# ---------------------------------------------------
def main():

    print("=" * 70)
    print("Mixture of Experts (MoE) Router Demo")
    print("=" * 70)

    test_queries = [
        "My python script is throwing an IndexError on line 5.",
        "I was charged twice for my subscription.",
        "Do you offer enterprise pricing?",
        "Hello, how are you?",
        "What is the current price of Bitcoin?"
    ]

    for i, query in enumerate(test_queries, 1):
        print("\n" + "-" * 70)
        print(f"Test Case {i}")
        print("-" * 70)

        result = process_request(query)

        print(f"User Input: {query}")
        print(f"Routing Decision: {result['category']}")

        if result["tool_used"]:
            print(f"Tool Used: {result['tool_name']}")
            print(f"Tool Result: {result['tool_result']}")

        print("\nExpert Response:")
        print(result["expert_response"])

    print("\n" + "=" * 70)
    print("Demo Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()