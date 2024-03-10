from pathlib import Path
from typing import AnyStr, Optional, Type
from PyPDF2 import PdfReader
from gentopia.tools.basetool import *
from pydantic import Field
from io import BytesIO
import requests
from bs4 import BeautifulSoup


class FetchAndReadPDFArgs(BaseModel):
    url: str = Field(..., description="The URL to fetch the PDF from")

class FetchAndReadPDFTool(BaseTool):
    """Fetch and read PDF file from a URL"""

    name = "FetchAndReadPDF"
    description = "Fetch a PDF from a URL and read its contents."
    args_schema: Optional[Type[BaseModel]] = FetchAndReadPDFArgs

    def _run(self, url) -> AnyStr:
        try:
            # Find PDF URL
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            pdf_url = None
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and '/pdf/*' in href:
                    pdf_url = href
                    break

            if pdf_url is None:
                return "PDF URL not found."

            # Download PDF
            response = requests.get(pdf_url)
            if response.status_code != 200:
                return "Failed to download PDF."

            pdf_stream = BytesIO(response.content)

            # Read PDF
            reader = PdfReader(pdf_stream)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

            return text

        except Exception as e:
            return "Error: " + str(e)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    url = "http://example.com"  # Replace with the actual URL
    ans = FetchAndReadPDFTool()._run(url)
    print(ans)


