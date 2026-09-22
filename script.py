import yaml
import os
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Any
from dotenv import load_dotenv
from weasyprint import HTML

# TODO: Use pydantic and fetch some info from .env files


class ResumeBuilder:
    def __init__(self) -> None:
        load_dotenv(override=True)
        self.root_path: str = str(Path(
            __file__).resolve().parent)
        self.templates_path: str = self.root_path + "/templates"
        self.info_path: str = self.root_path + "/personal_info"
        self.filename: str = os.getenv("yaml_name") or "resume.yaml"
        self.parsed_context = None
        self.output_html_name: str = os.getenv(
            "html_name") or "resume.html"
        self.output_pdf_name: str = os.getenv("pdf_name") or "resume.pdf"

    def load_context_vars(self) -> Any:
        try:
            with open(self.filename, 'r') as f:
                self.parsed_context = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as error:
            print(f"{error}")
            sys.exit(1)

    def generate_pdf(self) -> Any:
        doc = HTML(filename=self.output_html_name)
        doc.write_pdf(target=self.output_pdf_name)

    def setup_jinja(self, template_name: str) -> None:

        env = Environment(loader=FileSystemLoader(self.templates_path),
                          autoescape=select_autoescape())
        template = env.get_template(template_name)
        html = template.render(**self.parsed_context)
        with open(self.output_html_name, "w", encoding="utf-8") as f:
            f.write(html)


if __name__ == "__main__":
    resumeBuilder = ResumeBuilder()
    resumeBuilder.load_context_vars()
    resumeBuilder.setup_jinja("software_engineer.html.j2")
    resumeBuilder.generate_pdf()
