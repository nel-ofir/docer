from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.base import RunnableSequence
from langchain_huggingface import HuggingFacePipeline

"""
Creates a runnable that summarizes a file's content.
"""
def create_file_summary_chain(llm_pipeline: HuggingFacePipeline):
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
    return RunnableSequence(prompt, llm_pipeline)