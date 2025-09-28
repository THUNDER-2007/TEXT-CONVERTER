import streamlit as st
import fitz  # PyMuPDF for PDF
import pytesseract
from PIL import Image
import io

st.set_page_config(page_title="Handwriting OCR", layout="wide")

st.title("📄 Handwriting OCR (Tamil + English)")
st.write("Upload a *PDF, Photo, or Screenshot* → Extract *Tamil & English text* in one click!")

def extract_text_from_image(image_file):
    """Extract text from image (Tamil + English)."""
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image, lang="tam+eng")
    return text.strip()

def extract_text_from_pdf(pdf_file):
    """Extract text from each page of a PDF."""
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    all_text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        pix = page.get_pixmap()
        img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))

        text = pytesseract.image_to_string(image, lang="tam+eng")
        all_text += f"\n\n--- Page {page_num + 1} ---\n{text.strip()}"
    return all_text.strip()

uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        st.info("Processing PDF...")
        extracted_text = extract_text_from_pdf(uploaded_file)
    else:
        st.info("Processing Image...")
        extracted_text = extract_text_from_image(uploaded_file)

    if extracted_text:
        st.subheader("✅ Extracted Text:")
        st.text_area("Result", extracted_text, height=400)

        st.download_button(
            label="💾 Download as Text File",
            data=extracted_text,
            file_name="output_text.txt",
            mime="text/plain"
        )
    else:
        st.warning("⚠️ No text detected. Try another file.")
