from agent_network.base import BaseAgent
from agent_network.exceptions import ReportError
import requests

class docx_read_agent(BaseAgent):
    def __init__(self, graph, config, logger):
        super().__init__(graph, config, logger)

    def forward(self, messages, **kwargs):
        file_url = kwargs.get("file_url")
        if not file_url:
            raise ReportError("file_url is not provided")
        
        import io
        from docx import Document
        response = requests.get(file_url)
        docx_file = io.BytesIO(response.content)
        docx = Document(docx_file)
        docx_read_result = "\n".join(para.text for para in docx.paragraphs)
        self.log("assistant", docx_read_result)

        result = {
            "docx_read_result": docx_read_result
        }
        return result