import os, sys, json
import streamlit as st

# Use repo root (this file's directory), not parent
ROOT = os.path.dirname(__file__)
if ROOT not in sys.path: sys.path.insert(0, ROOT)

from utils.pdf_extraction import save_extraction
from tests.extraction_compare import run_compare, save_reports
from rag_pipeline.rag_core import load_config, build_or_load_index, retrieve_with_scores, answer_question
from tests.chunking_experiment import run_chunking_experiments
from utils.vision_analysis import analyze_image
from utils.long_context import hierarchical_summarize, qa_over_corpus
from utils.comparison_utils import append_comparison_result, export_comparison_table

try:
    from configurations import GEMINI_API_KEY
except Exception:
    import os as _os
    GEMINI_API_KEY = _os.getenv("GEMINI_API_KEY")

PDF_DIR = os.path.join(ROOT, "resources", "pdfs")
EXTRACT_DIR = os.path.join(ROOT, "extracted_output")
READINGS_DIR = os.path.join(ROOT, "resources", "readings")
RESULTS_DIR = os.path.join(ROOT, "results")
VSTORE_DIR = os.path.join(ROOT, "vector_store")
CONFIG_PATH = os.path.join(ROOT, "rag_pipeline", "config.json")

# Common UI messages
EXTRACTION_WARNING = "Please run extraction first."
UPLOAD_SELECT_MESSAGE = "Upload/select a PDF."

for d in [PDF_DIR, EXTRACT_DIR, READINGS_DIR, RESULTS_DIR, VSTORE_DIR]: os.makedirs(d, exist_ok=True)

def per_doc_paths(pdf_path):
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    cache_dir = os.path.join(VSTORE_DIR, base); os.makedirs(cache_dir, exist_ok=True)
    return {
        "extracted_json": os.path.join(EXTRACT_DIR, f"{base}.json"),
        "cache_dir": cache_dir,
        "compare_md": os.path.join(READINGS_DIR, f"extraction_comparison_{base}.md"),
        "compare_json": os.path.join(READINGS_DIR, f"extraction_comparison_{base}.json"),
        "long_json": os.path.join(RESULTS_DIR, f"long_context_{base}.json"),
        "long_md": os.path.join(RESULTS_DIR, f"long_context_{base}.md"),
    }

st.set_page_config(page_title="IntelliDoc AI — Modular", layout="wide")
st.title("IntelliDoc AI — Modular Streamlit App")

with st.sidebar:
    # Load defaults from config.json
    cfg = load_config(CONFIG_PATH)
    st.subheader("Settings")
    preset = st.selectbox("Preset", ["Balanced (default)", "Fast", "Accurate"], index=0)

    # Build a runtime config (hidden by default, overridable below)
    runtime_cfg = dict(cfg)
    if preset == "Fast":
        runtime_cfg["chunk_size"] = 300
        runtime_cfg["overlap"] = 30
        runtime_cfg["retrieval_top_k"] = 3
    elif preset == "Accurate":
        runtime_cfg["chunk_size"] = 800
        runtime_cfg["overlap"] = 150
        runtime_cfg["retrieval_top_k"] = 7
        # Optionally pick a stronger model if you have access:
        # runtime_cfg["llm_model"] = "gemini-1.5-pro"

    # Advanced settings (hidden for normal users)
    with st.expander("Advanced RAG settings (optional)", expanded=False):
        runtime_cfg["embedding_model"] = st.text_input("Embedding model", value=runtime_cfg["embedding_model"])
        runtime_cfg["chunk_size"] = st.number_input("Chunk size", 100, 4000, int(runtime_cfg["chunk_size"]), step=50)
        runtime_cfg["overlap"] = st.number_input("Overlap", 0, 1000, int(runtime_cfg["overlap"]), step=10)
        runtime_cfg["retrieval_top_k"] = st.slider("Top K", 1, 10, int(runtime_cfg["retrieval_top_k"]))
        runtime_cfg["llm_model"] = st.text_input("LLM model", value=runtime_cfg["llm_model"])
        prompt_template = st.text_area("Prompt template", value=cfg["prompt_template"], height=120)

        persist = st.checkbox("Persist these settings to rag_pipeline/config.json", value=False)
        if persist and st.button("Save settings"):
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            base = {}
            if os.path.exists(CONFIG_PATH):
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    try:
                        base = json.load(f) or {}
                    except Exception:
                        base = {}
            base.setdefault("embedding", {})
            base.setdefault("rag", {})
            base["embedding"]["model"] = runtime_cfg["embedding_model"]
            base["embedding"]["chunk_size"] = int(runtime_cfg["chunk_size"])
            base["embedding"]["overlap"] = int(runtime_cfg["overlap"])
            base["rag"]["retrieval_top_k"] = int(runtime_cfg["retrieval_top_k"])
            base["rag"]["llm"] = runtime_cfg["llm_model"]
            base["rag"]["prompt_template"] = prompt_template
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(base, f, ensure_ascii=False, indent=2)
            st.success("Saved to config.json")

    # Share runtime settings with tabs
    st.session_state.runtime_cfg = runtime_cfg
    st.session_state.prompt_template = locals().get("prompt_template", cfg["prompt_template"])

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("Developed by [Umair Yousif](https://www.linkedin.com/in/umairyousif) | [GitHub](https://github.com/umairyousif239)")
    st.sidebar.markdown("Powered by [Google Gemini-1.5-flash](https://developers.generativeai.google/products/gemini) | [Buildables Fellowship](https://buildables.dev/#/fellowship)")


