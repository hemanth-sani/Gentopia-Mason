from pathlib import Path
from typing import AnyStr, Optional, Type
from PyPDF2 import PdfReader
from gentopia.tools.basetool import *
from pydantic import Field
from io import BytesIO
import requests
import fitz  # PyMuPDF


class ReadPDFFromURLArgs(BaseModel):
    url: str = Field(..., description="The URL of the PDF file to read")
    file_path: str = Field(None, description="The path of the PDF file to read on the disk")

class ReadPDFTool(BaseTool):
    """Read PDF file from disk or URL"""

    name = "ReadPDF"
    description = "Read the contents of a PDF file from the hard disk or a URL."
    args_schema: Optional[Type[BaseModel]] = ReadPDFFromURLArgs

    def _run(self, file_path: Optional[str] = None, url: Optional[str] = None) -> AnyStr:
        try:
            if url:
                url.replace("abs","pdf")
                url+=".pdf"
                response = requests.get(url)
                response.raise_for_status()
                file_stream = BytesIO(response.content)
                doc = fitz.open("pdf", file_stream)
            elif file_path:
                doc = fitz.open(file_path)
            else:
                return "Error: No file path or URL provided."

            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text

        except requests.RequestException as e:
            return f"Request error: {e}"
        except Exception as e:
            return f"Error: {e}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    pdf_url = "https://example.com/somefile.pdf"  # Replace with your actual PDF URL
    ans = ReadPDFTool()._run(url=pdf_url)
    # You can also use file_path argument to read from disk
    # ans = ReadPDFTool()._run(file_path="example.pdf")
    print(ans)

