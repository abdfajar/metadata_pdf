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

def chunk_text(text, max_chars=5000):
    paragraphs = text.split("\n")
    chunks, current_chunk = [], ""

    for para in paragraphs:
        if len(current_chunk) + len(para) < max_chars:
            current_chunk += para + "\n"
        else:
            chunks.append(current_chunk)
            current_chunk = para + "\n"
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def get_outline_analysis(text, kunci):
    client = OpenAI(api_key=kunci)
    prompt = (
        "Diberikan isi dokumen berikut, ekstrak struktur atau outline dokumen secara hierarkis. "
        "Tampilkan daftar judul utama, bab, subbab, dan sub-subbab bila ada. "
        "Gunakan format markdown dan batasi output maksimal 1000 kata.\n\n"
        f"{text}"
    )

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Anda adalah asisten AI yang membantu mengekstrak struktur dokumen."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def analisis_outline_dokumen(file, kunci):
    filename = file.name.lower()

    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file)
    else:
        return "❌ Format file tidak didukung. Hanya PDF dan DOCX yang diterima."

    if not text.strip():
        return "❌ Tidak ada teks yang bisa diekstrak dari dokumen."

    chunks = chunk_text(text)
    outline_all = ""
    for i, chunk in enumerate(chunks):
        outline = get_outline_analysis(chunk, kunci)
        outline_all += f"\n### Bagian {i+1}\n" + outline + "\n"

    return outline_all

# Streamlit UI
st.set_page_config(page_title="Analisis Outline Dokumen", layout="centered")
st.title("📑 Analisis Outline Dokumen dengan OpenAI")

kunci = st.text_input("🔑 Masukkan API Key OpenAI Anda", type="password")
file = st.file_uploader("📁 Upload Dokumen PDF atau DOCX", type=["pdf", "docx"])

if st.button("🚀 Proses Outline"):
    if not kunci:
        st.error("API Key tidak boleh kosong.")
    elif not file:
        st.error("Silakan upload file terlebih dahulu.")
    else:
        with st.spinner("🔍 Mengekstrak struktur dokumen..."):
            hasil = analisis_outline_dokumen(file, kunci)
            st.markdown(hasil, unsafe_allow_html=True)
