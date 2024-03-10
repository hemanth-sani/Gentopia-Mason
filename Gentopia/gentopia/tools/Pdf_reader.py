from pathlib import Path
from typing import AnyStr, Optional, Type
from PyPDF2 import PdfReader
from gentopia.tools.basetool import BaseTool, BaseModel
from pydantic import Field

class ReadPDFArgs(BaseModel):
    file_path: str = Field(..., description="The path of the PDF file to read")

class ReadPDFTool(BaseTool):
    """Read PDF file from disk"""

    name = "ReadPDF"
    description = "Read the contents of a PDF file from the hard disk."
    args_schema: Optional[Type[BaseModel]] = ReadPDFArgs

    def _run(self, file_path) -> AnyStr:
        pdf_path = Path(file_path)
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            return "Error: " + str(e)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    pdf_path = "example.pdf"  # Replace with your PDF file path
    ans = ReadPDFTool()._run(pdf_path)
    print(ans)
