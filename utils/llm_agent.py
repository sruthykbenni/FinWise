# utils/llm_agent.py

import os
import streamlit as st
from openai import OpenAI
from groq import Groq

# ✅ Load API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ✅ Cache clients to avoid reloading every time
@st.cache_resource(show_spinner=False)
def get_openai_client():
    return OpenAI(api_key=OPENAI_API_KEY)

@st.cache_resource(show_spinner=False)
def get_groq_client():
    if GROQ_API_KEY:
        return Groq(api_key=GROQ_API_KEY)
    return None

def ask_llm(user_query, context_text):
    """
    Handles the logic for querying the LLM.
    - Uses OpenAI GPT-4o-mini as default.
    - Falls back to Groq if OpenAI fails or limit reached.
    """
    openai_client = get_openai_client()
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

    try:
        # --- Try OpenAI first ---
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

        # --- Try Groq as fallback ---
        if groq_client:
            try:
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI financial assistant."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.3,
                    max_tokens=512,
                )
                return response.choices[0].message.content.strip()

            except Exception as groq_error:
                print(f"⚠️ Groq API fallback error: {groq_error}")
                return "⚠️ Sorry, the language model service is temporarily unavailable. Please try again later."
        else:
            return "⚠️ Unable to connect to the language model. Please check your API keys."

