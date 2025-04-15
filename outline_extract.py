import fitz  # PyMuPDF
import docx
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

def get_outline_analysis(text, kunci):
    client = OpenAI(api_key=kunci)
    prompt = (
        "Diberikan isi dokumen berikut, ekstrak struktur atau outline dokumen secara hierarkis. "
        "Tampilkan daftar judul utama, bab, subbab, dan sub-subbab bila ada.\n\n"
        f"{text[:6000]}"
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

    return get_outline_analysis(text, kunci)
