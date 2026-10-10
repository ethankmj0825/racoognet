import os
from .openai_provider import OpenAIProvider
from .gemini_provider import GeminiProvider
from .deepseek_provider import DeepSeekProvider
from .llama_provider import LlamaProvider
from .alibaba_provider import AlibabaProvider
PROVIDERS={"openai":OpenAIProvider,"gemini":GeminiProvider,"deepseek":DeepSeekProvider,"llama":LlamaProvider,"alibaba":AlibabaProvider}
def get_llm(provider_name, model=None):
    api_map={"openai":"OPENAI_API_KEY","gemini":"GEMINI_API_KEY","deepseek":"DEEPSEEK_API_KEY","llama":"LLAMA_API_KEY","alibaba":"ALIBABA_API_KEY"}
    key=os.getenv(api_map[provider_name])
    if not key: raise ValueError(f"{api_map[provider_name]} not set")
    return PROVIDERS[provider_name](api_key=key, model=model)
