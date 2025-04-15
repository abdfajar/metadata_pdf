import fitz  # PyMuPDF
import docx
import streamlit as st
from openai import OpenAI

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def get_metadata_analysis(text, kunci):
    client = OpenAI(api_key=kunci)
    prompt = f"Ambil dan tampilkan metadata dari dokumen berikut:\n\n{text[:2000]}"

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Anda adalah asisten AI yang menganalisis metadata dokumen."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def analisis_metadata_dokumen(file, kunci):
    filename = file.name.lower()

    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file)
    else:
        return "Format file tidak didukung. Hanya PDF dan DOCX yang diterima."

    if not text.strip():
        return "Tidak ada teks yang bisa diekstrak dari dokumen."

    return get_metadata_analysis(text, kunci)

# Streamlit UI
st.set_page_config(page_title="Analisis Metadata Dokumen", layout="centered")
st.title("📄 Analisis Metadata Dokumen dengan OpenAI")

kunci = st.text_input("🔑 Masukkan API Key OpenAI Anda", type="password")
file = st.file_uploader("📁 Upload Dokumen PDF atau DOCX", type=["pdf", "docx"])

if st.button("🚀 Proses Metadata"):
    if not kunci:
        st.error("API Key tidak boleh kosong.")
    elif not file:
        st.error("Silakan upload file terlebih dahulu.")
    else:
        with st.spinner("🔍 Menganalisis metadata dokumen..."):
            hasil = analisis_metadata_dokumen(file, kunci)
            st.text_area("📌 Hasil Metadata", hasil, height=300)
