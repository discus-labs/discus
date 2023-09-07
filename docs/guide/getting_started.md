# Get Started with Discus

## Introduction

Here are a few quick steps to get Discus working.

---

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Basic Usage](#basic-usage)
4. [Advanced Usage](#advanced-usage)
5. [Support](#support)

---

## Installation

To install Discus, run the following command:

```bash
pip install discus
```

Now, make sure to integrate in your LLM provider. For example,

```bash
export OPENAI_API_KEY=your-api-key-here
```

---
## Installation

We can now get started. First, create your json following these guidelines:

* task_name: what you want to call your task
* task_type: the type of data you want to generate. Currently either LLM-Instances or LLM-Instructions
* task_explained: the specific guidelines of your task.
* generated_dataset_name: what you want the returned csv to be called.
* model_provider: the LLM you want to use. Currently only OpenAI.
* model_name: the exact model from your provider.
* number_of_rows: the number of data points you want to generate/enrich

```python
config = {
    "task_name": "English2Spanish",
    "task_type": "LLM-Instances",
    "task_explained": "english to to spanish",
    "generated_dataset_name": "eng2spanish.csv",
    "model_provider": "openai",
    "model_name": "gpt-3.5-turbo",
    "number_of_rows": "1500"
}
```

--- 
## Basic Usage

To run, import Discus. Then, create a Generator object.

```python
discus = Generator(config = "config_file_path")
generated_data = discus.run()
```

--- 
## Advanced Usage

Achieve better results by providing your model with a seed dataset. 

Seed dataset must be a csv without any extra columns. 
```python
discus = Generator(config = "config_file_path", seed_dataset = "csv_file_path")
generated_data = discus.run()
```
---
## Support
Discus is a rapidly developing project. We welcome contributions in all forms - bug reports, pull requests and ideas for improving the library.

Open an issue on Github for bugs and request features.
Grab an open issue, and submit a pull request!
