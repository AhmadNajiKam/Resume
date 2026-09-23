import yaml
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Any
from dotenv import load_dotenv
from weasyprint import HTML


class ResumeBuilder:
    def __init__(self) -> None:
        load_dotenv(override=True)
        self.root_path: Path = Path(
            __file__).resolve().parent
        self.templates_path: Path = self.root_path / "templates"
        self.output_path: Path = self.root_path / "output"
        self.filename: Path = self.root_path / \
            (os.getenv("yaml_name") or "resume.yaml")
        self.output_html_name: Path = self.output_path / (os.getenv(
            "html_name") or "resume.html")
        self.output_pdf_name: Path = self.output_path / \
            (os.getenv("pdf_name") or "resume.pdf")
        self.env: Environment = Environment(
            loader=FileSystemLoader(self.templates_path),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def load_context(self) -> dict[str, Any] | None:
        with self.filename.open("r", encoding="utf-8") as f:
            parsed_context: dict[str, Any] | None = yaml.safe_load(f)
            return parsed_context

    def generate_pdf(self) -> None:
        doc = HTML(filename=self.output_html_name)
        doc.write_pdf(target=self.output_pdf_name)

    def generate_html(self, template_name: str,
                      parsed_context: dict[str, Any]) -> None:
        self.output_path.mkdir(parents=True, exist_ok=True)
        template = self.env.get_template(template_name)
        html = template.render(**parsed_context)
        with open(self.output_html_name, "w", encoding="utf-8") as f:
            f.write(html)


if __name__ == "__main__":
    resume_builder = ResumeBuilder()
    context: dict[str, Any] | None = resume_builder.load_context()
    resume_builder.generate_html("software_engineer.html.j2", context)
    resume_builder.generate_pdf()
