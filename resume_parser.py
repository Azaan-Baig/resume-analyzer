from pypdf import PdfReader
from docx import Document


def extract_pdf_text(file):
    text = ""
    reader = PdfReader(file)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_docx_text(file):
    document = Document(file)
    return "\n".join(
        paragraph.text for paragraph in document.paragraphs
        if paragraph.text.strip()
    )


def extract_resume_text(file):
    filename = file.name.lower()

    if filename.endswith(".pdf"):
        return extract_pdf_text(file)

    if filename.endswith(".docx"):
        return extract_docx_text(file)

    raise ValueError("Only PDF and DOCX files are supported.")
