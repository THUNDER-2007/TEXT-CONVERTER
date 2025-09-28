import streamlit as st
import requests
from pdf2image import convert_from_bytes
import io

st.set_page_config(page_title="Handwriting OCR", layout="wide")
st.title("📄 Handwriting OCR (Tamil + English)")
st.write("Upload a PDF or image → Extract text page-wise!")

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

    texts = []
    for parsed in result.get("ParsedResults", []):
        texts.append(parsed.get("ParsedText", ""))

    return texts, None

# File uploader
uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.info("Processing file...")
    file_bytes = uploaded_file.read()

    if uploaded_file.type == "application/pdf":
        # Convert PDF to images
        images = convert_from_bytes(file_bytes)
        all_texts = []
        for idx, img in enumerate(images):
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            img_bytes = buf.getvalue()
            texts, error = ocr_space_file(img_bytes, language="eng", filetype="PNG")
            if error:
                st.error(f"Page {idx+1} error: {error}")
            else:
                all_texts.extend(texts)
    else:
        filetype = "PNG" if uploaded_file.type.startswith("image/") else None
        all_texts, error = ocr_space_file(file_bytes, language="eng", filetype=filetype)
        if error:
            st.error(f"Error: {error}")

    # Display extracted text page-wise
    if all_texts:
        for idx, t in enumerate(all_texts):
            st.subheader(f"Page {idx+1}")
            st.text_area(f"Page {idx+1} Text", t, height=200, key=f"page_{idx}")
