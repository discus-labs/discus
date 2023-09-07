from setuptools import setup

setup(
    name='Discus',
    version='0.1.1b0',
    description='generate high-quality data to unlock all AI possibilities',
    url='https://github.com/discus-labs/discus.git',
    author='Discus Founders',
    author_email='founders@discus.ai',
    packages=['discus'],
    install_requires=['os', 'openai','pandas','scikit-learn',"langchain==0.0.190", "chromadb==0.3.25",'tiktoken','glob2'],
)
