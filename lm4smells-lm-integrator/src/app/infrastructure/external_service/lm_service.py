import ollama
from infrastructure.abstractions.lm_base_service import LMBaseService
from infrastructure.config.settings import settings
from infrastructure.external_service.commands.lm_result import LMResult
import requests

class LMService(LMBaseService):
    def __init__(self):
        super().__init__()

    def send_message(self, model: str,  prompt: str):
        response = ollama.chat(
            model=model,
            stream=False,
            messages=[{
                'role': 'user',
                'content': prompt
            }],
            format=LMResult.model_json_schema(),
        )

        if 'message' in response and 'content' in response['message']:
            try:
                return LMResult.model_validate_json(response['message']['content'])
            except Exception:
                print("[WARNING] The file format is not JSON")

        return response['message']['content']

    def send_message_gpt(self, model: str, prompt: str):
        headers = {
            "Authorization": f"Bearer {settings.llm_gpt_api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        }

        response = requests.post(f"{settings.llm_gpt_host}/chat/completions", headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            response.raise_for_status()