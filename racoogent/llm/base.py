from abc import ABC, abstractmethod
class BaseLLM(ABC):
 @abstractmethod
 def chat(self, messages, tools=None): pass
