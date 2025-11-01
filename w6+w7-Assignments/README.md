# DocWeave AI — “Weaving extraction, RAG, vision, and long-context into answers”

A modular, Streamlit-based RAG pipeline for document Q&A with:
- Reliable PDF extraction (Docling) plus extractor comparison (PyPDF2, pdfplumber, Docling)
- Embedding + FAISS retrieval
- Side-by-side RAG vs Non‑RAG answers
- Chunking experiments
- Vision analysis (photo, document/screenshot, chart)
- Long-context hierarchical summarization + Q&A
- One-click exports of required deliverables

This app centralizes all scripts behind an easy UI; advanced settings are hidden by default.

## Quick Start (Windows)

- Python 3.10+
- Install dependencies:
  ```
  pip install -r requirements.txt
  ```
  If you don’t have a requirements.txt, install:
  ```
  pip install streamlit pillow sentence-transformers faiss-cpu google-generativeai PyPDF2 pdfplumber docling
  ```
- Set your API key:
  ```
  setx GEMINI_API_KEY "YOUR_API_KEY"
  ```
  Or put GEMINI_API_KEY in configurations.py.

- Run the app:
  ```
  python -m streamlit run app.py
  ```

## Project Structure (key paths)

- app.py — Streamlit UI (orchestrator)
- rag_pipeline/config.json — RAG settings (loaded as defaults)
- resources/pdfs/ — Put PDFs here (or upload in the UI)
- extracted_output/<doc>.json — Docling extraction outputs (JSON source of truth)
- vector_store/<doc>/ — Cached FAISS index, embeddings, chunks
- resources/readings/extraction_comparison_<doc>.(md|json) — Extractor comparison
- results/chunking_notes.md — Chunking experiment report
- results/comparison_results.json — Logged RAG vs Non‑RAG answers
- results/comparison_table.md — Markdown table exported from comparison_results.json
- results/images/ — Vision analyses (.md) and uploaded images
- results/long_context_<doc>.(md|json) — Long-context summary + Q&A

## Features

- Docling extraction (best-effort structure and tables) saved to JSON.
- Extractor comparison: PyPDF2, pdfplumber, Docling
  - Summary stats, Jaccard overlap, samples
  - One-click save to Markdown + JSON
- Indexing and retrieval with FAISS + sentence-transformers
- RAG Q&A with:
  - RAG answer shown prominently
  - Dropdown expander with RAG vs Non‑RAG answers and retrieved context
  - Log Q&A pairs and export a Markdown comparison table
- Chunking experiments:
  - Evaluate multiple chunk size/overlap settings
  - Log top‑k retrieved snippets with distances
- Vision analysis (Gemini):
  - Photograph description
  - Document OCR/structuring
  - Chart explanation
  - Saves analysis and image under results/images/
- Long-context:
  - Hierarchical summarization over large documents via chunked passes
  - Retrieval-backed Q&A for multi-part questions
  - Exports JSON + Markdown

## How to Use (Tabs)

1) Docling Extraction
- Upload/select a PDF (moved here for clarity).
- Click “Run Docling extraction” to create extracted_output/<doc>.json.
- Click “Build/Load Index” to create/load FAISS index (auto-switches to RAG tab).
- Preview shows the first extracted text snippets.

2) Indexing + RAG Q&A
- Ask a question.
- See the main RAG answer.
- Expand “Compare: RAG vs Non‑RAG (and retrieved context)” to:
  - View both answers side-by-side
  - Inspect retrieved chunks and distances
  - Log the pair to results/comparison_results.json
  - Export results/comparison_table.md

3) Extraction Comparison
- Run a head-to-head extraction on the selected PDF using PyPDF2, pdfplumber, and Docling.
- View stats and overlap in-app.
- Save Markdown + JSON reports to resources/readings/.

4) Chunking Experiments
- Runs a couple of pre-defined chunk size/overlap configs.
- For each config, shows top‑k retrieved snippets per question with distances.
- Saves results/chunking_notes.md.

5) Vision
- Upload an image; choose “photograph”, “document”, or “chart”.
- Runs Gemini Vision analysis; saves .md under results/images/ and persists the image file.

6) Long-Context
- Uses extracted text to build hierarchical summaries over chunked content (handles ~50k+ tokens via multiple passes, not a single call).
- Runs retrieval-backed Q&A for three configurable questions.
- Saves results to results/long_context_<doc>.md and .json.

## Settings

- Presets in the sidebar:
  - Balanced (default), Fast, Accurate (tunes chunk size/overlap/top_k)
- Advanced RAG settings (hidden inside an expander):
  - Embedding model (default: sentence-transformers/all-MiniLM-L6-v2)
  - Chunk size, overlap, Top‑K
  - LLM model (default: gemini-1.5-flash)
  - Prompt template
  - Optional: persist to rag_pipeline/config.json

Notes:
- JSON is the source of truth; Markdown is auto-generated for submission.
- Long-context chunk size/overlap control how the source is split; not the answer length.
- To cap/extend answer length, set generation_config.max_output_tokens in the LLM calls.

## Requirements

- Python 3.10+
- Packages:
  - streamlit, pillow, sentence-transformers, faiss-cpu, google-generativeai, PyPDF2, pdfplumber, docling
- API Key:
  - GEMINI_API_KEY in environment or configurations.py

## Troubleshooting

- NameError/path issues: Ensure app.py imports helper modules from utils/, rag_pipeline/, tests/ correctly and that ROOT is set to this repo directory.
- Missing FAISS: Install CPU build on Windows: `pip install faiss-cpu`.
- Docling errors: Make sure `docling` is installed; some PDFs may still have layout quirks.
- API errors: Verify GEMINI_API_KEY and internet connectivity.
- No text extracted: Check if PDF is image-only; try the Vision “document” OCR and/or different extractor for comparison report.

## Development Notes

- Modular architecture:
  - utils/: comparison, vision helpers
  - modules/rag_core.py, modules/extraction_compare.py, modules/chunking_experiment.py, modules/long_context.py (if present)
  - The Streamlit app calls these modules; it isn’t a monolith.
- Cached indexing:
  - Caches FAISS index/embeddings per document and chunk settings in vector_store/<doc>/.

## License

Educational use for Buildables Fellowship Week 6–7 assignments. Replace or extend with your license as needed.