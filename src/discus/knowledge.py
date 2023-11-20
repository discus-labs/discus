import os
import pytesseract
import chromadb

from PIL import Image
from pdf2image import convert_from_path
from discus.json.architecture import schema
from discus.json.config import DiscusConfig
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from discus.schema import SupportedModels

class Knowledge: 
    
    def __init__(self, config):
        """Initializes Knowledge class with config"""
        self.config = DiscusConfig(config)
        self.raw_data = {} #Structure: {"filename": ({metadata}, "content")}
        self.chunked_data = []
        self.data_to_embed = [] #List of document objects
        self.db = None
        self.retriever = None


    def _validate_config(self):
        """Validates the config against supported models and task types."""

        """TODO: Add validation process for embedding models either here or in gneerator class"""
        pass

    def extract_data(self, path):
        """TODO: add docstring"""
        """TODO: extract metadata"""
        #supports pdfs, images, 
        for root, _, files in os.walk(path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_extension = os.path.splitext(file_path)[1].lower()
                content = ""
                metadata = {}
                metadata["Title/File Name"] = file_name
                try:
                    if file_extension == ".txt":
                        with open(file_path, "r") as file:
                            content = file.read()
                    else:
                        if file_extension == ".pdf":
                            images = convert_from_path(file_path)
                            for image in images:
                                text = pytesseract.image_to_string(image)
                                content += text
                        elif file_extension in [".img", ".jpg", ".jpeg", ".png", ".ico"]: 
                            images = Image.open(file_path)
                            content = pytesseract.image_to_string(image)
                        else:
                            raise IOError
                except IOError as _:
                    print(f"{file_path} is unreadable (hint: make sure your knowledge base directory only contains files of type .txt or .pdf")

                if content != "":
                    self.raw_data[file_name] = (metadata, content)
                    doc = Document(page_content=content, metadata=metadata)
     
        return self.raw_data
    

    def chunk_data(self, size_proportion = .2, overlap = .2, path=None):
        '''
        chunk_proporition is proportion of context window
        overlap is proportion of chunk which overlaps with the next
        path - a path to a directory containing data
        '''
        

        if not self.config.context_window_length:
            raise IOError("Invaild context window length: provide a context window length")
        context_window_length = int(self.config.context_window_length)
        if context_window_length <= 0:
            raise IOError("Invalid context window length: provide a context window length")
        if overlap < 0 or overlap > 1:
            raise IOError("Overlap must be between 0 and 1")

        if size_proportion < 0 or size_proportion > 1: 
            raise IOError("Size proportion must be bewteen 0 and 1")

        if len(self.raw_data) == 0 and not path:
            raise IOError("No data to chunk! hint: make sure you provide a path or a data dictionary (see docs)")
        
        if path: 
            self.raw_data = self.extract_data(path)

        for v in self.raw_data.values():
            metadata, text = v
            try:
                text_splitter = CharacterTextSplitter(
                    separator =  " ",
                    chunk_size = int(context_window_length * size_proportion),
                    chunk_overlap  = int(context_window_length * size_proportion * overlap)
                )

                split_text = text_splitter.split_text(text)
                for chunk in split_text:
                    doc = Document(page_content=chunk, metadata=metadata)
                    self.chunked_data.append(doc)
                    
            except: 
                name = metadata["Title/File Name"]
                print(f"{name} could not be chunked")
        
        self.data_to_embed = self.chunked_data
        return self.chunked_data


    def generate_embeddings(self, collection_name, persist_path):
        if len(self.data_to_embed) == 0:
            raise IOError("No data to embed! hint: run extract_data() or chunk_data() (see docs)")
        if len(self.chunked_data) == 0:
            print("Warning: embedding raw data, this may trigger errors with large file sizes, consider chunking and proceed with caution!")
        
        embedding_function_provider = self.config.embedding_model_provider
        if not embedding_function_provider or embedding_function_provider not in SupportedModels:
            raise IOError("Invalid embedding function provider! hint: provide a valid embedding function provider in your config (see docs)")
        
        embedding_function_name = self.config.embedding_model_name
        if not embedding_function_name:
            raise IOError("No embedding function! hint: provide an embedding function in your config (see docs)")
        

        if embedding_function_provider == "openai":
            embedding_function = OpenAIEmbeddings(model=embedding_function_name)

        elif embedding_function_provider == "huggingface":
            embedding_function = SentenceTransformerEmbeddings(model_name=embedding_function_name)
        
        else:
            raise IOError("Invalid embedding function provider! hint: provide a valid embedding function provider in your config (see docs)") 
            
        self.db = Chroma.from_documents(collection_name=collection_name, documents=self.data_to_embed, embedding=embedding_function, persist_directory=persist_path)
        self.db.persist()

        return self.db
    
    def load_db(self, collection_name, persist_path):
        embedding_function_provider = self.config.embedding_model_provider
        if not embedding_function_provider or embedding_function_provider not in SupportedModels:
            raise IOError("Invalid embedding function provider! hint: provide a valid embedding function provider in your config (see docs)")
        
        embedding_function_name = self.config.embedding_model_name
        if not embedding_function_name:
            raise IOError("No embedding function! hint: provide an embedding function in your config (see docs)")
        

        if embedding_function_provider == "openai":
            embedding_function = OpenAIEmbeddings(model=embedding_function_name)

        elif embedding_function_provider == "huggingface":
            embedding_function = SentenceTransformerEmbeddings(model_name=embedding_function_name)
        
        else:
            raise IOError("Invalid embedding function provider! hint: provide a valid embedding function provider in your config (see docs)")

        self.db = Chroma(collection_name=collection_name, embedding_function=embedding_function, persist_directory=persist_path)

        return self.db
    
    def naive_retriever(self, k=3):
        if not self.db:
            raise IOError("No embeddings! hint: make sure you generate and store or load embeddings!")
        
        self.retriever = self.db.as_retriever(search_kwargs={"k": k})
        
        return self.retriever
    def retriever(self, query):
        return self.retriever.invoke(query)

