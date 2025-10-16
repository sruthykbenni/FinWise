# utils/llm_agent.py
import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource(show_spinner=False)
def get_openai_client():
    """Load OpenAI client with cached session."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY in .env or Streamlit secrets.")
    return OpenAI(api_key=api_key)

def ask_llm(query, context):
    """
    Ask the OpenAI LLM using retrieved context from RAG (user + external docs).
    Returns a natural, context-aware financial answer.
    """
    client = get_openai_client()
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
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return completion.choices[0].message.content.strip()
