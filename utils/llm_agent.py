# utils/llm_agent.py

import os
import streamlit as st
from openai import OpenAI
from groq import Groq

def get_openai_client():
    """Create OpenAI client using the latest key from sidebar or env."""
    api_key = (
        st.session_state.get("OPENAI_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )
    if not api_key:
        raise ValueError("⚠️ Missing OpenAI API key.")
    return OpenAI(api_key=api_key)

def get_groq_client():
    """Create Groq client using the latest key from sidebar or env."""
    api_key = (
        st.session_state.get("GROQ_API_KEY")
        or os.getenv("GROQ_API_KEY")
    )
    if not api_key:
        return None
    return Groq(api_key=api_key)

def ask_llm(user_query, context_text):
    """
    Handles the logic for querying the LLM.
    - Uses OpenAI GPT-4o-mini as default.
    - Falls back to Groq if OpenAI fails or limit reached.
    """
    try:
        openai_client = get_openai_client()
    except Exception as e:
        st.error(f"⚠️ OpenAI key error: {e}")
        openai_client = None

    groq_client = get_groq_client()

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

    # --- Try OpenAI First ---
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
            st.warning(f"⚠️ OpenAI API error: {openai_error}")

    # --- Fallback to Groq ---
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
            return f"⚠️ Groq API error: {groq_error}"

    return "⚠️ No valid API keys found. Please enter them in the sidebar."

