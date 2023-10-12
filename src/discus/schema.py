import pandas as pd
from enum import Enum
from discus.json.config import DiscusConfig

class SupportedModels(str, Enum):
    OpenAI = 'openai'
    HuggingFace = 'huggingface'

class TaskType(str, Enum):
    INSTRUCTIONS = "LLM-Instructions"
    INSTANCES = "LLM-Instances"

class SupportedEmbeddingModels(str, Enum):
    OpenAI = 'openai'
    HuggingFace = 'huggingface'
