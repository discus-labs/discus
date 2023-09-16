from discus.json.config import DiscusConfig
import os
import openai
import pandas as pd

class OpenAI:
    

    def __init__(self, config: DiscusConfig) -> None:
        self.config = config
        self.model_name = config.model_name or "gpt-3.5-turbo"

        if os.getenv("OPENAI_API_KEY") is None:
            raise ValueError("OPENAI_API_KEY environment variable not set")

    def _openai_generate(self, prompt):

        responses = []
        data = []
        message = prompt

        response = openai.ChatCompletion.create(
            model= self.model_name,
            messages=message,
            temperature=0.7
        )

        finish_reason = response.choices[0].finish_reason

        if finish_reason == 'length':
            lines = lines[:-1]
            if lines:
                last_line = lines[-1]
                if 'Input:' in last_line:
                    lines = lines[:-1]

        if finish_reason == 'length':
            if len(data) == 0:
                raise ValueError(
                    "Your instruction generations are exceeding the max token length. Consider providing shorter seed instructions or setting a lower max_length parameter.")

        if finish_reason == 'content_filter':
            raise ValueError(
                "Your instruction generations violate OpenAI's content policy. Consider providing more acceptable seed instructions.")

        return response

    def _get_data_from_model_response(self, response):
        content = response["choices"][0]["message"]["content"]
        data_dict = {}
        pairs = content.split("\n\n")

        for pair in pairs:
            line_dict = {}
            lines = pair.split("\n")
            for line in lines:
                key, value = line.split(": ", 1)
                line_dict[key] = value

            for key, value in line_dict.items():
                if key not in data_dict:
                    data_dict[key] = []
                data_dict[key].append(value)

        df = pd.DataFrame(data_dict)
        return df