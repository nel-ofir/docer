from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.base import RunnableSequence

"""
Creates a runnable that summarizes a file's content.
"""
def create_file_summary_chain():
    hf_pipe = pipeline(
        "text-generation",              # <-- causal LM needs text-generation
        model="EleutherAI/pythia-2.8b",
        trust_remote_code=True,
        device_map="auto",
        max_new_tokens=256
    )
    
    llm = HuggingFacePipeline(pipeline=hf_pipe)
    prompt = PromptTemplate(
        input_variables=["filename", "file_content"],
        template=(
            "You are a code documentation assistant. "
            "Please provide a concise summary of the file **{filename}**. "
            "Include:\n"
            "- Its purpose in the project\n"
            "- Key functions or classes\n"
            "- Any frameworks or libraries it uses\n\n"
            "```{file_content}```\n"
            "Summary:"
        )
    )
    return RunnableSequence(prompt, llm)