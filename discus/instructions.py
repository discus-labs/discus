import discus.openai_utils as openai_utils
import openai
import random

def generate_instructions(seed_examples,num_instructions,max_length=None):
    """
    Generates instructions using the configured language model.

    Parameters:
        seed_examples (list): A list of seed examples used to generate new instructions.
        num_instructions (int): The number of instructions to generate.
        max_length (int, optional): The maximum number of words allowed per instruction. Default is None.

    Returns:
        list: A list of generated instructions.
    """
    satisfied = False
    context = None
    while not satisfied:
        interim_results = _openai_generate_instructions(seed_examples,10,max_length, context = context)
        message = interim_results['message']
        instructions = interim_results['instructions']
        text = 'Below are 10 examples of the generated instructions:\n'
        for i in range(len(instructions)):
            text += f'{i+1}\t'
            text += f'{instructions[i]}\n'
        text += 'If you are satisfied with these instructions, press y. Otherwise, press n: '
        done = input(text)
        if done == 'y':
            satisfied = True
            final_results = _openai_generate_instructions(seed_examples, num_instructions, max_length, context = message)
            final_instructions = final_results['instructions']
            print('Finished Generating Instructions')
            return final_instructions
        else:
            feedback = input("Provide some concise feedback to improve the generated instructions: ")
            context = message + [{"role": "user", "content": feedback}]

def _openai_generate_instructions(seed_examples, num_instructions, max_length=None, context=None):
    if len(seed_examples) < 8:
        raise ValueError("Please provide at least 8 seed examples for the function to work.")

    openai.api_key = openai_utils.API_KEY
    model = openai_utils.LLM
    instructions = []
    responses = []
    if context:
        responses.append(context[-1])
    while len(instructions) < num_instructions:
        samples = []
        if len(instructions) >= 2:
            selected_instructions = random.sample(instructions, 2)
            selected_seed_examples = random.sample(seed_examples, 2)
            selected_combination = random.sample(seed_examples + instructions, 4)
            samples = selected_instructions + selected_seed_examples + selected_combination
        else:
            samples = random.sample(seed_examples, 8)

        command = ""
        for sample in samples:
            command += f"Example Instruction: {sample}\n"

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

        if max_length != None:
            command += f"Using the above examples, {generate_synonym} {num_instructions - len(instructions)} {adjective_synonym} instructions with a max of {max_length} words per instruction. Format the instructions like \"Instruction: <instruction>\", separating each new instruction with a newline."
        else:
            command += f"Using the above examples, {generate_synonym} {num_instructions - len(instructions)} {adjective_synonym} instructions. Format the instructions like \"Instruction: <instruction>\", separating each new instruction with a newline."

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

        for line in lines:
            if 'Instruction: ' in line:
                instruction_text = line.split('Instruction: ')[1].strip()
                instructions.append(instruction_text)

        if finish_reason == 'length':
            if len(instructions) == 0:
                raise ValueError(
                    "Your instruction generations are exceeding the max token length. Consider providing shorter seed instructions or setting a lower max_length parameter.")

        if finish_reason == 'content_filter':
            raise ValueError(
                "Your instruction generations violate OpenAI's content policy. Consider providing more acceptable seed instructions.")

    return {
        "instructions": instructions,
        "message": responses
    }

