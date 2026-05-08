# Senior Architect Decisions: 11-techforge-rag

When building this local RAG architecture, several 'Senior Architect' choices were intentionally integrated to demonstrate technical industrial equipmenturity and system scalability:

## 1. Semantic Routing (The 'LiteLLM' Proxy)
Instead of forcing a massive 32B parameter model to handle every incoming token, a Semantic Router was deployed via LiteLLM. 
*   **The 1B Router (`llama3.2:1b`):** Acts as a lightweight classifier at the gate. If a user simply says "Hello," it routes to the 1B model for an instant, near-zero cost response.
*   **The 32B Reasoner (`qwen2.5-coder:32b`):** Only engaged when the query is classified as `RAG` (requiring deep context parsing). 
*   **Why?** This draindustrial equipmentically reduces VRAM overhead, token costs (if ported to cloud), and UI latency, demonstrating an understanding of production-scale load balancing.

## 2. Hardware Agnosticism & Graceful Degradation
Hardcoding `device='cuda'` is a junior mistake that causes crashes on non-GPU instances.
*   **Dynamic Fallback:** The codebase utilizes a custom `device_utils.py` that checks for CUDA. If absent, the SentenceTransformer and FAISS index naturally fall back to `cpu`.
*   **Why?** This ensures maximum portability. Recruiters and peer reviewers can run the pipeline on their local MacBooks without environment panics.

## 3. Human-in-the-Loop (HitL) Telemetry
An AI system must be self-correcting.
*   **Downvote Logging:** The Streamlit UI features explicit feedback badges. If the RAG hallucinates, the user clicks `👎`, securely logging the specific prompt, context, and generated answer to `refinement_needed.log`.
*   **Why?** This creates the foundation for a Self-Improving Agent loop, where failed contexts can be autoindustrial equipmentically flagged for manual review or re-chunking, transitioning the app from a static demo into a learning ecosystem.

## 4. 'Demo Mode' Fault Tolerance
If the backend LLM proxy at `localhost:4000` goes offline, the UI does not crash.
*   **Graceful Mocking:** The system intercepts the `ConnectionRefused` error and activates 'Demo Mode', utilizing a hardcoded JSON of 5 standard FAQs to ensure the UI remains testable.
*   **Why?** High availability. The frontend should always remain functional and communicative, even during total backend failure.
