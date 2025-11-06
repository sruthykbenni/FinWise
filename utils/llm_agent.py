# utils/llm_agent.py

import os
import streamlit as st
from openai import OpenAI
from groq import Groq

# ✅ Dynamically fetch API keys each time (to allow sidebar updates)
def get_api_keys():
    openai_key = os.getenv("OPENAI_API_KEY") or st.session_state.get("OPENAI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY") or st.session_state.get("GROQ_API_KEY")
    return openai_key, groq_key

# ✅ Cache clients separately to improve efficiency
@st.cache_resource(show_spinner=False)
def get_openai_client(api_key):
    return OpenAI(api_key=api_key)

@st.cache_resource(show_spinner=False)
def get_groq_client(api_key):
    if api_key:
        return Groq(api_key=api_key)
    return None

def ask_llm(user_query, context_text):
    """
    Handles the logic for querying the LLM.
    - Uses Groq (Gemma-7B-IT) as primary for fast, free inference.
    - Falls back to OpenAI GPT-4o-mini when Groq fails or key not provided.
    """

    OPENAI_API_KEY, GROQ_API_KEY = get_api_keys()
    openai_client = get_openai_client(OPENAI_API_KEY) if OPENAI_API_KEY else None
    groq_client = get_groq_client(GROQ_API_KEY) if GROQ_API_KEY else None

    # Build prompt
    prompt = f"""
    You are FinWise — a helpful, reliable financial assistant chatbot.
    Use the context below to answer the user's query clearly and concisely.

    Context:
    {context_text}

    User Query:
    {user_query}

    Answer professionally and in simple terms.
    """

    # --- Prefer GROQ first ---
    if groq_client:
        try:
            response = groq_client.chat.completions.create(
                model="gemma-7b-it",
                messages=[
                    {"role": "system", "content": "You are a helpful AI financial assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=512,
            )
            return response.choices[0].message.content.strip()
        except Exception as groq_error:
            print(f"⚠️ Groq API error: {groq_error}")

    # --- Fallback to OpenAI ---
    if openai_client:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful AI financial assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=512,
            )
            return response.choices[0].message.content.strip()
        except Exception as openai_error:
            print(f"⚠️ OpenAI API error: {openai_error}")

    # --- If both fail ---
    return "⚠️ Sorry, both AI services are unavailable right now. Please check your API keys and try again later."
