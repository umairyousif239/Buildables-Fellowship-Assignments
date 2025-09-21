# LLM Agents & Retrieval Solutions - AI Journal & Reflection Companion

## Problem Statement
The problem that I intended to solve was how most personalized journals are kind of like a document file but managed. What I aimed to do was create an AI-assisted personal journal that keeps track of all your entries, provides feedback on what you say and graphs how your mood has been for the past few days. This would allow the journaling to feel a lot more personal and let you believe that someone is there to hear your thoughts and keep them to themselves.

## Solution Architecture
### Frontend / Interface

- Simple web app (Streamlit / Flask) or CLI where users input daily entries.
- Could also allow voice → text.

### Document Ingestion & Storage

- Store each journal entry in a vector database (FAISS).
- Use embeddings (HuggingFace) for semantic retrieval.
- LangChain Agent Core

### Conversational Memory: Keeps short-term dialogue context.

- Long-Term Memory (Vector DB): Retrieves old entries when relevant.

### Tools Integration:

- Sentiment analyzer (VADER).

### Analysis Layer

- Run daily entry through sentiment analysis → store score (+ tag like happy, neutral, stressed).
- Track frequency of emotions over time.

### Agent Responses

- Answer reflective questions: “How has my mood changed in the last 2 weeks?”
- Proactive insights: “You’ve been writing about burnout a lot recently, maybe schedule a break.”

## Setup Instructions
[Step-by-step setup guide]
All you need to do to get this to run is run `pip install -r requirements.txt` first to install all the necessary libraries. After that, just run the `streamlit run app.py` in the terminal to get the app running. The UI is super user-friendly as all the features are divided in to proper tabs.

## Demo Video
[Link to your video demonstration]

## Usage Examples
This project can be used in many ways. You can:
- Log entries for each day about how your day went.
- Chart how your mood has been over the past few days.
- See the mood charted as a graph.
- Ask about your mood in the insight tab.
- Get a reflection on your entry.

## Technical Challenges
The main challenge that I came across was implementing embedding. I was having issue with the Gemini API for some reason so I ended up changing it to the HuggingFace's all-MiniLM-L6-v2 model. That solved the issue for me.

## Impact & Results
As this idea was for a personal journal, I think I will start using it on my own. I will however post about it on my social media account to see if anyone is interested in this project and if so, they can use it on their own.

## Future Improvements
I think in the future, I could work more on it's Frontend and make it a bit better as the current one, however friendly, seems to fall flat. 