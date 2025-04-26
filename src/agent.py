import argparse
import os
from src.utils.repo_scanner import scan_repo
from src.chains.file_summary_chain import create_file_summary_chain
from src.chains.tech_extraction_chain import create_tech_extraction_chain
from src.chains.readme_generation_chain import create_readme_generation_chain

"""
Orchestrates scanning a repo and generating README.md via LangChain chains.
"""

def main():
    parser = argparse.ArgumentParser(description="Generate README.md from codebase")
    parser.add_argument("--repo_path", type=str, required=True)
    parser.add_argument("--include_exts", nargs="+", default=[".py", ".js", ".md"])
    parser.add_argument("--exclude_dirs", nargs="+", default=[".git", "__pycache__", "venv"])
    args = parser.parse_args()

    files = scan_repo(
        repo_path=args.repo_path,
        include_exts=args.include_exts,
        exclude_dirs=args.exclude_dirs
    )

    file_chain = create_file_summary_chain()
    tech_chain = create_tech_extraction_chain()
    readme_chain = create_readme_generation_chain()

    summaries = []
    technologies = []
    for path, content in files:
        summary = file_chain.invoke({"filename": path, "file_content": content})
        summaries.append(f"- **{path}**: {summary}")
        tech = tech_chain.invoke({"file_content": content})
        technologies.append(f"- **{path}**:\n{tech}")

    project_name = os.path.basename(os.path.normpath(args.repo_path))
    readme = readme_chain.invoke({
        "project_name": project_name,
        "summaries": "\n".join(summaries),
        "technologies": "\n".join(technologies)
    })

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print("README.md generated successfully.")

if __name__ == "__main__":
    main()