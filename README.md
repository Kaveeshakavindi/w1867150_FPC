## Getting started

Step 1 : Activate virtual environment

```bash
source .venv/bin/activate
```

Step 2 : Run backend

```bash
cd w1867150_IPD/Backend
python -m uvicorn api:app --reload
```

Step 3 : Run frontned

required npm version : 20

```bash
cd w1867150_IPD/Frontend/synapse-frontend
npm run dev
```
<<<<<<< HEAD
# System architecture

┌─────────────────────────────────────────────────────────┐
│           DATA PREPROCESSING PIPELINE                   │
│  1. ESG Topic Extraction (dataPreprocessing.py)         │
│  2. Topic Categorization (categorization/)              │
│  3. Vector Store Building (build_vectorstore.py)        │
└─────────────────────────────────────────────────────────┘

-----------------------------------------------------------


┌─────────────────────────────────────────────────────────┐
│              BACKEND (FastAPI + Python)                 │
│  ┌──────────────────────────────────────────────────┐   │
│  │  1. RETRIEVAL MODULE (retrieval.py)              │   │
│  │     • FAISS Vector Store                         │   │
│  │     • Semantic Search (HuggingFace Embeddings)   │   │
│  │     • 3 Document Types:                          │   │
│  │       - Company Reports                          │   │
│  │       - Counter-Evidence (lawsuits, violations)  │   │
│  │       - Supportive Evidence (awards, audits)     │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  2. ONTOLOGY REASONING (ontologyInfo.py)         │   │
│  │     • OWL Ontology (ontology.owl)                │   │
│  │     • Classes, Properties                        │   │
│  │     • Greenwashing Pattern Detection             │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │  3. LLM REASONING (pipeline.py + llm.py)         │   │
│  │     • Mistral 7B (via Ollama)                    │   │
│  │     • Evidence-based judgment                    │   │
│  │     • Structured JSON output                     │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼

┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js)                   │
│         User inputs company + ESG claim                 │
└────────────────────┬────────────────────────────────────┘
                     
=======

>>>>>>> c6f1b0fed3f17a5ced5ccef3c48defb6b72336ee
            
# w1867150_FPC
