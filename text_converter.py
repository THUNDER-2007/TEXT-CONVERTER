import streamlit as st
import requests

st.set_page_config(page_title="Handwriting OCR", layout="wide")
st.title("📄 Handwriting OCR (Tamil + English)")
st.write("Upload a PDF or image → Extract text with page-wise copy option!")

# OCR.Space API key
API_KEY = "K87727956988957"

def ocr_space_file(file_bytes, language="eng", filetype=None):
    """Send file to OCR.Space API and get extracted text."""
    payload = {
        "apikey": API_KEY,
        "language": language,
        "isOverlayRequired": False,
    }
    if filetype:
        payload["filetype"] = filetype

    files = {"file": ("file", file_bytes)}

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

    # OCR.Space returns ParsedResults as a list of pages
    texts = []
    for parsed in result.get("ParsedResults", []):
        texts.append(parsed.get("ParsedText", ""))

    return texts, None

# File uploader
uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.info("Processing file...")

    file_bytes = uploaded_file.read()
    filetype = "PDF" if uploaded_file.type == "application/pdf" else None

    texts, error = ocr_space_file(file_bytes, language="eng", filetype=filetype)

    if texts:
        for idx, t in enumerate(texts):
            st.subheader(f"Page {idx+1}")
            st.text_area(f"Page {idx+1} Text", t, height=200, key=f"page_{idx}")
            st.markdown(f"""
                <button onclick="navigator.clipboard.writeText({t})">
                📋 Copy Page {idx+1}</button>
            """, unsafe_allow_html=True)

    if error:
        st.error(f"Error occurred:\n{error}")
