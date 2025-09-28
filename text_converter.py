import streamlit as st
import requests

st.set_page_config(page_title="Text Converter OCR", layout="wide")
st.title("📄 Handwriting OCR (Tamil + English)")
st.write("Upload a PDF, photo, or screenshot → Extract Tamil & English text in one click!")

# Your OCR API key
API_KEY = "K87727956988957"

def ocr_space_file(file):
    """Send file to OCR.Space API and get extracted text."""
    payload = {
        "apikey": API_KEY,
        "language": "tam+eng",
        "isOverlayRequired": False
    }
    files = {"file": file.getvalue()}
    response = requests.post("https://api.ocr.space/parse/image",
                             files=files,
                             data=payload)
    result = response.json()
    if result.get("IsErroredOnProcessing"):
        return None, result.get("ErrorMessage")
    text = ""
    for parsed in result.get("ParsedResults", []):
        text += parsed.get("ParsedText", "")
    return text, None

uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.info("Processing file...")
    extracted_text, error = ocr_space_file(uploaded_file)
    if error:
        st.error(f"Error: {error}")
    elif extracted_text:
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
