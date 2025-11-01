from app.config.settings import GEMINI_API_KEY, logger
from google import generativeai as genai
from typing import Dict
import re
import json
import time

genai.configure(api_key=GEMINI_API_KEY)

class Agent:
    # Custom Exceptions
    class GenerateError(Exception):
        pass
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.prompt_path = "./app/prompts/generate_news.txt"
        self.logger = logger

    def generate_response(self, msg: str) -> str | None:
        try:
            self.logger.info("Send message to AI ...")
            response = self.model.generate_content(msg)
            self.logger.info("Return AI response ...")
            return response.text
        except Exception as e:
            raise Exception(e)

    def read_prompt(self, path: str) -> str:
        self.logger.debug(f"Reading this file -> {path}")
        with open(path, "r", encoding='utf-8') as prompt:
            return prompt.read()
    
    def generate_news(self) -> str:
        try:
            prompt = self.read_prompt(self.prompt_path)
            ai_response = self.generate_response(prompt)
            return ai_response
        except Agent.GenerateError as e:
            raise Agent.GenerateError(str(e))

    def extract_json(self, text: str) -> Dict[str, str] | None:
        match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if not match:
            match = re.search(r"(\{.*\})", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                return None
        return None
        
    def format_news(self, generated_news: str, max_retries: int = 3, retry_delay: float = 1.0) -> Dict[str, str]:
        for attempt in range(1, max_retries):
            try:
                news = self.extract_json(generated_news)
                if news is not None:
                    return news
                else:
                    raise Agent.GenerateError("Error to generate news!")
            except Agent.GenerateError:
                if attempt < max_retries:
                    self.logger.debug(f"[Attempt {attempt}] JSON invalid. Try Again...")
                    time.sleep(retry_delay)
                    generated_news = self.generate_news()
                else:
                    raise Agent.GenerateError("Error when trying to generate a news item multiple times.")
            
