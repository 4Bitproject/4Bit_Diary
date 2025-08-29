import google.generativeai as genai

from app.core.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)


class GeminiService:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-pro")

    async def summarize_diary(self, content: str) -> str:
        prompt = f"""
아래는 사용자가 작성한 일기 내용입니다. 이 일기의 핵심 내용을 간결하고 명확하게 요약해 주세요.

---
{content}
---

요약은 2~3문장 이내로 작성해 주세요.
        """

        try:
            response = await self.model.generate_content_async(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"AI 요약 생성 실패: {str(e)}")
