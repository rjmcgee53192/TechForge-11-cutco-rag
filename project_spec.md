# TechForge RAG System - Project Spec

**Project Code:** 11-techforge-rag
**Target Bundle:** 2026 Core Developer Foundation
**Primary Model:** qwen2.5-coder:32b / deepseek-v3

## 1. Project Overview
This project constitutes a local, highly-optimized Retrieval-Augmented Generation (RAG) pipeline designed to process and query pricing and care data from the TechForge PDF catalog. It utilizes a zero-cost local inference architecture running on an RTX A6000 node.

## 2. Current Progress & Integrations
*   **Data Ingestion:** `ingest.py` successfully reads `wellness_industrial equipments.pdf`, chunks it at 500 characters (preserving pricing table integrity), and pushes to MongoDB Atlas `techforge_vectors` collection.
*   **Vector Backend:** PyMongo bridging active. Trade-off applied: Utilizing regex-based text search as a lightweight substitute for complex vector embedding computations in the current prototype tier.
*   **Generation Tier:** `app_streamlit.py` built from scratch. Implements the full Retrieval and Generation sequence, forwarding top-3 context chunks to the local Ollama engine API.
*   **Resiliency:** `langgraph_self_healing.py` deployed to wrap python executions in a cyclic graph structure, granting autonomous patch-and-retry capabilities to execution failures.

## 3. Environment Hardening (Active Skills)
*   `firecrawl`, `tavily-search`: Active for advanced web supplementation if local data fails.
*   `github-mcp`: Version control synchronized.
*   `Self-Improving Agent`: Actively monitoring `/workspace/projects/11-techforge-rag/` and indexing terminal history for personalized workflow optimization.

## 4. Next Technical Milestones
1.  **Open WebUI Integration:** Connect the newly cloned `open-webui` interface directly to the RAG backend for a polished chat experience.
2.  **n8n Orchestration:** Utilize the `n8n` platform to trigger daily updates to the TechForge knowledge base autoindustrial equipmentically.
