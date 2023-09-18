from transformers import AutoTokenizer
import transformers
import torch

class HuggingFace:
    def __init__(self, config: DiscusConfig) -> None:
        self.config = config
        self.model_name = config.model_name or "meta-llama/Llama-2-7b-chat-hf"

    def _hf_generate(self, prompt, context = None):

        message = prompt[0] + " " + prompt[1]
        tokenizer = AutoTokenizer.from_pretrained(model)
        pipeline = transformers.pipeline(
            "text-generation",
            model = self.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        sequences = pipeline(
            message,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
            max_length=200,
        )

        for seq in sequences:
            print(f"Result: {seq['generated_text']}")

        return sequences

    def _get_data_from_model_response(self, response):
        pass 

