from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
import discus.openai_utils as openai_utils
import openai
from langchain.document_loaders import TextLoader
import pandas as pd
import os
import glob2

### needs to be integrated still into the new architecture

def create_vector_store(documents_path,vector_store_path='vector_db',chunks=512,overlap=20):
    """
    Create a vector store from text documents using OpenAI embeddings.

    This function reads text documents from a specified path, processes them using OpenAI embeddings,
    and creates a vector store for efficient text similarity searches using Chroma.

    Parameters:
    documents_path (str): The path to the directory containing the text documents.
    vector_store_path (str, optional): The path where the vector store will be saved. Defaults to 'vector_db'.
    chunks (int, optional): The chunk size in characters for splitting the documents. Defaults to 512.
    overlap (int, optional): The character overlap between chunks. Defaults to 20.

    Returns:
    None

    Note:
    This function sets the OpenAI API key using the 'OPENAI_API_KEY' environment variable from your 'openai_utils' module.
    It reads text documents from the specified path, splits them into chunks, processes them using OpenAI embeddings,
    and then creates and persists a Chroma vector store for efficient text similarity searches.
    """
    os.environ["OPENAI_API_KEY"] = openai_utils.API_KEY
    docs = []
    text_splitter = CharacterTextSplitter(chunk_size=chunks, chunk_overlap=overlap)
    for file_path in glob2.glob(os.path.join(documents_path, "*.txt")):
        loader = TextLoader(file_path)
        documents = loader.load()
        [docs.append(doc) for doc in text_splitter.split_documents(documents)]

    embedding_function = OpenAIEmbeddings()

    docsearch = Chroma.from_documents(documents=docs, embedding=embedding_function,
                                  persist_directory=vector_store_path)

    docsearch.persist()
    return docsearch, docs

def load_vector_store(vector_store_path):
    """
    Load a Chroma vector store from a specified path.

    This function loads a previously created Chroma vector store from the specified path and returns it.

    Parameters:
    vector_store_path (str): The path where the vector store is saved.

    Returns:
    Chroma: The loaded Chroma vector store.

    Note:
    This function sets the OpenAI API key using the 'OPENAI_API_KEY' environment variable from your 'openai_utils' module.
    It loads the vector store using the provided path and creates an instance of the OpenAIEmbeddings class for embedding.
    The returned Chroma instance can be used for efficient text similarity searches.
    """
    os.environ["OPENAI_API_KEY"] = openai_utils.API_KEY
    embeddings = OpenAIEmbeddings()
    return Chroma(persist_directory=vector_store_path,embedding_function=embeddings)

def query_vector_store(vector_db,query):
    """
    Query a Chroma vector store for relevant documents and generate a response using OpenAI's chat model.

    This function queries a Chroma vector store using the provided query, retrieves relevant documents,
    and generates a response to the query using OpenAI's chat model.

    Parameters:
    vector_db (Chroma): The Chroma vector store instance to be queried.
    query (str): The query to search for relevant documents and generate a response.

    Returns:
    str: The generated response to the query.

    Note:
    This function sets the OpenAI API key using the 'OPENAI_API_KEY' environment variable from your 'openai_utils' module.
    It queries the Chroma vector store to retrieve relevant documents and uses the provided query to generate a response
    using OpenAI's chat model. The response is returned as a string.
    """
    os.environ["OPENAI_API_KEY"] = openai_utils.API_KEY
    docsearch = vector_db.as_retriever(search_type="mmr", search_kwargs={"k": 2})
    docs = docsearch.get_relevant_documents(query)
    openai.api_key = openai_utils.API_KEY
    model = openai_utils.LLM
    if len(docs) == 1:
        prompt = "Below is some context:\n"
        prompt += docs[0].page_content
        prompt += f"\nUsing the above context, answer the following query: {query}. If you don't have the information to answer the query, just say that you are unable to answer the query."
    elif len(docs) == 2:
        prompt = "Below are two pieces of context:\n"
        prompt += docs[0].page_content
        prompt += "\n"
        prompt += docs[1].page_content
        prompt += f"\nUsing the above context, answer the following query: {query}. If you don't have the information to answer the query, just say that you are unable to answer the query."
    else:
        prompt = f"Answer the following query: {query}. If you don't have the information to answer the query, just say that you are unable to answer the query."

    message = [
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=message,
        temperature=0.7
    )

    resp = response.choices[0].message
    text = resp["content"].strip()

    return text

