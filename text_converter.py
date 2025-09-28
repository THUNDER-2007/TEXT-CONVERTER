import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="Handwriting OCR", layout="wide")
st.title("📄 Handwriting OCR (Tamil + English)")
st.write("Upload a PDF or image → Extract text with page-wise copy option!")

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
        response = requests.post("https://api.ocr.space/parse/image",
                                 files=files,
                                 data=payload)
        result = response.json()
    except Exception as e:
        return None, str(e)

    if result.get("IsErroredOnProcessing"):
        return None, result.get("ErrorMessage")
    
    texts = []
    for parsed in result.get("ParsedResults", []):
        texts.append(parsed.get("ParsedText", ""))
    
    return texts, None

uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.info("Processing
