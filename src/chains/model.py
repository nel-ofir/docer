from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from langchain_huggingface import HuggingFacePipeline


def get_huggingface_pipeline(model_id: str) -> HuggingFacePipeline:
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        trust_remote_code=False,
        torch_dtype="float16"
    )
    hf_pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256
    )

    llm = HuggingFacePipeline(pipeline=hf_pipe)
    
    return llm