# 💬 Transaction Query RAG with Ollama + Mistral

This project lets you run **local, private financial queries** over your transactions using **RAG (Retrieval-Augmented Generation)** with **Ollama** and **Mistral**.

---

## 🛠 Setup Instructions

### 1. Install Ollama
Download and install Ollama from [https://ollama.com/download](https://ollama.com/download).

Start the Ollama server:

```bash
ollama serve
```

### 2. Pull the Mistral Model

Pull the Mistral model locally:

```bash
ollama pull mistral
```

### 3. Set up Python Environment

Create and activate a virtual environment:

```bash
python3 -m venv ollama-env
source ollama-env/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Required libraries:
- pandas
- chromadb
- sentence-transformers
- ollama

(Alternatively, you can install them manually.)

---

## 🗂️ Prepare Your Transactions CSV

Make sure your `your_transactions.csv` is in the project folder.

Expected columns:

```
Transaction Date, Post Date, Description, Category, Type, Amount, Memo
```

Example row:

```csv
04/03/2025,04/04/2025,HARBOR FREIGHT TOOLS3541,Shopping,Sale,-7.71,
```

---

## 🚀 Run the Project

```bash
python query-rag.py
```

Then type queries like:

- "Sum all DoorDash transactions."
- "How much did I spend in Groceries?"
- "What was refunded from Amazon?"

The model retrieves only relevant transactions and answers intelligently.

---

## 📦 Notes
- Runs **fully locally** (no cloud).
- Supports **multi-turn conversations** (chat memory).
- Handles thousands of transactions efficiently.

---

## 📜 License
MIT License
