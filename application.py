#!/usr/bin/env python3

from typing import Any
from config import Config, get_config
from template_compiler import TemplateCompiler
from template_loader import TemplateLoader, YamlLoader
from resume_builder import PDFResumeBuilder



def main() -> None:
    config: Config = get_config()
    loader: TemplateLoader = YamlLoader(config)
    context: Any = loader.load_context()
    compiler: TemplateCompiler = TemplateCompiler(config)
    template: str = compiler.convert(loader.env, context)
    pdfbuilder: PDFResumeBuilder = PDFResumeBuilder(config)
    pdfbuilder.build_resume(template)



if __name__ == "__main__":
    main()
