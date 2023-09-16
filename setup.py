from setuptools import setup, find_packages

setup(
    name='Discus',
    version='0.1.3b0',
    description='Generate high-quality data to unlock all AI possibilities',
    url='https://github.com/discus-labs/discus.git',
    author='Discus Founders',
    author_email='founders@discus.ai',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'openai',
        'pandas',
        'scikit-learn',
        'langchain==0.0.190',
        'chromadb==0.3.25',
        'tiktoken',
        'glob2',
    ],
)