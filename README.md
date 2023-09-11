# [Discus](https://discus.ai)

<div align="center" style="width:800px">
	
![Commit Activity](https://img.shields.io/github/commit-activity/m/discus-labs/discus) ![Stars](https://img.shields.io/github/stars/discus-labs/discus)

</div>


## ⚡ Quick Install

`pip install discus`

for the most recent version please do `pip install discus@git+https://github.com/discus-labs/discus`

## 📖 Documentation

[https://discus.ai/docs/index.html](https://discus.ai/docs/index.html)

## 🏷 What is Discus

Access to high-quality and large datasets is critical when it comes to ML testing/evaluation. Discus is a Python library that leverages LLM's to generate user guided data to solve this critical problem. 

Keep up with updates on our [twitter](https://twitter.com/discuslabs) or our [discord](https://discord.gg/t6ADqBKrdZ).

# Get Started with Discus
Here are a few quick steps to get Discus working.

After installing Discus, make sure to integrate in your LLM provider. For example,

```bash
export OPENAI_API_KEY=your-api-key-here
```

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
    "task_explained": "generate english to spanish translation.", # fill in the blank. "you are trying to _____"
    "generated_dataset_name": "eng2spanish.csv",
    "model_provider": "openai",
    "model_name": "gpt-3.5-turbo",
    "number_of_rows": "1500"
}
```

To run, import Discus. Then, create a Generator object.

```python
discus = Generator(config = "config_file_path")
generated_data = discus.run()
```

Achieve better results by providing your model with a seed dataset. 

```python
discus = Generator(config = "config_file_path", seed_dataset = "csv_file_path")
generated_data = discus.run()
```
---
## Support
Discus is a rapidly developing project. We welcome contributions in all forms - bug reports, pull requests and ideas for improving the library.

Open an issue on Github for bugs and request features.
Grab an open issue, and submit a pull request!
Discus is a rapidly developing project. We welcome contributions in all forms - bug reports, pull requests and ideas for improving the library.

1. Open an [issue](https://github.com/discus-labs/discus/issues) on Github for bugs and request features.
2. Grab an open issue, and submit a pull request!