tabs = st.tabs([
    "1) Docling Extraction",
    "2) Indexing + RAG Q&A",
    "3) Extraction Comparison",
    "4) Chunking Experiments",
    "5) Vision",
    "6) Long-Context",
])

# 1) Docling Extraction
with tabs[0]:
    uploaded = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded:
        save_path = os.path.join(PDF_DIR, uploaded.name)
        with open(save_path, "wb") as f:
            f.write(uploaded.read())
        st.success(f"Saved: {save_path}")
    pdfs = [os.path.join(PDF_DIR, f) for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
    selected_pdf = st.selectbox("Select PDF", options=pdfs, format_func=os.path.basename) if pdfs else None
    if not selected_pdf:
        st.info("Upload/select a PDF above to continue.")
    else:
        paths = per_doc_paths(selected_pdf)
        if st.button("Run Docling extraction"):
            out = save_extraction(selected_pdf, paths["extracted_json"])
            st.success(f"Saved: {out}")
        if os.path.exists(paths["extracted_json"]):
            data = json.load(open(paths["extracted_json"], "r", encoding="utf-8"))
            st.caption(f"Source: {data.get('source_pdf')}")
            st.code("\n".join((data.get("texts") or [])[:10]))

with tabs[1]:
    if not selected_pdf:
        st.info(UPLOAD_SELECT_MESSAGE)
    else:
        paths = per_doc_paths(selected_pdf)
        paths = per_doc_paths(selected_pdf)
        if not os.path.exists(paths["extracted_json"]):
            st.warning(EXTRACTION_WARNING)
        else:
            if st.button("Build/Load Index"):
                rcfg = st.session_state.get("runtime_cfg", load_config(CONFIG_PATH))
                embedder, index, chunks = build_or_load_index(
                    paths["extracted_json"], paths["cache_dir"],
                    rcfg["embedding_model"], int(rcfg["chunk_size"]), int(rcfg["overlap"])
                )
                st.session_state.embedder = embedder
                st.session_state.index = index
                st.session_state.chunks = chunks
                st.success("Index ready.")

            if "index" in st.session_state and "chunks" in st.session_state and "embedder" in st.session_state:
                rcfg = st.session_state.get("runtime_cfg", load_config(CONFIG_PATH))
                prompt_template = st.session_state.get("prompt_template", rcfg["prompt_template"])
                q = st.text_input("Question")
                if st.button("Answer", key="ask_rag"):
                    rag_ans = answer_question(
                        q, True,
                        st.session_state.index, st.session_state.chunks, st.session_state.embedder,
                        rcfg["llm_model"], prompt_template, k=int(rcfg["retrieval_top_k"])
                    )
                    non_rag_ans = answer_question(
                        q, False,
                        st.session_state.index, st.session_state.chunks, st.session_state.embedder,
                        rcfg["llm_model"], prompt_template, k=int(rcfg["retrieval_top_k"])
                    )
                    st.subheader("RAG Answer")
                    st.write(rag_ans)
                    with st.expander("Compare: RAG vs Non‑RAG (and retrieved context)"):
                        st.markdown("#### RAG")
                        st.write(rag_ans)
                        st.markdown("#### Non‑RAG")
                        st.write(non_rag_ans)
                        st.markdown("#### Retrieved context")
                        top = retrieve_with_scores(q, st.session_state.index, st.session_state.chunks, st.session_state.embedder, k=int(rcfg["retrieval_top_k"]))
                        for i, (c, d) in enumerate(top, 1):
                            st.markdown(f"- {i}) dist={d:.2f}")
                            st.code(c)

                    # New: logging and export controls
                    colA, colB = st.columns(2)
                    if colA.button("Add to comparison log"):
                        p = append_comparison_result(RESULTS_DIR, q, rag_ans, non_rag_ans)
                        colA.success(f"Logged to {p}")
                    if colB.button("Export comparison table (Markdown)"):
                        out, err = export_comparison_table(RESULTS_DIR)
                        if out: colB.success(f"Saved {out}")
                        else: colB.error(err)

with tabs[2]:
    if not selected_pdf:
        st.info(UPLOAD_SELECT_MESSAGE)
    else:
        paths = per_doc_paths(selected_pdf)
        if st.button("Run comparison"):
            data = run_compare(selected_pdf)
            st.write(data["engines"]); st.write(data["overlaps"])
            if st.button("Save report"):
                save_reports(data, paths["compare_md"], paths["compare_json"])
                st.success(f"Saved: {paths['compare_md']} and {paths['compare_json']}")

with tabs[3]:
    if not selected_pdf:
        st.info(UPLOAD_SELECT_MESSAGE)
    else:
        paths = per_doc_paths(selected_pdf)
        if not os.path.exists(paths["extracted_json"]):
            st.warning(EXTRACTION_WARNING)
        else:
            cfgs = [{"size": 300, "overlap": 50}, {"size": 800, "overlap": 150}]
            questions = [
                "What is the main goal of the AI Surveillance System?",
                "Which technologies are mentioned in the proposal?",
                "What are the limitations discussed?",
                "What datasets or data sources does it use?",
                "What conclusions are drawn?"
            ]
            if st.button("Run experiments"):
                md = run_chunking_experiments(paths["extracted_json"], cfgs, questions, embedding_model=cfg["embedding_model"])
                out_md = os.path.join(RESULTS_DIR, "chunking_notes.md")
                with open(out_md, "w", encoding="utf-8") as f: f.write(md)
                st.success(f"Saved: {out_md}")
                st.code(md[:2000] + ("..." if len(md) > 2000 else ""))

# 5) Vision
with tabs[4]:
    img = st.file_uploader("Upload image", type=["png","jpg","jpeg"])
    task = st.selectbox("Task", ["photograph","document","chart"])
    if img and st.button("Analyze image"):
        text = analyze_image(img, task=task, model_id=cfg["llm_model"], api_key=GEMINI_API_KEY)
        st.write(text)
        # Save outputs
        import time
        out_dir = os.path.join(RESULTS_DIR, "images")
        os.makedirs(out_dir, exist_ok=True)
        stem, ext = os.path.splitext(getattr(img, "name", f"uploaded_{int(time.time())}.png"))
        md_path = os.path.join(out_dir, f"{stem}_{task}.md")
        img_path = os.path.join(out_dir, f"{stem}_{task}{ext or '.png'}")
        # Write analysis
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Vision Analysis: {stem}{ext} ({task})\n\n")
            f.write(text + "\n")
        # Persist uploaded image
        with open(img_path, "wb") as f:
            f.write(img.getbuffer())
        st.success(f"Saved: {md_path} and {img_path}")

with tabs[5]:
    if not selected_pdf:
        st.info(UPLOAD_SELECT_MESSAGE)
    else:
        paths = per_doc_paths(selected_pdf)
        if not os.path.exists(paths["extracted_json"]):
            st.warning(EXTRACTION_WARNING)
        else:
            jd = json.load(open(paths["extracted_json"], "r", encoding="utf-8"))
            jd = json.load(open(paths["extracted_json"], "r", encoding="utf-8"))
            corpus = jd.get("texts", [])
            size = st.number_input("Summary chunk size", 1000, 8000, 2000, 200)
            overlap = st.number_input("Summary overlap", 0, 1000, 300, 50)
            q1 = st.text_input("Q1", "Summarize the project goals and list the main components.")
            q2 = st.text_input("Q2", "What methods or technologies are proposed? Mention hardware and software.")
            q3 = st.text_input("Q3", "What are potential limitations or risks, and how might they be mitigated?")
            if st.button("Run long-context"):
                lvl1, lvl2 = hierarchical_summarize(corpus, model_id=cfg["llm_model"], api_key=GEMINI_API_KEY, size=int(size), overlap=int(overlap))
                qa = qa_over_corpus(corpus, [q1,q2,q3], embedding_model=cfg["embedding_model"], model_id=cfg["llm_model"], api_key=GEMINI_API_KEY)
                st.subheader("Level-2 Summary"); st.write(lvl2)
                out_json = paths["long_json"]; out_md = paths["long_md"]
                with open(out_json, "w", encoding="utf-8") as f:
                    json.dump({"level1_count": len(lvl1), "level2_summary": lvl2, "qa": qa}, f, ensure_ascii=False, indent=2)
                with open(out_md, "w", encoding="utf-8") as f:
                    f.write("# Long-context Demo\n\n## Level-2 Summary\n\n"+lvl2+"\n\n## Q&A\n\n")
                    for item in qa: f.write(f"### Q: {item['question']}\n\n{item['answer']}\n\n")
                st.success(f"Saved: {out_json} and {out_md}")