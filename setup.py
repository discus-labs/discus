from setuptools import setup

setup(
    name='Discus',
    version='0.1.1b0',
    description='A package containing everything you need to finetune your LLMs',
    url='https://github.com/discus-labs/discus-synthetics.git',
    author='Discus Founders',
    author_email='founders@discus.ai',
    packages=['discus'],
    install_requires=['openai','pandas','scikit-learn',"langchain==0.0.190", "chromadb==0.3.25",'tiktoken','glob2'],
)
