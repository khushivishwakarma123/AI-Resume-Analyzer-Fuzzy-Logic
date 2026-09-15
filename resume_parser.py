from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file):
    """
    Extract text from a PDF resume.
    """
    text = ""

    try:
        reader = PdfReader(file)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")

    return text.strip()


def extract_text_from_docx(file):
    """
    Extract text from a DOCX resume.
    """
    text = ""

    try:
        document = Document(file)

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"

    except Exception as e:
        raise Exception(f"Error reading DOCX: {e}")

    return text.strip()


def extract_text_from_txt(file):
    """
    Extract text from a TXT resume.
    """
    try:
        return file.read().decode("utf-8").strip()

    except Exception as e:
        raise Exception(f"Error reading TXT file: {e}")


def extract_resume_text(file):
    """
    Detect the uploaded file type and extract its text.
    """

    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif file_name.endswith(".docx"):
        return extract_text_from_docx(file)

    elif file_name.endswith(".txt"):
        return extract_text_from_txt(file)

    else:
        raise ValueError(
            "Unsupported file format. Please upload PDF, DOCX or TXT."
        )