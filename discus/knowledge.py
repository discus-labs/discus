from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
import discus.openai_utils as openai_utils
import openai
from langchain.document_loaders import TextLoader
import pandas as pd

import os
import glob2

def create_vector_store(documents_path,vector_store_path='vector_db',chunks=512,overlap=20):
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
    os.environ["OPENAI_API_KEY"] = openai_utils.API_KEY
    embeddings = OpenAIEmbeddings()
    return Chroma(persist_directory=vector_store_path,embedding_function=embeddings)

def query_vector_store(vector_db,query):
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

def generate_prompts(documents_path,instruction=None,max_length=None,chunks=512,overlap=20):
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
