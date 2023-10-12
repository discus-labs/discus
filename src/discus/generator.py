import pandas as pd
import os
import json

from discus.schema import SupportedModels, TaskType
from discus.json.architecture import schema
from discus.json.config import DiscusConfig
from discus.models.openai import OpenAI
from discus.models.huggingface import HuggingFace
from discus.operations.instance import Instance
from discus.operations.instruction import Instruction

class Generator:

    def __init__(self, config):
        """Initialize the generator and parse the config.""" 
        self.config = DiscusConfig(config)
        self._validate_config()

    def _validate_config(self):
        """Validates the config against supported models and task types."""
        
        if self.config.model_provider not in SupportedModels._value2member_map_:
            raise ValueError(f"Unsupported model provider. Supported providers are: {list(SupportedModels)}")
        
        if self.config.task_type not in TaskType._value2member_map_:
            raise ValueError(f"Unsupported task type. Supported task types are: {list(TaskType)}")
    
    def run(self, seed_dataset='seed_dataset.csv', knowledge_base='/library/knowledgebase'):
        """Load seed dataset and generate the synthetic dataset based on the parsed config."""
        
        seed = None

        if os.path.exists(seed_dataset):
            seed = self._load_data(seed_dataset)
        
        model_name = self.config.model_name
        model_provider = self.config.model_provider
    
        if self.config.task_type == TaskType.INSTANCES: 
            instance_generator = Instance(self.config)
            prompt = instance_generator.generate_prompt(seed)

        if self.config.task_type == TaskType.INSTRUCTIONS:
            instruction_generator = Instruction(self.config)
            prompt = instruction_generator.generate_prompt(seed)
                
        if model_provider == 'openai':
            model = OpenAI(self.config)
            response = model._openai_generate(prompt = prompt)
            generated_data = model._get_data_from_model_response(response)

        elif model_provider == 'huggingface':
            model = HuggingFace(self.config)
            response = model._hf_generate(prompt = prompt)
            generated_data = response
        else:
            raise ValueError(f"Unsupported model provider. Supported providers are: {list(SupportedModels)}")

        if generated_data is None:
            raise ValueError("The data wasn't generated.")

        return generated_data
    
    def _load_data(self, file_path):
        """Load data from the CSV file."""
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Error loading data from {file_path}: {str(e)}")
