import os
from openai import OpenAI

class LlamaProvider:
    def __init__(self, api_key=None, model=None, **kwargs):
        base = os.getenv("LLAMA_BASE_URL") or "https://ollama.com/v1"
        key = api_key or os.getenv("LLAMA_API_KEY")
        m = model or os.getenv("LLAMA_MODEL") or "gpt-oss:20b"
        if not m or not str(m).strip():
            m = "gpt-oss:20b"
        self.model = str(m).strip()
        print(f"[llama] using model: {self.model} @ {base}")
        self.client = OpenAI(base_url=base, api_key=key)

    def chat(self, messages, tools=None):
        kw = {"model": self.model, "messages": messages}
        if tools:
            kw["tools"] = tools
        r = self.client.chat.completions.create(**kw)
        msg = r.choices[0].message
        return {
            "content": msg.content or "",
            "tool_calls": [
                {"name": tc.function.name, "arguments": tc.function.arguments, "id": tc.id}
                for tc in (msg.tool_calls or [])
            ]
        }
