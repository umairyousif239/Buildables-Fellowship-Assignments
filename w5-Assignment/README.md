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
All you need to do to get this to run is run ```pip install -r requirements.txt``` first to install all the necessary libraries. After that, just run the `streamlit run app.py` in the terminal to get the app running. The UI is super user-friendly as all the features are divided in to proper tabs.

## Demo Video
[Link to your video demonstration]

## Usage Examples
[How to use your solution]

## Technical Challenges
[Key problems solved during development]

## Impact & Results
[Measured or projected impact]

## Future Improvements
[Planned enhancements]