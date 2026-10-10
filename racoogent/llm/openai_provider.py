from .base import BaseLLM
from openai import OpenAI
class OpenAIProvider(BaseLLM):
    def __init__(self, api_key, model="gpt-4o-mini"):
        self.client=OpenAI(api_key=api_key); self.model=model
    def chat(self, messages, tools=None):
        kw={"model":self.model,"messages":messages}
        if tools: kw["tools"]=tools
        r=self.client.chat.completions.create(**kw)
        m=r.choices[0].message
        return {"content":m.content or "","tool_calls":[{"name":tc.function.name,"arguments":tc.function.arguments,"id":tc.id} for tc in (m.tool_calls or [])]}
