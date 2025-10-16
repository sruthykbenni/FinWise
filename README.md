# 💰 FinWise — AI-Powered Personal Financial Advisor

FinWise is an **AI-powered personal financial dashboard** and **RAG-based financial chatbot** built using **Streamlit**, **LangChain**, **OpenAI API**, and **Plotly**.  
It helps users **analyze their spending patterns**, **visualize insights**, and **chat with an intelligent assistant** that understands both their personal financial data and reliable financial sources online.

---

## 🚀 Features

### 🔐 **User Authentication (users.db)**
- Secure user management handled via **SQLite database (`users.db`)**
- Passwords are **hashed with bcrypt** using `passlib`
- Persistent sessions and validation handled by `session_manager.py`
- Preloaded with a default demo user for quick login

### 📊 **Financial Dashboard**
- Upload your transaction data (CSV) or load a demo dataset
- Auto-categorizes transactions into meaningful groups (Food, Rent, Salary, Transport, etc.)
- Calculates **Income, Expense, and Net Flow** dynamically per month
- Visual insights using **Plotly**:
  - Monthly spending trends  
  - Category breakdown  
  - Top merchants  

### 🧠 **AI Financial Chatbot (RAG + OpenAI GPT-4)**
- Built using **LangChain** + **FAISS** + **OpenAI API**
- Uses **Retrieval-Augmented Generation (RAG)** to ensure factual, data-based responses
- Understands:
  - Your **uploaded transaction data**
  - **Seeded financial documents** (e.g., RBI guidelines, investment guides, personal finance best practices)
- Example queries:
  > “What were my biggest expenses last month?”  
  > “Summarize my income vs expenses this quarter.”  
  > “How can I save more based on my transaction patterns?”  
  > “Explain what mutual funds are, based on RBI/SEBI guidelines.”

### 🗃️ **Smart Data Handling**
- Works with various bank export formats (Debit/Credit, Amount-only, etc.)
- Automatically detects date and amount columns
- Categorizes expenses and incomes intelligently

### 🧮 **Visualization & Insights**
- Beautiful Plotly dashboards  
- Real-time calculations for monthly insights  
- Trendline comparison between months

---

## 🧠 **Architecture Overview**

```
              ┌─────────────────────────────────┐
              │      User Transaction Data      │
              └──────────────┬──────────────────┘
                             │
                Preprocessing & Categorization
                             │
           ┌───────────────────────────────────────┐
           │ FAISS Vector Store (Local Embeddings) │
           └───────────────────────────────────────┘
                             │
                        RAG Retriever
                             │
                     Context Sent to LLM
                             │
              ┌────────────────────────────────┐
              │  OpenAI GPT-4 (via LangChain)  │
              └────────────────────────────────┘
                             │
                      Smart AI Response
```

---

## ⚙️ **Installation & Setup**

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

### 4️⃣ Add Your OpenAI API Key

Create a `.env` file in the project root and add:

```
OPENAI_API_KEY=your_openai_api_key_here
```

You can get your API key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).

### 5️⃣ Initialize the User Database

```bash
python - <<'PY'
from utils.auth import init_db, create_user
init_db()
create_user("demo_user", "DemoPass123")
print("✅ demo_user created successfully!")
PY
```
This creates:
- A SQLite database file: users.db
- A users table with hashed passwords and session support

### 6️⃣ Run the App

```bash
streamlit run app.py
```

Then log in using:

* Username: `demo_user`
* Password: `DemoPass123`

---

## 🧩 Folder Structure

```
FinWise/
│
├── app.py                         # Main Streamlit entry
├── requirements.txt               # Dependencies
├── .env                           # Stores OpenAI API Key
│
├── pages/
│   ├── 1_Dashboard.py             # Analytics dashboard
│   ├── 2_Chatbot.py               # Chatbot interface
│   └── 3_Profile.py               # User summary page
│
├── utils/
│   ├── auth.py                    # Authentication
│   ├── session_manager.py         # Session validation
│   ├── preprocessing.py           # Data cleaning
│   ├── analysis.py                # Financial calculations
│   ├── plotly_charts.py           # Charts and visuals
│   ├── rag_setup.py               # RAG embedding + retrieval
│
├── vector_index.faiss             # FAISS index file
├── index_meta.pkl                 # Metadata for RAG
│
└── data/
    ├── sample_transactions.csv    # Example dataset
    └── seed_docs/                 # Standard financial references
```

---

## 🧠 **RAG + OpenAI Integration Details**

* **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
* **Vector Database**: FAISS (in-memory index)
* **LLM Backend**: OpenAI GPT-4 via LangChain
* **Retriever Chain**: Context-aware querying from both user and reference data

This setup ensures:

* Reliable, **fact-grounded answers**
* Personalized responses using **your financial history**
* Support for **financial advice, summaries, and planning**

---

## 📈 Example Queries

| User Query                                                | Example AI Response                                                                                                                                 |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| “Summarize my income and expense for September.”          | “You earned ₹25,000 and spent ₹18,400, resulting in a net savings of ₹6,600.”                                                                       |
| “What are my top 3 spending categories?”                  | “Food & Dining (35%), Transport (22%), and Groceries (18%).”                                                                                        |
| “Explain SIP investments using reliable finance sources.” | “A Systematic Investment Plan (SIP) allows you to invest in mutual funds periodically. It helps with rupee cost averaging, as per SEBI guidelines.” |

---

## 🌐 Deployment Options

* [Streamlit Cloud](https://streamlit.io/cloud)
* Render / Railway / Hugging Face Spaces
* Self-hosted on VPS with `uvicorn` + FastAPI microservices (optional)

---

## 📚 Future Enhancements

✅ Integration with live banking APIs (Plaid / Yodlee)
✅ Expense forecasting using ML models (Prophet / LSTM)
✅ Voice-based financial assistant
✅ PDF bank statement auto-parsing
✅ Investment portfolio optimization module

---

## 🧑‍💻 Author

👩‍💻 Sruthy K Benni
[LinkedIn](https://www.linkedin.com/in/sruthy-k-benni)

---

## 🪪 License

This project is licensed under the **MIT License** — free for personal, research, and educational use.

---

## 🌟 Acknowledgments

* [OpenAI API](https://platform.openai.com/)
* [LangChain](https://www.langchain.com/)
* [Sentence Transformers](https://www.sbert.net/)
* [FAISS](https://github.com/facebookresearch/faiss)
* [Streamlit](https://streamlit.io)
* [Plotly](https://plotly.com/python/)

---