def complete_instances(inputs, vector_db, instruction = None, max_length=None):
    """
    Generate completions for a list of input instances using contextual information and OpenAI's chat model.

    This function takes a list of input instances, retrieves relevant contextual information from a Chroma vector store,
    and generates completions for each input instance using OpenAI's chat model.

    Parameters:
    inputs (list): A list of input instances for which completions are to be generated.
    vector_db (Chroma): The Chroma vector store instance to retrieve contextual information.
    instruction (str, optional): An additional instruction for generating meaningful completions. Defaults to None.
    max_length (int, optional): The maximum word count for generated completions. Defaults to None.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the input instances and their corresponding generated completions.

    Note:
    This function sets the OpenAI API key using the 'OPENAI_API_KEY' environment variable from your 'openai_utils' module.
    It retrieves relevant contextual information using the Chroma vector store, generates completions for each input
    instance using OpenAI's chat model, and returns a DataFrame containing input instances and their completions.
    """
    os.environ["OPENAI_API_KEY"] = openai_utils.API_KEY
    docsearch = vector_db.as_retriever(search_type="mmr", search_kwargs={"k": 2})
    openai.api_key = openai_utils.API_KEY
    model = openai_utils.LLM
    outputs = []
    for i in inputs:
        docs = docsearch.get_relevant_documents(i)
        if len(docs) == 1:
            prompt = "Below is some context:\n"
            prompt += docs[0].page_content
            if max_length:
                prompt += f"\nUsing the above context, generate an output with a max word count of {max_length} corresponding to the following input: {i}."
            else:
                prompt += f"\nUsing the above context, generate an output corresponding to the following input: {i}."
            if instruction:
                prompt += f" Remember to generate an output that make sense in the context of the following instruction: {instruction}"
        elif len(docs) == 2:
            prompt = "Below are two pieces of context:\n"
            prompt += docs[0].page_content
            prompt += "\n"
            prompt += docs[1].page_content
            if max_length:
                prompt += f"\nUsing the above context, generate an output with a max word count of {max_length} corresponding to the following input: {i}."
            else:
                prompt += f"\nUsing the above context, generate an output corresponding to the following input: {i}."
            if instruction:
                prompt += f" Remember to generate an output that make sense in the context of the following instruction: {instruction}"
        else:
            if max_length:
                prompt += f"Using the above context, generate an output with a max word count of {max_length} corresponding to the following input: {i}."
            else:
                prompt += f"Using the above context, generate an output corresponding to the following input: {i}."
            if instruction:
                prompt += f" Remember to generate an output that make sense in the context of the following instruction: {instruction}"

        message = [
            {"role": "user", "content": prompt}
        ]

        response = openai.ChatCompletion.create(
            model=model,
            messages=message,
            temperature=0.7
        )

        resp = response.choices[0].message
        text = resp["content"].strip()
        outputs.append({'input':i,'output':text})

    return pd.DataFrame(outputs,columns=['input', 'output'])

def generate_prompts(documents_path, instruction=None, max_length=None, chunks=512, overlap=20):
    """
    Generate a comprehensive list of prompts based on text documents and OpenAI's chat model.

    This function reads text documents from a specified path, generates prompts based on contextual information,
    and returns a comprehensive list of prompts that users might ask an LLM using OpenAI's chat model.

    Parameters:
    documents_path (str): The path to the directory containing the text documents.
    instruction (str, optional): An additional instruction for generating meaningful prompts. Defaults to None.
    max_length (int, optional): The maximum word count for generated prompts. Defaults to None.
    chunks (int, optional): The chunk size in characters for splitting the documents. Defaults to 512.
    overlap (int, optional): The character overlap between chunks. Defaults to 20.

    Returns:
    list: A list of generated prompts.

    Note:
    This function sets the OpenAI API key using the 'OPENAI_API_KEY' environment variable from your 'openai_utils' module.
    It reads text documents from the specified path, generates prompts based on contextual information, and returns
    a list of prompts that users might ask an LLM. The prompts are generated using OpenAI's chat model.
    """
    docs = []
    prompts = []
    openai.api_key = openai_utils.API_KEY
    model = openai_utils.LLM
    text_splitter = CharacterTextSplitter(chunk_size=chunks, chunk_overlap=overlap)

    for file_path in glob2.glob(os.path.join(documents_path, "*.txt")):
        loader = TextLoader(file_path)
        documents = loader.load()
        [docs.append(doc) for doc in text_splitter.split_documents(documents)]

    for d in docs:
        prompt = "Below is some context:\n"
        prompt += f"{d.page_content}\n"
        if max_length:
            prompt += f"Using the above context, generate a comprehensive list of prompts with a max of {max_length} words per prompt that users might ask an LLM. Output each generated prompt on a separate line and format the lines like \"Prompt: <prompt>\""
        else:
            prompt += f"Using the above context, generate a comprehensive list of prompts that users might ask an LLM. Output each generated prompt on a separate line and format the lines like \"Prompt: <prompt>\""
        if instruction:
            prompt += f" Remember to generate prompts that make sense in context of the following instruction: {instruction}"

        message = [
            {"role": "user", "content": prompt}
        ]

        response = openai.ChatCompletion.create(
            model=model,
            messages=message,
            temperature=0.7
        )

        resp = response.choices[0].message
        text = resp["content"].strip()
        lines = text.split('\n')

        for line in lines:
            if 'Prompt: ' in line:
                prompt = line.split('Prompt: ')[1].strip()
                prompts.append(prompt)

    return prompts
