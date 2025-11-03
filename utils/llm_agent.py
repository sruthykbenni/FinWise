# utils/llm_agent.py
import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource(show_spinner=False)
def get_groq_client():
    """Load Groq client with cached session."""
    api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY in .env or Streamlit secrets.")
    return Groq(api_key=api_key)

def ask_llm(query, context):
    """
    Ask the Groq Llama3 model using retrieved financial context.
    Returns a concise, professional financial insight.
    """
    client = get_groq_client()
    prompt = f"""
You are FinWise — an intelligent AI-powered personal financial advisor.
Use the provided context (user's transactions and financial documents) to respond professionally.

Context:
{context}

User question:
{query}

Guidelines:
- Be concise but insightful (2–4 sentences).
- When data relates to spending, summarize or compute simple insights (totals, categories).
- If data is missing, respond gracefully ("Based on available information...").
- Do not repeat the context or file names in the answer.
Answer:
"""

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return completion.choices[0].message.content.strip()
