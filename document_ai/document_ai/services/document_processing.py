import pdfplumber
import docx
from fastapi import UploadFile
from PIL import Image
import pytesseract
from io import BytesIO

async def process_document(file: UploadFile) -> str:
    if file.content_type == "application/pdf":
        return await process_pdf(file)
    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return await process_docx(file)
    elif file.content_type.startswith("image/"):
        return await process_image(file)
    else:
        raise ValueError("Unsupported file type")

async def process_pdf(file: UploadFile) -> str:
    # Read the file content into bytes
    pdf_content = await file.read()
    with pdfplumber.open(BytesIO(pdf_content)) as pdf:
        text = ''.join(page.extract_text() for page in pdf.pages)
    return text

async def process_docx(file: UploadFile) -> str:
    # Read the file content into bytes
    docx_content = await file.read()
    doc = docx.Document(BytesIO(docx_content))
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

async def process_image(file: UploadFile) -> str:
    # Read the file content into bytes
    image_content = await file.read()
    image = Image.open(BytesIO(image_content))
    text = pytesseract.image_to_string(image)
    return text
