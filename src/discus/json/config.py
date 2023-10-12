import json
from typing import Any, Dict

class DiscusConfig:
    """
    The class that parses the DiscusConfig.
    """
    def __init__(self, config_path: str) -> None:
        self.config_data = self._parse_config(config_path)
        self._set_attributes()
        
    def _set_attributes(self) -> None:
        """
        Set instance variables using keys from config data.
        Raise an error if a key is missing.
        """
        required_keys = [
            "task_name", "task_type", "task_explained",
            "model_provider", "model_name", 
            "number_of_rows", "generated_dataset_name"
        ]
        
        optional_keys = [
            "context_window_length", "embedding_model_provider", "embedding_model_name"
        ]
        
        for key in required_keys:
            try:
                setattr(self, key, self.config_data[key])
            except KeyError:
                raise ValueError(f"{key} doesn't exist")
        
        for key in optional_keys:
            setattr(self, key, self.config_data.get(key, None))

    def _parse_config(self, config_path: str) -> Dict[str, Any]:
        """
        Parse the JSON config file.
        """
        with open(config_path, "r") as file:
            return json.load(file)
