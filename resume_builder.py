from weasyprint import HTML
from abc import ABC, abstractmethod

from config import Config

class ResumeBuilder(ABC):

    def __init__(self, config) -> None:
        self.config: Config = config

    @abstractmethod
    def build_resume(self, template: str) -> None:
        pass


class PDFResumeBuilder(ResumeBuilder):

    def __init__(self, config) -> None:
        super().__init__(config)

    def build_resume(self, template: str) -> None:
        # I need to find a way to generlize this one
        doc = HTML(file_obj=template)
        doc.write_pdf(target=self.config.final_file)
