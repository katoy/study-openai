import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class DescriptionGenerator:
    """OpenAI API を用いて検出結果に基づいた説明を生成するクラス"""

    def request_openai_completion(self, prompt):
        """OpenAI API でプロンプトに基づく説明を生成"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは物体認識の結果を説明するアシスタントです。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return response.choices[0].message['content'].strip()

    def generate_description(self, detections, max_length=100):
        """検出結果に基づき説明を生成"""
        labels = [label for label, _ in detections]
        prompt = f"以下の物体を検出しました: {', '.join(labels)}. これらの物体について説明してください。"
        
        full_description = ""
        while True:
            try:
                description = self.request_openai_completion(prompt)
                full_description += description
                if len(full_description) > max_length:
                    return self.trim_description(full_description, max_length)
                if self.is_sentence_complete(full_description):
                    break
                prompt = "続けてください: " + full_description
            except Exception as e:
                print(f"OpenAI API エラー: {e}")
                return "説明生成に失敗しました。"
        return full_description

    def trim_description(self, description, max_length=100):
        """指定文字数を超える場合、最後の文までで切り詰める"""
        if len(description) <= max_length:
            return description
        last_period_index = description.rfind("。", 0, max_length)
        return description[:last_period_index + 1] if last_period_index != -1 else description[:max_length]

    def is_sentence_complete(self, text):
        """文末が適切な句読点で終わっているかを確認"""
        return text.endswith(('.', '!', '?', '。', '！', '？'))
