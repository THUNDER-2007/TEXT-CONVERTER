import streamlit as st
import requests

st.set_page_config(page_title="Handwriting OCR", layout="wide")
st.title("📄 Handwriting OCR (Tamil + English)")
st.write("Upload an image → Extract text!")

# OCR.Space API key
API_KEY = "K87727956988957"

def ocr_space_file(file_bytes, language="eng", filetype="PNG"):
    """Send file to OCR.Space API and get extracted text."""
    payload = {
        "apikey": API_KEY,
        "language": language,
        "isOverlayRequired": False,
    }

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

    texts = []
    for parsed in result.get("ParsedResults", []):
        texts.append(parsed.get("ParsedText", ""))

    return texts, None

# File uploader (images only)
uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.info("Processing image...")
    file_bytes = uploaded_file.read()

    texts, error = ocr_space_file(file_bytes, language="eng", filetype="PNG")

    if texts:
        for idx, t in enumerate(texts):
            st.subheader(f"Page {idx+1}")
            st.text_area(f"Page {idx+1} Text", t, height=200, key=f"page_{idx}")

    if error:
        st.error(f"Error occurred:\n{error}")
