import json

class DiscusConfig:
    """The class that parses the DiscusConfig."""
    def __init__(self, config_path):
        self.config_data = self._parse_config(config_path)
        
        # Setting parameters as instance variables
        try:
            self.task_name = self.config_data["task_name"]
        except KeyError:
            raise ValueError("Task_name doesn't exist")
        
        try:
            self.task_type = self.config_data["task_type"]
        except KeyError:
            raise ValueError("Task_type doesn't exist")

        try:
            self.task_explained = self.config_data["task_explained"]
        except KeyError:
            raise ValueError("Task_explained doesn't exist")
        
        try:
            self.generated_dataset_name = self.config_data["generated_dataset_name"]
        except KeyError:
            raise ValueError("Generated_dataset_name doesn't exist")

        try:
            self.model_provider = self.config_data["model_provider"]
        except KeyError:
            raise ValueError("Model_provider doesn't exist")

        try:
            self.model_name = self.config_data["model_name"]
        except KeyError:
            raise ValueError("Model_name doesn't exist")

        try:
            self.number_of_rows = self.config_data["number_of_rows"]
        except KeyError:
            raise ValueError("Number_of_rows doesn't exist")

    def _parse_config(self, config_path):
        """Parse the JSON config file."""
        with open(config_path, "r") as file:
            return json.load(file)
