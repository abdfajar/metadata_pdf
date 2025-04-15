import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt
import os

# UI: Input API Key
st.title("📊 PandasAI Chat with Auto Visualization")
st.markdown("Masukkan API Key OpenAI untuk mulai.")
api_key = st.text_input("🔑 OpenAI API Key", type="password")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Upload CSV file
    uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("📄 Data Preview")
        st.dataframe(df.head())

        # SmartDataframe dengan LLM
        llm = OpenAI(api_token=api_key)
        sdf = SmartDataframe(df, config={"llm": llm})

        # Input query
        st.subheader("💬 Tanyakan sesuatu tentang data")
        user_query = st.text_area("Ketik pertanyaanmu di sini", height=100)

        if st.button("🔍 Jalankan Query") and user_query:
            with st.spinner("Memproses pertanyaan..."):
                try:
                    result = sdf.chat(user_query)

                    # Auto detect & show result
                    if isinstance(result, plt.Figure):
                        st.subheader("📈 Visualisasi")
                        st.pyplot(result)
                    elif isinstance(result, pd.DataFrame):
                        st.subheader("📊 Tabel Hasil")
                        st.dataframe(result)
                    else:
                        st.subheader("📝 Jawaban")
                        st.write(result)
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
else:
    st.warning("Silakan masukkan API Key terlebih dahulu.")
