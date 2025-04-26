from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.base import RunnableSequence

"""
Creates a chain that stitches summaries and tech info into a final README.
"""
def create_readme_generation_chain():
    hf_pipe = pipeline(
        "text-generation",              # <-- causal LM needs text-generation
        model="EleutherAI/pythia-2.8b",
        trust_remote_code=True,
        device_map="auto",
        max_new_tokens=256
    )
    
    llm = HuggingFacePipeline(pipeline=hf_pipe)

    template = PromptTemplate(
        input_variables=["project_name", "summaries", "technologies"],
        template=(
            ''''# {project_name}

            "
            "## Overview
            "
            "{summaries}

            "
            "## Technologies Used
            "
            "{technologies}

            "
            "## Architecture & Flow
            "
            "Using the above information, write a concise description of how the components interact and the overall data/control flow of the application.
            '''
        )
    )

    return RunnableSequence(template, llm)