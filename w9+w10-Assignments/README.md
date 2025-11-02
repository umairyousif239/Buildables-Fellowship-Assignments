# 🤖 MCP GitHub Agent — *Gemini Enhanced*

## 🚀 Overview
**MCP GitHub Agent** is an intelligent repository analysis tool powered by **Google’s Gemini 2.5 Flash** model.  
It allows users to analyze any public GitHub repository and receive structured insights — including reasoning, detailed analysis, and an overall summary — through an elegant **Streamlit web interface**.

This project demonstrates practical integration of AI models with REST APIs, real-time data processing, and local data persistence — all key aspects of modern software engineering and AI-driven applications.

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | Streamlit |
| **Backend API** | FastAPI *(or Flask alternative)* |
| **AI Model** | Google Gemini 2.5 Flash |
| **Language** | Python 3.x |
| **Data Storage** | Local JSON file (auto-generated) |
| **HTTP Client** | Requests |

---

## 🧠 Core Features

### 1. AI-Powered Repository Analysis
- Fetches and processes GitHub repository data (commits, issues, pull requests, etc.).
- Sends repository summary to **Gemini 2.5 Flash**, which generates:
  - **Reasoning** — step-by-step logical breakdown of repo activity.
  - **Analysis** — detailed interpretation of trends, progress, and code health.
  - **Summary** — concise high-level overview.

### 2. Local History Storage
- Automatically stores previous analysis results in a **local JSON file**.
- Users can revisit or view previous insights anytime without reanalyzing.

### 3. Interactive Streamlit Interface
- Clean, centered UI with:
  - Text input for repository name (e.g., `openai/gpt-4`)
  - Loading spinners during API and AI processing
  - Tabbed view for **Reasoning**, **Analysis**, and **Summary**
- Fully responsive and easy to navigate.

### 4. Gemini 2.5 Integration
- Uses Google’s latest multimodal generative AI model for reasoning and summarization.
- Ensures consistent structured JSON responses with auto-parsing.

---

## 🧩 Architecture

    User → Streamlit UI → FastAPI Endpoint (/analyze_repo)

                        ↓ ↓

    Gemini 2.5 Flash ←→ Local JSON Storage

---

## 💾 Data Flow Summary
1. User enters a GitHub repo name.  
2. The backend API retrieves basic data about that repo.  
3. The frontend sends this data to **Gemini 2.5 Flash**.  
4. Gemini returns structured reasoning, analysis, and summary.  
5. The results are displayed in tabs and saved locally.

---

## 🧠 Reflection — How MCP Improved Context Awareness

The integration of the Model Context Protocol (MCP) significantly enhanced this project’s ability to reason with real, dynamic information instead of relying solely on static prompts. By connecting the LangGraph reasoning flow to the MCP layer (mcp_github.py), the agent gained the ability to fetch live repository data — including commits, issues, and pull requests — directly from GitHub’s API.

This made the AI agent context-aware in a meaningful way:

It reasons using up-to-date information about a repository’s activity and structure.

The LangGraph pipeline can process this data step-by-step, ensuring logical flow and explainable reasoning.

MCP provides a clean separation between reasoning (LangGraph) and retrieval (external APIs), resulting in a modular, maintainable, and scalable system.

Overall, MCP transformed the agent from a simple LLM prompt wrapper into a context-driven reasoning system capable of making informed analyses of real-world data sources. This separation of concerns mirrors how production-grade AI agents are built — ensuring reliability, adaptability, and clear interpretability.

---

## 🧰 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/umairyousif239/Buildables-Fellowship-Assignments/tree/main/w9%2Bw10-Assignments
cd mcp-github-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Gemini API key
mkdir .streamlit
echo "[secrets]\nGEMINI_API_KEY = 'your_api_key_here'" > .streamlit/secrets.toml

# 4. Run the app
streamlit run app.py