import random
import pandas as pd
from discus.json.config import DiscusConfig

class Instruction:
    def __init__(self, config: DiscusConfig) -> None:
        self.config = config

    def generate_prompt(self, seed_dataset: pd.DataFrame = None,  context = None) -> list:
        command = ""

        num_instructions = self.config.number_of_rows

        if seed_dataset is not None:
            self.seed_dataset = seed_dataset
            seed_examples = self.transform_dataframe(seed_dataset)

            for i in range(len(seed_examples)):
                instruction_text = seed_examples[i]["input"]
                command += f"Example Instruction {i + 1}: {instruction_text}\n"

        generate_options = ["create",
                            "produce",
                            "generate",
                            "formulate",
                            "develop",
                            "construct",
                            "make",
                            "fabricate",
                            "write",
                            "compose"]

        generate_synonym = random.choice(generate_options)

        adjective_options = [
            "fresh, unique, and innovative",
            "novel, inventive, and imaginative",
            "unprecedented, pioneering, and imaginative",
            "cutting-edge, innovative, and inventive",
            "innovative, imaginative, and groundbreaking",
            "unconventional, creative, and original",
            "inventive, visionary, and novel",
            "imaginative, fresh, and innovative",
            "creative, groundbreaking, and trailblazing",
            "original, inventive, and imaginative"
        ]
        adjective_synonym = random.choice(adjective_options)


        command += f"Using the above examples, {generate_synonym} {num_instructions} {adjective_synonym} instructions. Format the instructions like \"Instruction: <instruction>\", separating each new instruction with a newline."
        

        task_guidelines = self.config.task_explained
        command += f"{task_guidelines}\n"

        message = []
        if context:
            context_array = context
            message = context_array + [{"role": "user", "content": command}]
        else:
            message = [
                {"role": "system",
                 "content": "You are a helpful data scientist AI assistant helping generate instructions to teach a large language model. You are trying to " + task_guidelines},
                {"role": "user", "content": command}
            ]
        return message
            

    def transform_dataframe(self, df):
        """
        Transforms a DataFrame into a list of dictionaries.

        Parameters:
            df (pandas.DataFrame): The DataFrame to be transformed.

        Returns:
            list: A list of dictionaries containing 'input' and 'output' keys.
        """
        if df.shape[1] != 2:
            raise ValueError("The dataframe must have exactly 2 columns.")

        transformed_data = []

        for row in df.itertuples(index=False):
            input_text = str(row[0])
            output_text = str(row[1])
            transformed_data.append({"input": input_text, "output": output_text})

        return transformed_data
