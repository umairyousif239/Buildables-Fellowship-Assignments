import streamlit as st
from datetime import date

from src.utils.llm_setup import embeddings
from src.utils.db import create_db, add_entry
from src.utils.journal_store import init_db, upsert_entry, get_entry_by_date, list_entries, sentiment_trend
from src.agent import reflect

# Initialize vector DB and SQLite
if "db" not in st.session_state:
    if embeddings is None:
        st.error("Embeddings not initialized. Please check your Hugging Face API key and configuration.")
    else:
        st.session_state.db = create_db(embeddings)
        init_db()

st.title("📝 AI Journal & Reflection Companion")

tab1, tab2, tab3 = st.tabs(["Write", "History", "Insights"])

with tab1:
    st.subheader("Write today's entry")
    with st.form(key="write_form"):
        col1, col2 = st.columns([2, 1])
        with col1:
            selected_date = st.date_input("Date", value=date.today(), key="write_date")
        with col2:
            st.markdown("<div style='visibility:hidden'>Date</div>", unsafe_allow_html=True)
            load_clicked = st.form_submit_button("Load Saved", use_container_width=True)

        if load_clicked:
            existing = get_entry_by_date(selected_date.isoformat())
            if existing:
                st.session_state["entry_text"] = existing["content"]
                st.success("Loaded saved entry for this date.")
            else:
                st.session_state["entry_text"] = ""
                st.info("No saved entry for this date.")

        entry = st.text_area(
            "Your thoughts...",
            value=st.session_state.get("entry_text", ""),
            height=200,
            placeholder="Write freely about your day, feelings, or anything on your mind...",
        )

        c1, c2 = st.columns([1, 1])
        with c1:
            save_only = st.form_submit_button("Save only", type="secondary", use_container_width=True)
        with c2:
            save_reflect = st.form_submit_button("Save & Reflect", type="primary", use_container_width=True)

        submitted = save_only or save_reflect or load_clicked

    # Handle form submission outside the form block
    if submitted and not load_clicked:
        if not entry.strip():
            st.warning("Please write something before saving.")
        else:
            from src.tools.sentiment import analyze_sentiment_with_scores
            sent, sent_score = analyze_sentiment_with_scores(entry)
            reflection_text = None
            if save_reflect:
                reflection_text = reflect(st.session_state.db, entry)
            upsert_entry(
                selected_date.isoformat(),
                entry,
                sentiment=sent,
                reflection=reflection_text,
                sentiment_score=sent_score,
            )
            add_entry(st.session_state.db, f"[{selected_date.isoformat()}] {entry}")
            st.success("Saved successfully.")
            if reflection_text:
                st.write("### Reflection")
                st.write(reflection_text)

with tab2:
    st.subheader("Recent entries")
    recent = list_entries(limit=14)
    if recent:
        for r in recent:
            with st.expander(f"{r['date']} — {r.get('sentiment', 'unknown')}"):
                st.markdown("**Entry**")
                st.write(r.get("content") or "")
                if r.get("reflection"):
                    st.markdown("**Reflection**")
                    st.write(r["reflection"])
                # Re-generate reflection button
                regen_key = f"regen_{r['date']}"
                if st.button("Re-generate reflection", key=regen_key):
                    new_reflection = reflect(st.session_state.db, r.get("content") or "")
                    # Persist updated reflection
                    upsert_entry(
                        r["date"],
                        r.get("content") or "",
                        sentiment=r.get("sentiment"),
                        reflection=new_reflection,
                        sentiment_score=r.get("sentiment_score"),
                    )
                    st.success("Updated reflection saved.")
                    st.write("**New Reflection**")
                    st.write(new_reflection)
    else:
        st.caption("No entries yet. Your recent entries will appear here.")

with tab3:
    # Compute once for both Q&A and chart
    trend = sentiment_trend(days=14)

    # 1) Analytics Q&A first
    st.subheader("Ask about your mood (no AI)")
    q_col1, q_col2 = st.columns([3, 1])
    with q_col1:
        q = st.text_input("Question", placeholder="e.g., How has my mood changed in the last 2 weeks?")
    with q_col2:
        st.markdown("<div style='visibility:hidden'>Question</div>", unsafe_allow_html=True)
        ask = st.button("Analyze", use_container_width=True)
    if ask:
        if not trend:
            st.info("Not enough data yet. Add a few entries first.")
        else:
            # Compare earlier vs recent half of available scores
            last14 = [t for t in trend if t.get("sentiment_score") is not None]
            if len(last14) < 4:
                st.info("Need at least a few days with entries to analyze.")
            else:
                import statistics
                half = max(1, len(last14) // 2)
                prev = [t["sentiment_score"] for t in last14[:half]]
                recent = [t["sentiment_score"] for t in last14[half:]]
                prev_avg = statistics.fmean(prev) if prev else 0.0
                recent_avg = statistics.fmean(recent) if recent else 0.0
                delta = recent_avg - prev_avg
                if delta > 0.05:
                    direction = "improved"
                elif delta < -0.05:
                    direction = "declined"
                else:
                    direction = "held steady"
                st.write(
                    f"In the last two weeks, your average sentiment {direction}. "
                    f"Previous avg: {prev_avg:+.2f}, Recent avg: {recent_avg:+.2f}."
                )

    st.divider()
    # 2) Mood over time chart and list
    st.subheader("Mood over time (last 14 days)")
    if trend:
        import pandas as pd
        scores = [t["sentiment_score"] for t in trend if t.get("sentiment_score") is not None]
        if scores:
            avg = sum(scores) / len(scores)
            st.metric("Avg sentiment (14d)", f"{avg:+.2f}")
        # Line chart for daily scores
        df = pd.DataFrame(trend)
        if not df.empty and "sentiment_score" in df.columns:
            df = df.sort_values("date")
            df_chart = df[["date", "sentiment_score"]].set_index("date")
            st.line_chart(df_chart)
        st.write("Daily sentiment (higher is more positive):")
        for t in trend:
            day = t["date"]
            label = t.get("sentiment", "?")
            score = t.get("sentiment_score")
            st.caption(f"{day}: {label} ({score:+.2f})" if score is not None else f"{day}: {label}")
    else:
        st.caption("Sentiment trend will appear once you have entries with scores.")