import streamlit as st
import requests

st.set_page_config(page_title="Handwriting OCR", layout="wide")
st.title("📄 Handwriting OCR (Tamil + English)")
st.write("Upload a PDF, photo, or screenshot → Extract Tamil & English text in one click!")

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
        payload["filetype"] = filetype  # Explicitly set file type for PDFs

    try:
        files = {"file": file.getvalue()}
        response = requests.post("https://api.ocr.space/parse/image",
                                 files=files,
                                 data=payload)
        result = response.json()
    except Exception as e:
        return None, str(e)

    if result.get("IsErroredOnProcessing"):
        return None, result.get("ErrorMessage")
    
    text = ""
    for parsed in result.get("ParsedResults", []):
        text += parsed.get("ParsedText", "")
    
    return text, None

# Streamlit file uploader
uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.info("Processing file...")

    # Set file type for PDF explicitly
    filetype = "PDF" if uploaded_file.type == "application/pdf" else None

    # Run OCR for Tamil first
    tamil_text, error_ta = ocr_space_file(uploaded_file, language="ta", filetype=filetype)
    uploaded_file.seek(0)  # Reset file pointer for second request

    # Run OCR for English
    english_text, error_en = ocr_space_file(uploaded_file, language="eng", filetype=filetype)

    extracted_text = ""
    if tamil_text:
        extracted_text += "✅ Tamil Text:\n" + tamil_text + "\n\n"
    if english_text:
        extracted_text += "✅ English Text:\n" + english_text

    if error_ta or error_en:
        st.error(f"Errors occurred:\nTamil: {error_ta}\nEnglish: {error_en}")

    if extracted_text.strip():
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
