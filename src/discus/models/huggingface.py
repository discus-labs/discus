from langchain.llms import HuggingFacePipeline
import torch
from transformers import AutoConfig, AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from transformers.models.auto.modeling_auto import MODEL_FOR_CAUSAL_LM_MAPPING, MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING
from discus.json.config import DiscusConfig

class HuggingFace:
    def __init__(self, config: DiscusConfig) -> None:
        self.default_model = "meta-llama/Llama-2-7b-chat-hf"
        self.config = config
        self.model_name = config.model_name or self.default_model
        self.params = {"temperature": 0.0, "quantize": 8}

    def _hf_generate(self, prompt, context = None):        
        self.model_params = self.params
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_name, use_fast=True, add_prefix_space=True
        )


 # credit to refuel-ai/autolabel/src/models/hf_pipeline.py

        bits = self.model_params["quantize"]
        model_config = AutoConfig.from_pretrained(self.model_name)
        if isinstance(model_config, tuple(MODEL_FOR_CAUSAL_LM_MAPPING)):
            AutoModel = AutoModelForCausalLM
        elif isinstance(model_config, tuple(MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING)):
            AutoModel = AutoModelForSeq2SeqLM
        else:
            raise ValueError(
                "model_name is neither a causal LM nor a seq2seq LM. Please check the model_name."
            )
        
        if not torch.cuda.is_available():
            model = AutoModel.from_pretrained(self.model_name)
        elif bits == "16":
            model = AutoModel.from_pretrained(
                self.model_name, torch_dtype=torch.float16, device_map="auto"
            )
        elif bits == "8":
            model = AutoModel.from_pretrained(
                self.model_name, load_in_8bit=True, device_map="auto"
            )
        else:
            model = AutoModel.from_pretrained(self.model_name, device_map="auto")
        
        args = dict(self.model_params) 
        args.pop("quantize", None)
        pipe = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            **args,
        )
        
        self.llm = HuggingFacePipeline(pipeline=pipe, model_kwargs=args)
        
        prompts = [prompt[0], prompt[1]]
        output = self.llm.generate(prompts)

        return output

    def _get_data_from_model_response(self, response):
        pass 

