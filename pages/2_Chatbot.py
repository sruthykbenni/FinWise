# pages/2_Chatbot.py
import streamlit as st
from utils.llm_agent import ask_llm
from utils.rag_setup import get_rag_index

st.set_page_config(page_title="FinWise Chatbot", page_icon="🤖", layout="wide")

st.markdown("<h2 style='text-align:center;'>🤖 FinWise Chat Assistant</h2>", unsafe_allow_html=True)
st.write("Ask me about your spending habits, budgets, or any transaction insights!")

rag = get_rag_index()

# --- Initialize Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Chat Input UI ---
user_query = st.chat_input("Type your message here...")

if user_query:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)

    # --- Retrieve relevant context using RAG ---
    similar_docs = rag.query(user_query, top_k=5)
    context_text = "\n".join([d.get("text", "") for d in similar_docs]) if similar_docs else ""

    # --- Generate chatbot response ---
    with st.spinner("Thinking..."):
        try:
            bot_response = ask_llm(user_query, context_text)
        except Exception as e:
            bot_response = f"⚠️ Error generating response: {e}"

    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(bot_response)

    # Save chat history
    st.session_state.chat_history.append({"user": user_query, "bot": bot_response})

# --- Display Chat History ---
if st.session_state.chat_history:
    with st.expander("🕓 View Chat History"):
        for i, chat in enumerate(st.session_state.chat_history, 1):
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**FinWise:** {chat['bot']}")
            st.markdown("---")

# --- Sidebar Information ---
st.sidebar.markdown("### 💡 FinWise AI Chatbot")
st.sidebar.info(
    "FinWise uses your transaction history and embedded documents to answer "
    "personal finance questions. Ask me anything related to your spending, income, or budget!"
)
st.sidebar.markdown("✅ Powered by OpenAI GPT-4o-mini (with Groq fallback)")

