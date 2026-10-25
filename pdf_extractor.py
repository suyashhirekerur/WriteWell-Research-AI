import pdfplumber
import docx


def extract_text_from_pdf(file):
    """Extract text from a PDF file object."""
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"
    except Exception as e:
        text = f"Error extracting PDF: {str(e)}"
    return text


def extract_text_from_docx(file):
    """Extract text from a DOCX file object."""
    try:
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception as e:
        return f"Error extracting DOCX: {str(e)}"


def extract_text_from_txt(file):
    """Extract text from a plain text file."""
    try:
        return file.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"Error reading TXT: {str(e)}"


def extract_text(uploaded_file):
    """Route extraction based on file type."""
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif name.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)
    return ""
