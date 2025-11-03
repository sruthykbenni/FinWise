# utils/llm_agent.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_groq_client():
    """Initialize and return Groq client."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY. Please add it to .env or Streamlit secrets.")
    return Groq(api_key=api_key)

def ask_llm(query: str, context: str) -> str:
    """Ask Groq Llama3 model using context for financial Q&A."""
    if not query.strip():
        return "⚠️ Please enter a valid question."
    if not context.strip():
        return "⚠️ No relevant data found to answer this question."

    prompt = f"""
You are FinWise — an intelligent AI-powered financial assistant.
Use the following context (transactions + documents) to answer precisely and professionally.

Context:
{context}

User question: {query}

Guidelines:
- Be clear and concise (3–4 sentences).
- Base answers on the given context.
- If information is incomplete, say “Based on available data...”
Answer:
"""

    try:
        client = get_groq_client()
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=512,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error calling Groq API: {str(e)}"
