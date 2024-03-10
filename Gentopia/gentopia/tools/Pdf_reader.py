from PyPDF2 import PdfReader
from gentopia.tools.basetool import BaseTool, BaseModel
from typing import Optional, Type
from pydantic import Field

# Define arguments for the PDF tool
class ReadPDFArgs(BaseModel):
    file_path: str = Field(..., description="Path to the PDF file")

# PDF Reading Tool
class ReadPDFTool(BaseTool):
    name = "read_pdf"
    description = "Read a PDF file and return its text."
    args_schema: Optional[Type[BaseModel]] = ReadPDFArgs

    def _run(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    async def _arun(self, *args: Any, **kwargs: Any)) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = ReadPDFTool()._run("abc.pdf")
    print(ans)
