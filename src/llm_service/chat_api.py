"""封装大模型 API 调用（OpenAI / 智谱 / 文心一言等）"""

from openai import OpenAI


class LLMClient:
    """统一的大模型调用客户端"""

    def __init__(self, api_key: str, base_url: str | None = None):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def chat(self, messages: list[dict], model: str = "gpt-3.5-turbo") -> str:
        """发送对话请求"""
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content or ""
