from jinja2 import Environment, FileSystemLoader, TemplateError, select_autoescape
from config import Config
from typing import Any
from abc import ABC, abstractmethod
import yaml



class TemplateLoader(ABC):
    def __init__(self, config: Config) -> None:
                self.config: Config = config
                self.env: Environment = Environment(
            loader=FileSystemLoader(self.config.templates_path),
            autoescape=select_autoescape(["html", "xml"])
        )

    @abstractmethod
    def load_context(self) -> Any:
        pass

class YamlLoader(TemplateLoader):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def load_context(self) -> Any:
        try:
            with self.config.source_file.open("r", encoding="utf-8") as f:
                parsed_context: Any = yaml.safe_load(f)
                return parsed_context
        except IOError as e:
             print(f"I/O error({e.errno}): {e.strerror}")
        except Exception as e:
            print(f"error has happened: {e}")
