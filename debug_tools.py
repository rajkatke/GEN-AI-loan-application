import os
from langchain_google_genai import ChatGoogleGenerativeAI
from loan_mcp import validate_pan
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=os.getenv("GEMINI_API_KEY"))

print(f"Tool type: {type(validate_pan)}")
print(f"Tool attributes: {dir(validate_pan)}")

from langchain_core.tools import StructuredTool

print(f"Has fn attribute: {hasattr(validate_pan, 'fn')}")

try:
    # Try binding the underlying function
    print("Attempting to bind validate_pan.fn...")
    llm_with_tools = llm.bind_tools([validate_pan.fn])
    print("Binding .fn successful")
except Exception as e:
    print(f"Binding .fn failed: {e}")

try:
    # Try wrapping in StructuredTool
    print("Attempting to wrap in StructuredTool...")
    tool = StructuredTool.from_function(validate_pan.fn)
    llm_with_tools = llm.bind_tools([tool])
    print("Binding StructuredTool successful")
except Exception as e:
    print(f"Binding StructuredTool failed: {e}")
