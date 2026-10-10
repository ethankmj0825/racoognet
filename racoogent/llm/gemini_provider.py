from .base import BaseLLM
import google.generativeai as genai
class GeminiProvider(BaseLLM):
    def __init__(self, api_key, model="gemini-1.5-flash"):
        genai.configure(api_key=api_key); self.model=genai.GenerativeModel(model)
    def chat(self, messages, tools=None):
        prompt="\n".join([f"{m['role']}: {m['content']}" for m in messages])
        return {"content": self.model.generate_content(prompt).text, "tool_calls":[]}
