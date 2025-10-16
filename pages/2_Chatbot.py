# pages/2_Chatbot.py
import streamlit as st
from utils.rag_setup import get_rag_index
from utils.llm_agent import ask_llm

st.set_page_config(page_title="FinWise Chatbot", layout="wide")

st.title("💬 FinWise Financial Assistant")

st.markdown("""
Ask anything about your financial data or general finance topics.
Your chatbot combines your uploaded transactions with standard financial documents for accurate, context-aware answers.
""")

query = st.text_area("Enter your question:", placeholder="e.g. Summarize my top expenses this month")

if st.button("Get Answer") and query.strip():
    with st.spinner("Analyzing your financial data..."):
        rag = get_rag_index()
        results = rag.query(query, top_k=5)
        context = "\n\n".join([r["text"] for r in results])
        sources = list({r["source"] for r in results})

        if not context:
            st.warning("No relevant data found yet. Try uploading transactions or ingesting seed docs.")
        else:
            answer = ask_llm(query, context)
            st.markdown("### 🧠 Answer")
            st.write(answer)

            st.markdown("**Sources Used:**")
            for s in sources:
                st.markdown(f"- {s}")
