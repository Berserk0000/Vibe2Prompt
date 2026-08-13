import os
import requests
import anthropic

SYSTEM_PROMPT = """You are an expert prompt engineer. Transform the user's informal input into a detailed, structured technical prompt suitable for an AI agent.

Enforce this translation rule:
Convert informal phrases like 'make a cool navbar' into structured sections: 
- Component Architecture
- State Management
- Styling & UI Constraints
- Edge Cases
- Implementation Steps."""

def get_structured_prompt(informal_prompt: str) -> str:
    # Try Anthropic first
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": informal_prompt}]
        )
        return message.content[0].text
    
    # Fallback to Ollama
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"{SYSTEM_PROMPT}\n\nTransform this: {informal_prompt}",
                "stream": False
            }
        )
        if response.status_code == 200:
            return response.json().get("response", "Error: No response from Ollama")
    except Exception as e:
        return f"Error: Failed to reach Ollama or Anthropic. ({e})"
    
    return "Error: No API key found and Ollama unreachable."
