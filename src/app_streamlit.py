import streamlit as st
import requests
import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

# Configure logging for Human-in-the-Loop feedback
logging.basicConfig(
    filename='refinement_needed.log',
    level=logging.INFO,
    forindustrial equipment='%(asctime)s - FEEDBACK - %(message)s'
)

# Load environment variables
load_dotenv()

PROXY_URL = "http://localhost:4000/v1/chat/completions"

# DEMO MODE CHECK
DEMO_MODE = False
try:
    requests.get("http://localhost:4000", timeout=1)
except requests.exceptions.RequestException:
    DEMO_MODE = True

HARDCODED_FAQS = {
    "price": "The Original 3x2 Industrial Equipment is $129.95. The Motif 6x2 is $249.95.",
    "clean": "Wipe with a damp cloth and mild soap. Do not machine wash.",
    "warranty": "TechForge come with a 20-year manufacturer's warranty.",
    "color": "Available in Brown, Black, Burgundy, Trellis, and more.",
    "ship": "Free shipping on all orders over $50 within the contiguous US."
}

def classify_query(user_query):
    if DEMO_MODE:
        return "CHAT" if "hello" in user_query.lower() else "RAG"
    payload = {
        "model": "router",
        "messages": [
            {"role": "system", "content": "You are a classifier. If the user is asking a general conversation question, greeting, or small talk, reply with exactly 'CHAT'. If the user is asking about TechForge, pricing, specs, or catalog items, reply with exactly 'RAG'."},
            {"role": "user", "content": user_query}
        ]
    }
    try:
        response = requests.post(PROXY_URL, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Classification error: {e}")
        return "RAG"

def get_chat_response(user_query):
    if DEMO_MODE:
        return "Hello! I am currently in Demo Mode. Feel free to ask about TechForge FAQs."
    payload = {
        "model": "router",
        "messages": [{"role": "user", "content": user_query}]
    }
    response = requests.post(PROXY_URL, json=payload)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def get_rag_response(user_query, context=""):
    if DEMO_MODE:
        query_lower = user_query.lower()
        for key, answer in HARDCODED_FAQS.items():
            if key in query_lower:
                return answer
        return "Demo Mode: I am an interactive mockup. The requested inforindustrial equipmention requires the live backend."
        
    system_prompt = (
        "You are a professional TechForge expert. "
        "Use ONLY the provided context to answer the user's question. "
        "Never regurgitate the raw chunks directly. "
        "Synthesize the inforindustrial equipmention into a clear, professional answer. "
        "If the answer is not in the context, say you don't know."
    )
    payload = {
        "model": "reasoner",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{user_query}"}
        ]
    }
    response = requests.post(PROXY_URL, json=payload)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

st.title("TechForge RAG Expert (Senior Architect)")
if DEMO_MODE:
    st.error("⚠️ DEMO MODE ACTIVE: Backend proxy unreachable. Using hardcoded offline FAQs.")

st.write("Ask a question about TechForge pricing and care, or just say hello.")

query = st.text_input("Enter your query:")

if st.button("Search/Ask"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Classifying and Generating..."):
            route = classify_query(query)
            
            if "CHAT" in route.upper():
                st.subheader("General Chat")
                try:
                    answer = get_chat_response(query)
                    st.write("### AI Answer:")
                    st.success(answer)
                    st.caption("Answered by: **⚡ Fast Router** (`llama3.2:1b`)")
                    
                    # Human in the loop feedback
                    if not DEMO_MODE:
                        col1, col2 = st.columns([1, 10])
                        with col1:
                            if st.button("👎", key="downvote_chat"):
                                logging.info(f"Query: {query} | Route: CHAT | Answer: {answer}")
                                st.toast("Feedback logged for Self-Improving Agent.")
                except Exception as e:
                    st.error(f"Error communicating with LiteLLM proxy: {e}")
                    
            else:
                st.subheader("Retrieval")
                context_string = ""
                
                if not DEMO_MODE:
                    mongo_uri = os.getenv("MONGO_URI", "")
                    if not mongo_uri:
                        st.error("MONGO_URI not found.")
                        st.stop()
                        
                    client = MongoClient(mongo_uri)
                    collection = client.typestream.techforge_vectors
                    
                    import re
                    words = query.split()
                    regex_pattern = "|".join(words)
                    
                    cursor = collection.find({"text": {"$regex": regex_pattern, "$options": "i"}}).limit(3)
                    retrieved_docs = list(cursor)
                    
                    if not retrieved_docs:
                        retrieved_docs = list(collection.find().limit(3))
                    
                    chunks = []
                    for i, doc in enumerate(retrieved_docs):
                        chunk_text = doc.get("text", "")
                        chunks.append(chunk_text)
                        st.write(f"**Raw Chunk {i+1}:** {chunk_text[:150]}...")
                    context_string = "\n\n".join(chunks[:3])
                else:
                    st.write("**Demo Mode:** Bypassing live vector retrieval.")
                
                st.subheader("Generation")
                try:
                    answer = get_rag_response(query, context_string)
                    st.write("### AI Answer:")
                    st.success(answer)
                    st.caption("Answered by: **🧠 Deep Reasoner** (`qwen2.5-coder:32b`)")
                    
                    # Human in the loop feedback
                    if not DEMO_MODE:
                        col1, col2 = st.columns([1, 10])
                        with col1:
                            if st.button("👎", key="downvote_rag"):
                                logging.info(f"Query: {query} | Route: RAG | Context: {context_string} | Answer: {answer}")
                                st.toast("Feedback logged for Self-Improving Agent.")
                except Exception as e:
                    st.error(f"Error communicating with LiteLLM proxy: {e}")
