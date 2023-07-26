import discus.openai_utils as openai_utils
import openai
import random
import pandas as pd

def generate_instances(seed_examples,num_instances,instruction=None, max_input_length=None, max_output_length=None):
    """
    Generates instances using the configured language model.

    Parameters:
        seed_examples (list): A list of seed examples used to generate new instances. Each item in the list should be a dictionary with two keys: input and output.
        num_instances (int): The number of instances to generate.
        instruction (str, optional): An additional instruction to guide instance generation. Default is None.
        max_input_length (int, optional): The maximum number of words allowed per input. Default is None.
        max_output_length (int, optional): The maximum number of words allowed per output. Default is None.

    Returns:
        pandas.DataFrame: A DataFrame containing the generated instances with 'input' and 'output' columns.
    """
    satisfied = False
    context = None
    while not satisfied:
        interim_results = _openai_generate_instances(seed_examples,10,instruction,max_input_length,max_output_length, context = context)
        message = interim_results['message']
        instances = interim_results['instances']
        text = 'Below are 10 examples of the generated instances:\n'
        for i in range(len(instances)):
            text += f'{i+1}\t'
            text += f'Input: {instances[i]["input"]}\n'
            text += f'\tOutput: {instances[i]["output"]}\n'
        text += 'If you are satisfied with these instances, press y. Otherwise, press n: '
        done = input(text)
        if done == 'y':
            satisfied = True
            final_results = _openai_generate_instances(seed_examples, num_instances, instruction, max_input_length, max_output_length, context = message)
            final_instances = final_results['instances']
            final_df = pd.DataFrame(final_instances,columns=['input', 'output'])
            print('Finished Generating Instances')
            return final_df
        else:
            feedback = input("Provide some concise feedback to improve the generated instances: ")
            context = message + [{"role": "user", "content": feedback}]

def transform_dataframe(df):
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

def _openai_generate_instances(seed_examples, num_instances, instruction=None, max_input_length=None, max_output_length=None, context=None):
    if len(seed_examples) < 8:
        raise ValueError("Please provide at least 8 seed examples for the function to work.")

    openai.api_key = openai_utils.API_KEY
    model = openai_utils.LLM
    instances = []
    responses = []
    if context:
        responses.append(context[-1])
    while len(instances) < num_instances:
        samples = []
        if len(instances) >= 2:
            selected_instructions = random.sample(instances, 2)
            selected_seed_examples = random.sample(seed_examples, 2)
            selected_combination = random.sample(seed_examples + instances, 4)
            samples = selected_instructions + selected_seed_examples + selected_combination
        else:
            samples = random.sample(seed_examples, 8)

        command = ""
        for i in range(len(samples)):
            input_text = samples[i]["input"]
            output_text = samples[i]["output"]
            command += f"Example Input {i + 1}: {input_text}\n"
            command += f"Example Output {i + 1}: {output_text}\n"

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

        if max_input_length and max_output_length:
            command += f"Using the above examples and context, {generate_synonym} {num_instances - len(instances)} {adjective_synonym} input/output combos with a max of {max_input_length} words per input and {max_output_length} words per output. Format the input/output combos like below:\n\"Input: <input>\"\n\"Output: <output>\"\nSeparate each new input/output with a newline."
        elif max_input_length:
            command += f"Using the above examples and context, {generate_synonym} {num_instances - len(instances)} {adjective_synonym} input/output combos with a max of {max_input_length} words per input. Format the input/output combos like below:\n\"Input: <input>\"\n\"Output: <output>\"\nSeparate each new input/output with a newline."
        elif max_output_length:
            command += f"Using the above examples and context, {generate_synonym} {num_instances - len(instances)} {adjective_synonym} input/output combos with a max of {max_output_length} words per output. Format the input/output combos like below:\n\"Input: <input>\"\n\"Output: <output>\"\nSeparate each new input/output with a newline."
        else:
            command += f"Using the above examples and context, {generate_synonym} {num_instances - len(instances)} {adjective_synonym} input/output combos. Format the input/output combos like below:\n\"Input: <input>\"\n\"Output: <output>\"\nSeparate each new input/output with a newline."

        if instruction:
            command += f" Remember to generate input/output combos that make sense in the context of the following instruction: {instruction}"

        message = []

        if context:
            context_array = context
            message = context_array + [{"role": "user", "content": command}]
        else:
            message = [
                {"role": "system",
                 "content": "You are a helpful AI assistant trying to help someone generate instructions they could potentially teach a large-language model."},
                {"role": "user", "content": command}
            ]
            
        response = openai.ChatCompletion.create(
            model=model,
            messages=message,
            temperature=0.7
        )

        resp = response.choices[0].message
        message.append(resp)
        responses.append(resp)
        finish_reason = response.choices[0].finish_reason
        text = resp["content"].strip()
        lines = text.split('\n')

        if finish_reason == 'length':
            lines = lines[:-1]
            if lines:
                last_line = lines[-1]
                if 'Input:' in last_line:
                    lines = lines[:-1]

        for i in range(len(lines)):
            if 'Input: ' in lines[i]:
                input_text = lines[i].split('Input: ')[1].strip()
                output_text = lines[i + 1].split('Output: ')[1].strip()
                instances.append({"input": input_text, "output": output_text})

        if finish_reason == 'length':
            if len(instances) == 0:
                raise ValueError(
                    "Your instruction generations are exceeding the max token length. Consider providing shorter seed instructions or setting a lower max_length parameter.")

        if finish_reason == 'content_filter':
            raise ValueError(
                "Your instruction generations violate OpenAI's content policy. Consider providing more acceptable seed instructions.")

    return {
        "instances": instances,
        "message": responses
    }
