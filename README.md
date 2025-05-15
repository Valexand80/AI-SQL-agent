#  AI SQL Agent (Natural Language to SQL)

This project is a natural language interface for querying a MySQL database using OpenAI’s GPT-3.5 Turbo.  
You can type plain English questions, and the app will generate and run valid SQL queries, then return results in a readable table.

---

## 📸 Screenshot

![Demo Screenshot](Streamlit_SQL.jpg)

---

## 🚀 Features

- 🔍 Natural language input → SQL query generation
- 🤖 GPT-3.5 Turbo via OpenAI API
- 🗄️ Connects to a live MySQL database (local or cloud)
- 📊 Results displayed in a Streamlit web interface
- 🔐 Environment variables keep credentials secure

---

## 📂 Folder Contents

- `streamlit_app.py` – Streamlit interface for running the agent
- `notebook.ipynb` – Development notebook with code and schema tests
- `agent.env` – **(not included)** Local secrets
- `.env.example` – Template for environment variables
- `screenshot.jpg` – Example of the app in action

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-sql-agent.git
cd ai-sql-agent
