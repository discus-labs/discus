from typing import List
from discus.schema import SupportedModels, TaskType 

def retrieve_supported_models() -> List[str]:
    """Generate given model providers.
    
    This function retrieves the list of model providers from SupportedModels enum.
    """
    return [enum_member.value for enum_member in SupportedModels]

def retrieve_task_types() -> List[str]:
    """Generate given task types.
    
    This function retrieves the list of acceptable task_types from TaskType enum.
    """
    return [enum_member.value for enum_member in TaskType]

# architecture definition for Generator
schema = {
    "$schema": "ADD A LINK THAT AUTO DOWNLOADS TEMPLATE JSON FOR DISCUS",
    "title": "Discus Config",
    "description": "The configuration to generate datasets",
    "type": "object",
    "properties": {
        "task_name": {
            "type": "string",
            "description": "The name of the task (for example: English2Spanish)",
        },
        "task_type": {
            "enum": retrieve_task_types(),
            "description": "The type of task",
        },
        "task_explained": {
            "type": "string",
            "description": "Highly specific guidelines or explanation of what the task is",
        },
        "generated_dataset_name": {
            "type": "string",
            "description": "Name for the generated dataset",
        },
        "model_provider": {
            "enum": retrieve_supported_models(),
            "description": "The provider of the model",
        },
        "model_name": {
            "type": "string",
            "description": "The specific name of the model to be used",
        },
        "number_of_rows": {
            "type": "string",
            "description": "The number of rows to generate",
        },
    },
    "required": [
        "task_name",
        "task_type",
        "task_explained",
        "model_provider",
        "model_name",
    ],
    "additionalProperties": False,
}
