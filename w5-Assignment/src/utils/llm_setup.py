from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import config

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key=config.GEMINI_API_KEY
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-004",
    api_key=config.GEMINI_API_KEY
)