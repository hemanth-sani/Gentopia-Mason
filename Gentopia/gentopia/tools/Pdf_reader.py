from pathlib import Path
from typing import AnyStr, Optional, Type
from PyPDF2 import PdfReader
from gentopia.tools.basetool import *
from pydantic import Field
from io import BytesIO
import requests


class ReadPDFFromURLArgs(BaseModel):
    url: str = Field(..., description="Reads the URL PDF")

class ReadPDFTool(BaseTool):
    """Reads the URL PDF"""

    name = "ReadPDF"
    description = "Reads the URL PDF"
    args_schema: Optional[Type[BaseModel]] = ReadPDFFromURLArgs

    def _run(self, file_path: str = None, url: str = None) -> AnyStr:
        try:
            if url:
                response = requests.get(url)
                response.raise_for_status()
                file = BytesIO(response.content)
            else:
                pdf_path = Path(file_path)
                file = open(pdf_path, 'rb')
            
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text() or ""
                if len(text) + len(page_text) > 9000:
                    text += page_text[:9000 - len(text)]
                    break
                else:
                    text += page_text
            
            file.close()
            return text

        except requests.RequestException as e:
            return f"Request error: {e}"
        except Exception as e:
            return f"Error: {e}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    pdf_url = "https://file.pdf"  
    pdf = ReadPDFTool()._run(url=pdf_url)
    
    print(pdf)


