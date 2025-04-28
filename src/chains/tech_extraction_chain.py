from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.runnables.base import RunnableSequence
from langchain_huggingface import HuggingFacePipeline

"""
Creates a runnable that extracts language/framework/purpose info from code.
"""
def create_tech_extraction_chain(llm_pipeline: HuggingFacePipeline):
    examples = [
        {
            "file_content": "```python\n# user_service.py\nfrom fastapi import APIRouter\n# ...\n```",
            "technologies": (
                "- Language: Python\n"
                "- Frameworks: FastAPI, SQLAlchemy\n"
                "- Purpose: Defines REST endpoints for user CRUD operations"
            )
        },
        {
            "file_content": "```typescript\n// ui_component.tsx\nimport React from 'react';\n// ...\n```",
            "technologies": (
                "- Language: TypeScript\n"
                "- Frameworks: React, Redux\n"
                "- Purpose: UI components for rendering and updating user profiles"
            )
        }
    ]

    example_prompt = PromptTemplate(
        input_variables=["file_content", "technologies"],
        template="```{file_content}```\nTechnologies:\n{technologies}"
    )

    fewshot = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="For the following code, list the primary language, frameworks/libraries, and its high-level purpose.\n\n",
        suffix="\nTechnologies:",
        input_variables=["file_content"],
        example_separator="\n\n"
    )

    return RunnableSequence(fewshot, llm_pipeline)