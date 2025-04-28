from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.base import RunnableSequence
from langchain_huggingface import HuggingFacePipeline

"""
Creates a chain that stitches summaries and tech info into a final README.
"""
def create_readme_generation_chain(llm_pipeline: HuggingFacePipeline):
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

    return RunnableSequence(template, llm_pipeline)