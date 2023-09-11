import os
from discus import Generator, Dataset

discus = Generator(config = "/Users/rohankshah/Desktop/discus/examples/eng2spanish/eng2spanish.json")
generated_data = discus.run()

gen = Dataset(generated_data)
result = gen.n_most_unique_elements(1000)