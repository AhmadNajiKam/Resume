from config import Config
from jinja2 import Environment, TemplateError
from typing import Any

class TemplateCompiler:
    def __init__(self, config: Config) -> None:
        config.output_dir.mkdir(parents=True, exist_ok=True)
        self.config: Config = config

    def convert(self, env: Environment,
                parsed_context: Any) -> str:
        try:
            template = env.get_template(self.config.template_name)
            output = template.render(**parsed_context)
        except TemplateError as e:
            print(f"Template error has happened: {e.message}")
        else:
            return output
        return ""
