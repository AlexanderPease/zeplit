import logging
import openai
from enum import Enum
from dataclasses import dataclass

openai.api_key = "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"


@dataclass
class OpenAIModel:
    name: str
    model_name: str
    max_tokens: int

class OpenAIModels(Enum):
    GPT3 = OpenAIModel(name="gpt3", model_name="text-davinci-003", max_tokens=4097)
    GPT35_Turbo = OpenAIModel(name="gpt35_turbo", model_name="gpt-3.5-turbo", max_tokens=4096)
    GPT4 = OpenAIModel(name="gpt4", model_name="gpt-4", max_tokens=8192)

def get_description_for_function(function):
    system_prompt = f"""Provide a succinct English language description of the Python function."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": function.code},
    ]

    response = openai.ChatCompletion.create(
        model=OpenAIModels.GPT35_Turbo.value.model_name,
        messages=messages,
        temperature=0.05,
    )
    return response["choices"][0]["message"]["content"]
