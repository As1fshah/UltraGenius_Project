from PyPDF2 import PdfReader
from docx import Document
def get_pdf_text(file):
    text=""
    pdf_reader= PdfReader(file)
    for page in pdf_reader.pages:
        text+= page.extract_text()
    return  text

def get_docx_text(file):
    document = Document(file)
    text = ""
    for para in document.paragraphs:
        text += para.text + "\n"
    return  text

def get_text(files):
    text = ""
    for file in files:
        if file.name.endswith('.pdf'):
            text += get_pdf_text(file)
        elif file.name.endswith('.docx'):
            text += get_docx_text(file)
        else:
            return "Unsupported file type. Please upload a PDF or DOCX file."
    return text
