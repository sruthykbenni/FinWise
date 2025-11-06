# 💰 FinWise: AI-Powered Personal Financial Advisor

FinWise is an **AI-powered personal financial dashboard** and **RAG-based financial chatbot** built using **Streamlit**, **LangChain**, **OpenAI GPT-4o-mini**, **FAISS**, and **Plotly**.  
It helps users **analyze spending patterns**, **visualize insights**, and **chat with an intelligent assistant** that understands both their personal financial data and reliable financial sources.

🔗 **Live Demo:** [https://finwise-gen-ai.streamlit.app/](https://finwise-gen-ai.streamlit.app/)

---

## 🚀 Features

### 🔐 User Authentication
- Secure user login and signup with **SQLite (`users.db`)**
- Passwords hashed using **bcrypt + passlib**
- Persistent session validation via `session_manager.py`
- Demo user available for quick access

### 📊 Financial Dashboard
- Upload your transaction CSV or load a demo dataset
- Auto-categorizes transactions (Food, Rent, Salary, etc.)
- Calculates **Income, Expense, and Net Flow** per month
- Plotly visualizations for:
  - Monthly spending trends  
  - Category breakdown  
  - Top merchants  

### 🧠 AI Financial Chatbot (RAG + GPT-4o-mini)
- Powered by **Retrieval-Augmented Generation (RAG)**  
- Uses **OpenAI GPT-4o-mini** primarily, with **Groq fallback (llama-3.1-8b-instant)**
- Retrieves context from:
  - Uploaded transactions  
  - Seeded financial PDFs or text files (e.g., RBI/SEBI docs)
- Supports live API key entry via sidebar
- Example queries:
  > “What were my biggest expenses last month?”  
  > “Summarize my income vs expenses this quarter.”  
  > “How can I reduce my transport costs?”  
  > “Explain SIPs based on RBI guidelines.”

### 🗃️ Smart Data Handling
- Works with various bank export formats  
- Automatically detects and standardizes columns  
- Intelligent expense categorization  

### 🧮 Visualization & Insights
- Real-time Plotly dashboards  
- Income vs Expense trend analysis  
- Monthly summaries and reports  

---

## 🧠 Architecture Overview


          ┌──────────────────────────────┐
          │  User Transaction Data (CSV) │
          └──────────────┬───────────────┘
                         │
           Preprocessing & Categorization
                         │
             ┌───────────────────────────┐
             │ FAISS Vector Index (RAG)  │
             └───────────────────────────┘
                         │
                  Context Retrieval
                         │
    ┌───────────────────────────────────────────┐
    │  OpenAI GPT-4o-mini + Groq (Fallback)     │
    └───────────────────────────────────────────┘
                         │
                  Personalized Insight



---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/FinWise.git
cd FinWise
````

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
# or
source .venv/bin/activate    # macOS/Linux
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Add API Keys

Create a `.env` file in your project root and add:

```
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_optional_groq_api_key_here
```

You can also enter these dynamically in the sidebar while the app runs.

**Primary model:** GPT-4o-mini (OpenAI)
**Fallback model:** LLaMA-3.1-8B-Instant (Groq)

### 5️⃣ Initialize Database

```bash
python - <<'PY'
from utils.auth import init_db, create_user
init_db()
create_user("demo_user", "DemoPass123")
print("✅ demo_user created successfully!")
PY
```

### 6️⃣ Run the App

```bash
streamlit run app.py
```

Login credentials:

```
Username: demo_user
Password: DemoPass123
```

---

## 🧩 Folder Structure

```
FinWise/
│
├── app.py                       # Main Streamlit entry
├── requirements.txt             # Dependencies
├── .env                         # API keys
│
├── pages/
│   ├── 0_Home.py                # Home navigation page
│   ├── 1_Dashboard.py           # Financial analytics
│   ├── 2_Chatbot.py             # RAG chatbot with API key input
│   └── 3_Profile.py             # User profile & reports
│
├── utils/
│   ├── auth.py                  # Authentication logic
│   ├── session_manager.py       # Session handling
│   ├── preprocessing.py         # Data cleaning
│   ├── analysis.py              # Financial computations
│   ├── plotly_charts.py         # Plotly visuals
│   ├── rag_setup.py             # FAISS + embeddings
│   └── llm_agent.py             # GPT-4o-mini + Groq logic
│
├── data/
│   ├── sample_transactions.csv  # Demo data
│   └── seed_docs/               # RBI/SEBI reference PDFs
│
├── vector_index.faiss           # FAISS index
└── index_meta.pkl               # Metadata for RAG
```

---

## 🧠 RAG + LLM Integration

| Component         | Description                                |
| ----------------- | ------------------------------------------ |
| **Embeddings**    | `sentence-transformers/all-MiniLM-L6-v2`   |
| **Vector Store**  | FAISS                                      |
| **Primary Model** | GPT-4o-mini (OpenAI)                       |
| **Fallback**      | LLaMA-3.1-8B-Instant (Groq)                |
| **Retriever**     | Context from transactions + reference PDFs |

This enables:

* Fact-grounded, data-driven financial insights
* Personalized answers from your actual data
* Resilience to API limits with multi-model fallback

---

## 📈 Example Queries

| User Query                                        | Example Response                                                                                        |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| “Summarize my income and expenses for September.” | “You earned ₹25,000 and spent ₹18,400 — net savings ₹6,600.”                                            |
| “Top 3 spending categories?”                      | “Food (35%), Transport (22%), and Groceries (18%).”                                                     |
| “Explain SIPs in mutual funds.”                   | “A SIP allows periodic mutual fund investments and helps average market costs, as per SEBI guidelines.” |

---

## 🌐 Deployment

* **Streamlit Cloud** *(recommended)*
* Render / Railway / Hugging Face Spaces
* Self-hosted with FastAPI + Uvicorn

---

## 📚 Future Enhancements

✅ Voice-based assistant
✅ Predictive expense forecasting (Prophet / LSTM)
✅ PDF statement parsing
✅ Investment portfolio analytics
✅ Multi-user cloud version

---

## 👩‍💻 Author

**Sruthy K Benni**
*MSc Computer Science (Data Analytics)*
🔗 [LinkedIn](https://www.linkedin.com/in/sruthy-k-benni)

---

## 🪪 License

Licensed under the **MIT License** — free for personal, research, and educational use.

---

## 🌟 Acknowledgments

* [OpenAI API](https://platform.openai.com/)
* [Groq API](https://console.groq.com/docs/overview)
* [LangChain](https://www.langchain.com/)
* [Sentence Transformers](https://www.sbert.net/)
* [FAISS](https://github.com/facebookresearch/faiss)
* [Streamlit](https://streamlit.io)
* [Plotly](https://plotly.com/python/)

```

---

Would you like me to generate a **short GitHub project description (2–3 lines)** you can paste under the repository name too? It’ll make your repo stand out immediately when viewed.
```
