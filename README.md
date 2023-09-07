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

## 🚀 Getting started


In order to use this package, you need to first install it.

```bash
pip install discus
```

Now, you can import the package and set the OpenAI key.

```bash
import discus.openai_utils as utils
import discus.instructions as instructions
import discus.instances as instances
import discus.cleaning as cleaning

utils.set_openai_llm("OPENAI_API_KEY")
```

After executing the set_openai_llm function, you will be prompted for input in the console as shown below.

```bash
0: gpt-4-0314
1: gpt-3.5-turbo-16k-0613
2: gpt-3.5-turbo-0301
3: gpt-3.5-turbo-16k
4: gpt-4
5: gpt-3.5-turbo-0613
6: gpt-3.5-turbo
7: gpt-4-0613
Select the number of your desired model: 5
```

### Generate Instructions

```bash
seed_examples = [
'Write a description of a famous landmark in at least 200 words.',
'Generate a short story that involves time travel and a surprising twist ending.',
'Compose a persuasive essay arguing for the importance of renewable energy sources.',
'Write a step-by-step tutorial on how to bake a chocolate chip cookie.',
'Create a dialogue between two characters discussing the benefits and drawbacks of social media.',
'Generate a list of ten useful productivity tips for managing time effectively.',
'Write a review of a recent movie, including your thoughts on the plot, acting, and cinematography.',
'Compose a letter of recommendation for a coworker highlighting their skills and accomplishments.',
'Write a speech on the importance of mental health and strategies for self-care.',
'Generate a poem that evokes a sense of tranquility and appreciation for nature.'
]

new_instructions = instructions.generate_instructions(seed_examples,20)
```

After executing the generate_instructions function, you will be prompted for input in the console as shown below.

```bash
Below are 10 examples of the generated instructions:
1	Write a detailed travel guide for a fictional city, including information on its history, attractions, and local cuisine, in at least 500 words.
2	Create a superhero origin story, complete with an unique superpower, a compelling backstory, and a formidable archenemy.
3	Write a persuasive essay arguing for the implementation of renewable energy sources as the primary means of power generation worldwide.
4	Design a board game that combines elements of strategy, problem-solving, and teamwork, providing clear rules and objectives.
5	Compose a series of short dialogues between animals in a zoo, capturing their thoughts, emotions, and unique personalities.
6	Write a step-by-step guide on how to build a sustainable garden, incorporating eco-friendly practices and maximizing space utilization.
7	Create a comprehensive training program for aspiring astronauts, including physical fitness routines, mental resilience exercises, and simulated space missions.
8	Write a script for a short film set in a post-apocalyptic world, exploring themes of survival, hope, and human resilience.
9	Compose a collection of haikus that celebrate the beauty and serenity of different seasons, capturing vivid imagery and emotions.
10	Design a futuristic cityscape, illustrating innovative architectural concepts, advanced transportation systems, and sustainable living solutions.
If you are satisfied with these instructions, press y. Otherwise, press n: n
Provide some concise feedback to improve the generated instructions: make them more related to school
Below are 10 examples of the generated instructions:
1	Write a research paper on the impact of technology in education, exploring both the positive and negative effects.
2	Create a presentation on the history and significance of a famous literary work, analyzing its themes and symbolism.
3	Design a poster promoting the benefits of reading and literacy, using eye-catching visuals and persuasive language.
4	Compose a persuasive letter to the school board advocating for the inclusion of a new extracurricular activity or club.
5	Write a short play that addresses the issue of bullying in schools, highlighting the importance of empathy and kindness.
6	Create a detailed lesson plan for teaching a complex mathematical concept, incorporating hands-on activities and visual aids.
7	Write a personal narrative about a challenging experience in school and how it shaped your character and resilience.
8	Design an infographic illustrating the steps students can take to improve their study habits and achieve academic success.
9	Compose a series of blog posts discussing the benefits of learning a second language, including practical tips for language acquisition.
10	Write a persuasive essay arguing for the inclusion of more diverse literature in the school curriculum, promoting cultural understanding and empathy.
If you are satisfied with these instructions, press y. Otherwise, press n: y
Finished Generating Instructions
```

### Generate Instances

```bash
seed_examples = [
{'input' : "Hello, how are you?",
'output' : "¡Hola, ¿cómo estás?"},
{'input' : "Can you please pass me the salt?",
'output' : "¿Puedes pasarme la sal, por favor?"},
{'input' : "I love going to the beach during summer.",
'output' : "Me encanta ir a la playa durante el verano."},
{'input' : "Where is the nearest post office?",
'output' : "¿Dónde está la oficina de correos más cercana?"},
{'input' : "What time does the movie start?",
'output' : "¿A qué hora comienza la película?"},
{'input' : "I need to make a reservation for two people.",
'output' : "Necesito hacer una reserva para dos personas."},
{'input' : "Could you recommend a good restaurant?",
'output' : "¿Podrías recomendarme un buen restaurante?"},
{'input' : "How do I get to the train station?",
'output' : "¿Cómo llego a la estación de tren?"},
{'input' : "What's your favorite book?",
'output' : "¿Cuál es tu libro favorito?"},
{'input' : "I want to learn Spanish.",
'output' : "Quiero aprender español."}
]

new_instances = instances.generate_instances(seed_examples,20,'Translate from English to Spanish')
```

### Clean LLM Datasets

```bash
seed_examples = [
{'input' : "Hello, how are you?",
'output' : "¡Hola, ¿cómo estás?"},
{'input' : "Can you please pass me the salt?",
'output' : "¿Puedes pasarme la sal, por favor?"},
{'input' : "I love going to the beach during summer.",
'output' : "Me encanta ir a la playa durante el verano."},
{'input' : "Where is the nearest post office?",
'output' : "¿Dónde está la oficina de correos más cercana?"},
{'input' : "What time does the movie start?",
'output' : "¿A qué hora comienza la película?"},
{'input' : "I need to make a reservation for two people.",
'output' : "Necesito hacer una reserva para dos personas."},
{'input' : "Could you recommend a good restaurant?",
'output' : "¿Podrías recomendarme un buen restaurante?"},
{'input' : "How do I get to the train station?",
'output' : "¿Cómo llego a la estación de tren?"},
{'input' : "What's your favorite book?",
'output' : "¿Cuál es tu libro favorito?"},
{'input' : "I want to learn Spanish.",
'output' : "Quiero aprender español."}
]

my_data = Dataset(generated_data)
clean_ten_instances = my_data.n_most_unique_elements(10)

```
## Features

1. Generate high-quality instructions or instances for LLMs for all use cases using GPT
2. Give high-quality natural language feedback in the console to adapt your generated data to your own needs
3. Clean your dataset to reduce replicates and thus bias
## 🙌 Contributing

Discus is a rapidly developing project. We welcome contributions in all forms - bug reports, pull requests and ideas for improving the library.

1. Open an [issue](https://github.com/discus-labs/discus/issues) on Github for bugs and request features.
2. Grab an open issue, and submit a pull request!
