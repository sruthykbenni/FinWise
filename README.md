# 💰 FinWise — AI-Powered Personal Financial Advisor

FinWise is an **AI-powered personal financial dashboard** and **RAG-based financial chatbot** built using **Streamlit**, **LangChain**, and **Plotly**.  
It helps users **analyze their spending patterns**, **visualize financial insights**, and **chat with an AI assistant** that understands both their personal transactions and real-world financial data.

---

## 🚀 Features

### 🔐 **User Authentication**
- Secure login and session management using `passlib` and `SQLAlchemy`
- Each user has a **personalized financial workspace**

### 📊 **Interactive Financial Dashboard**
- Upload your own **transaction CSV file** or use built-in sample data
- Auto-categorizes expenses and detects income intelligently
- Provides insights into:
  - **Monthly spending trends**
  - **Category-wise breakdown**
  - **Top merchants**
  - **Income, Expense, and Net Flow summaries**
- Dynamic visualizations built using **Plotly**

### 🧠 **AI Financial Chatbot (RAG-Enabled)**
- Uses **Retrieval-Augmented Generation (RAG)** with FAISS & Sentence Transformers  
- Understands both:
  - Your **uploaded transaction data**
  - **External financial documents** (seeded from credible public finance resources)
- Provides meaningful, data-grounded answers like:
  > “What were my biggest expenses last month?”  
  > “How can I save more based on my current spending pattern?”  
  > “Summarize my spending on transport this quarter.”

### 🗃️ **Smart Data Ingestion**
- Automatically parses transaction data in various formats  
  (e.g., Debit/Credit columns, unsigned Amounts, or different date formats)
- Integrates seamlessly into the RAG knowledge base

### 💡 **Tech Stack**
| Layer | Tools & Libraries |
|--------|-------------------|
| **Frontend** | Streamlit |
| **Backend Logic** | Python 3.11+, FastAPI (optional microservices) |
| **Database** | SQLite (via SQLAlchemy) |
| **Visualization** | Plotly |
| **AI/LLM** | LangChain + Sentence Transformers (`all-MiniLM-L6-v2`) |
| **Vector DB** | FAISS |
| **Authentication** | Passlib (bcrypt) |
| **Document Parsing** | PDFPlumber, Pandas |
| **Deployment** | Streamlit Cloud / Localhost |

---

## 🧩 Folder Structure

```

FinWise/
│
├── app.py                         # Streamlit main entry
├── requirements.txt               # Dependencies
│
├── data/
│   └── sample_transactions.csv    # Example dataset for demo
│
├── pages/
│   ├── 1_Dashboard.py             # Financial insights & charts
│   ├── 2_Chatbot.py               # AI chatbot interface
│   └── 3_Profile.py               # User reports & summaries
│
├── utils/
│   ├── auth.py                    # User login & authentication
│   ├── session_manager.py         # Session validation
│   ├── preprocessing.py           # Data cleaning & categorization
│   ├── analysis.py                # Spend, category, merchant analytics
│   ├── plotly_charts.py           # Plotly visualization helpers
│   ├── rag_setup.py               # RAG vector DB & embedding setup
│
└── rag/
├── seed_docs/                 # Seeded reference documents
└── vector_index.faiss         # Vector index file

````

---

## ⚙️ Installation & Setup

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/<your-username>/FinWise.git
cd FinWise
````

### 2️⃣ **Create a Virtual Environment**

```bash
python -m venv .venv
```

### 3️⃣ **Activate the Environment**

* On Windows:

  ```bash
  .venv\Scripts\activate
  ```
* On macOS/Linux:

  ```bash
  source .venv/bin/activate
  ```

### 4️⃣ **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 5️⃣ **Initialize the Database**

```bash
python - <<'PY'
from utils.auth import init_db, create_user
init_db()
create_user("demo_user", "DemoPass123")
print("✅ demo_user created successfully!")
PY
```

### 6️⃣ **Run the Application**

```bash
streamlit run app.py
```

### 7️⃣ **Login and Explore**

* Username: `demo_user`
* Password: `DemoPass123`

---

## 🧠 RAG Chatbot Data Flow

1. **User uploads financial data (CSV)**
   → Preprocessed & vectorized via `SentenceTransformer`.
2. **FAISS Index** stores embeddings locally.
3. **LLM (via LangChain)** retrieves top-k context snippets.
4. **Response generated** by combining user data + retrieved knowledge.

This ensures **context-aware, personalized financial insights** without relying solely on the model’s memory.

---

## 📈 Example Insights

| Query                                                 | AI Response (Example)                                                                   |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------- |
| *“What’s my biggest expense this month?”*             | “Your largest expense was ₹4,500 at Amazon on Sept 12.”                                 |
| *“Summarize my entertainment spending this quarter.”* | “You spent ₹2,850 on entertainment including Netflix and movie tickets.”                |
| *“How can I optimize my travel expenses?”*            | “Consider reducing Ola and Uber rides; 18% of your total expense comes from transport.” |

---

## 🧮 Sample Transaction Format

| Date       | Description          | Amount | Category      |
| ---------- | -------------------- | ------ | ------------- |
| 2025-09-01 | ACME Ltd Salary      | 25000  | Income        |
| 2025-09-02 | Uber Trip            | 250    | Transport     |
| 2025-09-03 | Supermarket ABC      | 650    | Groceries     |
| 2025-09-04 | Netflix Subscription | 499    | Entertainment |

---

## 🧠 LLMs & AI Integration

* Embedding Model: `sentence-transformers/all-MiniLM-L6-v2`
* Retrieval Engine: FAISS (local)
* LLM Options:

  * **Default:** HuggingFace LLM (no external API)
  * **Optional:** OpenAI GPT-4 / Gemini via LangChain integration
* RAG pipeline ensures factual, grounded answers using:

  * User’s transaction summaries
  * Seeded credible financial documents

---

## 🌐 Deployment

You can deploy FinWise on:

* **Streamlit Cloud** *(recommended for simplicity)*
* **Render / Railway / Hugging Face Spaces**
* Or a self-hosted VPS with FastAPI backend integration

---

## 📚 Future Enhancements

✅ Integration with bank APIs (Yodlee / Plaid)
✅ Expense forecasting using Prophet or LSTM
✅ Goal-based savings planner
✅ Multi-user analytics dashboard for CSR / corporate use
✅ PDF bank statement ingestion with auto-OCR

---

## 🧑‍💻 Author

**👩‍💻 Sruthy K Benni**
Passionate about AI and Data Science ⭐
[LinkedIn](https://www.linkedin.com/in/sruthy-k-benni) 

---

## 🪪 License

This project is licensed under the **MIT License** — feel free to use and modify it for personal or academic purposes.

---

## 🌟 Acknowledgments

* [Streamlit](https://streamlit.io)
* [LangChain](https://www.langchain.com/)
* [Sentence Transformers](https://www.sbert.net/)
* [Plotly](https://plotly.com/python/)
* [FAISS](https://github.com/facebookresearch/faiss)

---

