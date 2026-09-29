from pathlib import Path
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=False
    )

    # ---- These are 100% controlled by .env, any extension works ----
    # .env example:
    # SOURCE_FILE=resume.json
    # INTERMEDIATE_FILE=resume.html
    # FINAL_FILE=resume.pdf
    source_file_name: str = "resume.yaml"
    intermediate_file_name: str = "resume.html"
    final_file_name: str = "resume.pdf"
    source_format: str = "yaml"
    intermediate_format: str = "html"
    final_format: str = "pdf"
    template_name: str = ""

    # ---- Directories ----
    root_path: Path = Field(default_factory=lambda: Path(__file__).resolve().parent)
    template_dir_name: str = "templates"
    output_dir_name: str = "output"

    @computed_field
    @property
    def templates_path(self) -> Path:
        return self.root_path / self.template_dir_name

    @computed_field
    @property
    def output_dir(self) -> Path:
        return self.root_path / self.output_dir_name

    # ---- Full resolved paths ----
    @computed_field
    @property
    def source_file(self) -> Path:
        return self.root_path / self.source_file_name

    @computed_field
    @property
    def intermediate_file(self) -> Path:
        return self.output_dir / self.intermediate_file_name

    @computed_field
    @property
    def final_file(self) -> Path:
        return self.output_dir / self.final_file_name

@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config()
