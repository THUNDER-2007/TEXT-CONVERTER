import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="Handwriting OCR", layout="wide")
st.title("📄 Handwriting OCR (Tamil + English)")
st.write("Upload a PDF or image → Extract text with page-wise copy option!")

# Your OCR.Space API key
API_KEY = "K87727956988957"

def ocr_space_file(file, language="eng", filetype=None):
    """Send file to OCR.Space API and get extracted text."""
    payload = {
        "apikey": API_KEY,
        "language": language,
        "isOverlayRequired": False
    }
    if filetype:
        payload["filetype"] = filetype

    files = {"file": (file.name, file.getvalue())}

    try:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files=files,
            data=payload
        )
        result = response.json()
    except Exception as e:
        return None, str(e)

    if result.get("IsErroredOnProcessing"):
        return None, result.get("ErrorMessage")
    
    texts = []
    for parsed in result.get("ParsedResults", []):
        texts.append(parsed.get("ParsedText", ""))
    
    return texts, None

# Streamlit file uploader
uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.info("Processing file...")

    filetype = "PDF" if uploaded_file.type == "application/pdf" else None

    # Handle PDF page-wise
    if filetype == "PDF":
        pdf = PdfReader(uploaded_file)
        for i, page in enumerate(pdf.pages):
            st.subheader(f"Page {i+1}")
            # Extract text directly from PDF page
            page_text = page.extract_text() or "No text detected on this page"
            st.text_area(f"Page {i+1} Text", page_text, height=200, key=f"page_{i}")
            # Copy button for each page
            st.markdown(f"""
                <button onclick="navigator.clipboard.writeText({page_text})">
                📋 Copy Page {i+1}</button>
            """, unsafe_allow_html=True)
    else:
        # For images
        texts, error = ocr_space_file(uploaded_file, language="eng")
        if texts:
            for idx, t in enumerate(texts):
                st.subheader(f"Page {idx+1}")
                st.text_area(f"Page {idx+1} Text", t, height=200, key=f"img_{idx}")
                st.markdown(f"""
                    <button onclick="navigator.clipboard.writeText({t})">
                    📋 Copy Page {idx+1}</button>
                """, unsafe_allow_html=True)
        if error:
            st.error(f"Error occurred:\n{error}")
