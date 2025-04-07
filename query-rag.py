import pandas as pd
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import ollama

# Load transactions from CSV
csv_file = "your_transactions.csv"  # <<< Replace with your actual CSV path
df = pd.read_csv(csv_file)

# Create clean text for each transaction (includes Description, Transaction Date, Category, Type, Amount)
texts = [
    f"{row['Description']} on {row['Transaction Date']} in category {row['Category']} type {row['Type']} amount {row['Amount']}"
    for idx, row in df.iterrows()
]

# Embed transactions
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = embed_model.encode(texts)

# Create ChromaDB in-memory
db = chromadb.Client(Settings(anonymized_telemetry=False))
collection = db.create_collection("transactions")

# Add transactions to Chroma
for i, (text, embedding) in enumerate(zip(texts, embeddings)):
    collection.add(
        documents=[text],
        embeddings=[embedding.tolist()],
        ids=[str(i)]
    )

print(f"✅ Loaded and embedded {len(texts)} transactions.")

# Initialize conversation history
messages = []

# Start dynamic query loop
while True:
    user_query = input("\n❓ Ask a question about your transactions (or type 'exit' to quit): ")
    
    if user_query.lower() in ['exit', 'quit']:
        print("👋 Exiting. Bye!")
        break

    # Embed user query
    query_embedding = embed_model.encode([user_query])

    # Retrieve relevant transactions
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=200
    )

    relevant_transactions = results["documents"][0]

    if not relevant_transactions:
        print("⚠️ No relevant transactions found.")
        continue

    # Print retrieved transactions
    print("\n📄 Retrieved Transactions:")
    for idx, txn in enumerate(relevant_transactions, 1):
        print(f"{idx}. {txn}")

    # Build final prompt
    context = "\n".join(relevant_transactions)
    final_prompt = f"""
You are given a list of transactions:
{context}

{user_query}

Answer clearly and directly. If a sum is requested, provide only the number.
"""

    # Update conversation history
    messages.append({"role": "user", "content": final_prompt})

    # Query Ollama model
    response = ollama.chat(model="mistral", messages=messages)

    # Print model's answer
    print(f"\n🧠 Answer: {response['message']['content']}")

    # Save model's response to conversation history
    messages.append({"role": "assistant", "content": response['message']['content']})
