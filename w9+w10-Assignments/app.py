import os
import requests
import streamlit as st
import html

st.set_page_config(page_title="MCP GitHub Repo Analyzer", layout="wide")

backend_from_secrets = None
try:
	backend_from_secrets = st.secrets.get("BACKEND_URL")
except Exception:
	backend_from_secrets = None

BACKEND_URL = backend_from_secrets or os.getenv("BACKEND_URL", "http://localhost:8000")

if "history" not in st.session_state:
	st.session_state.history = []


def call_backend(query: str):
	url = f"{BACKEND_URL.rstrip('/')}/analyze_repo"
	try:
		r = requests.get(url, params={"query": query}, timeout=60)
		r.raise_for_status()
		return r.json()
	except Exception as e:
		return {"error": str(e)}


def render_result(result: dict, container):
	container.markdown("### Analysis")
	if not result:
		container.info("No result returned from backend.")
		return
	if "error" in result:
		container.error(result["error"]) 
		return

	# show main summary
	summary = result.get("summary") or result.get("data") or result.get("result")
	if isinstance(summary, (dict, list)):
		container.json(summary)
	else:
		container.write(summary)

	# optional fields: traces, details
	traces = result.get("traces") or result.get("reasoning") or result.get("details")
	if traces:
		with container.expander("Reasoning / traces", expanded=False):
			if isinstance(traces, (dict, list)):
				st.json(traces)
			else:
				st.write(traces)


st.title("MCP GitHub Repository Analyzer")
st.subheader("MCP GitHub Repository Analyzer is a tool that can be used to retrieve recent commits, issues and pull requests and compose them in an easily readable form.")
st.markdown("---")

# Query input
st.write("Enter queries like `analyze openai/gpt-4`.")
with st.form(key="query_form"):
	query = st.text_input("Ask about a repo…", placeholder="analyze openai/gpt-4")
	submit = st.form_submit_button("Send")

# Output box
results_box = st.container()

def _render_boxed_result(result: dict, container):
	"""Render the main result inside a styled boxed HTML block."""
	if not result:
		container.markdown("<div style='padding:12px'>No result returned from backend.</div>", unsafe_allow_html=True)
		return

	# show error inside box
	if "error" in result:
		error_html = f"<div style='border:1px solid #6b7280; background:#2b2f33; padding:14px; border-radius:8px; color:#fff;'><strong>Error</strong><pre style='white-space:pre-wrap;color:#ffb4b4'>{html.escape(result['error'])}</pre></div>"
		container.markdown(error_html, unsafe_allow_html=True)
		return

	summary = result.get("summary") or result.get("data") or result.get("result") or "(no summary)"
	# prepare summary HTML
	if isinstance(summary, (dict, list)):
		import json
		body = f"<pre style='white-space:pre-wrap;color:#d1d5db'>{html.escape(json.dumps(summary, indent=2))}</pre>"
	else:
		body = f"<div style='color:#d1d5db'>{html.escape(str(summary))}</div>"

	# traces/details
	traces = result.get("traces") or result.get("reasoning") or result.get("details")
	traces_html = ""
	if traces:
		if isinstance(traces, (dict, list)):
			import json
			traces_html = f"<details style='margin-top:10px;color:#cbd5e1'><summary style='cursor:pointer'>Reasoning / traces</summary><pre style='white-space:pre-wrap;color:#cbd5e1'>{html.escape(json.dumps(traces, indent=2))}</pre></details>"
		else:
			traces_html = f"<details style='margin-top:10px;color:#cbd5e1'><summary style='cursor:pointer'>Reasoning / traces</summary><pre style='white-space:pre-wrap;color:#cbd5e1'>{html.escape(str(traces))}</pre></details>"

	# final boxed html
	boxed_html = (
		"<div style='border:1px solid #374151; background:#0b1220; padding:16px; border-radius:10px;'>"
		f"<div style='font-weight:600; color:#e6eef8; margin-bottom:8px'>Analysis</div>"
		f"{body}"
		f"{traces_html}"
		"</div>"
	)
	container.markdown(boxed_html, unsafe_allow_html=True)

# History
history_box = st.container()


if submit and query:
	# call backend and render into the boxed output
	with results_box:
		status = st.info("Fetching analysis from backend…")
		result = call_backend(query)
		status.empty()
		_render_boxed_result(result, results_box)
		# record history
		st.session_state.history.append((query, result))

elif st.session_state.history:
	# if no new submit, show last result in box
	last_q, last_res = st.session_state.history[-1]
	_render_boxed_result(last_res, results_box)
else:
	# initial empty state box
	results_box.markdown("<div style='border:1px dashed #334155; padding:16px; border-radius:10px; color:#94a3b8'>No results yet — enter a query above and press Send.</div>", unsafe_allow_html=True)


# Render history below the output
history_box.markdown("---")
history_box.markdown("### History")
if st.session_state.history:
	# Show recent queries in a dropdown (newest first)
	recent = list(reversed(st.session_state.history[-20:]))
	# include a visible placeholder option at the top so nothing is selected by default
	placeholder_label = "-- select a previous query --"
	options = [placeholder_label] + [q for q, _ in recent]
	selected = history_box.selectbox("Select a previous query", options, index=0, key="history_select")
	# find selected result
	if selected == placeholder_label:
		history_box.write("No query selected — choose one from the dropdown to view its result.")
	else:
		idx = options.index(selected) - 1  # adjust for blank option at head
		qsel, rsel = recent[idx]
		history_box.markdown(f"**{html.escape(qsel)}**")
		if isinstance(rsel, dict) and rsel.get("summary"):
			s = rsel.get("summary")
			if isinstance(s, (dict, list)):
				import json
				history_box.text(json.dumps(s, indent=2))
			else:
				history_box.write(s)
		elif isinstance(rsel, dict) and rsel.get("error"):
			history_box.write(f"Error: {rsel.get('error')}")
		else:
			history_box.write(rsel)
else:
	history_box.write("No history yet — run a query.")


st.caption(f"Backend: {BACKEND_URL} — override with BACKEND_URL env var")

