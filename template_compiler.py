from config import Config
from jinja2 import Environment
from typing import Any

class TemplateCompiler:
    def __init__(self, config: Config) -> None:
        config.output_dir.mkdir(parents=True, exist_ok=True)
        self.config: Config = config

    def convert(self, env: Environment,
                parsed_context: Any) -> str:
        template = env.get_template(self.config.template_name)
        output = template.render(**parsed_context)
        return output

