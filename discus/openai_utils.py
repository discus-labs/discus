import openai
API_KEY = None
LLM = None

def set_openai_llm(api_key):
    """
    Sets the OpenAI API key and allows the user to select the desired language model.

    Parameters:
        api_key (str): The OpenAI API key.

    Returns:
        None
    """
    global API_KEY, LLM
    API_KEY = api_key
    openai.api_key = API_KEY
    model_lst = openai.Model.list()
    available = []
    for i in model_lst['data']:
        if i['id'].startswith('gpt-3.5') or i['id'].startswith('gpt-4'):
            available.append(i['id'])
    text = ""
    for i in range(len(available)):
        text += f'{i}: {available[i]}\n'
    text += "Select the number of your desired model: "
    select = input(text)
    LLM = available[int(select)]

