import os
from langchain_google_genai import ChatGoogleGenerativeAI

# If using Option A, ensure load_dotenv() was called first
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    print("✅ API Key detected!")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    print(llm.invoke("Say hello!").content)
else:
    print("❌ API Key NOT found. Check your .env file or environment variables.")