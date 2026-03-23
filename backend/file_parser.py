import PyPDF2
import docx
from io import BytesIO

async def extract_text(file):
    content = await file.read()

    if file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(BytesIO(content))
        return " ".join([page.extract_text() or "" for page in reader.pages])

    elif file.filename.endswith(".docx"):
        doc = docx.Document(BytesIO(content))
        return "\n".join([p.text for p in doc.paragraphs])

    elif file.filename.endswith(".txt"):
        return content.decode("utf-8")

    return ""