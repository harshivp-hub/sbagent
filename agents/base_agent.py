# agents/base_agent.py

import json
import os
from typing import Dict, Any

import openai

class BaseAgent:
    def __init__(self, model: str):
        self.model = model

    def call_llm(self, prompt: str) -> str:
        """
        Use the new openai.chat.completions.create interface.
        If anything goes wrong, return '{}' so analyze() can fall back.
        """
        try:
            # New (v1+) ChatCompletion interface
            resp = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system",  "content": "You are a cloud optimization assistant."},
                    {"role": "user",    "content": prompt}
                ]
            )
            return resp.choices[0].message.content
        except Exception as e:
            # Log to stderr or a logger if you want:
            # print("LLM call failed:", e, file=sys.stderr)
            return "{}"

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement analyze()")
