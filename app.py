# file: app.py

import streamlit as st
import random
import pdfplumber

st.set_page_config(page_title="Quiz Rimescolati", layout="wide")
st.title("🧠 Generatore di Quiz Rimescolati")
st.write("Carica il PDF dei quiz, seleziona il numero e visualizza le risposte in ordine casuale.")

uploaded_file = st.file_uploader("📄 Carica il file PDF", type="pdf")

if uploaded_file:
    quiz = []
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    if len(row) >= 5 and row[0].isdigit():
                        domanda = row[1].strip()
                        risposte = [row[2].strip(), row[3].strip(), row[4].strip()]
                        corretta = risposte[0]
                        risposte_mischiate = risposte[:]
                        random.shuffle(risposte_mischiate)
                        indice_corretta = risposte_mischiate.index(corretta)
                        quiz.append({
                            "domanda": domanda,
                            "risposte": risposte_mischiate,
                            "corretta": chr(65 + indice_corretta)
                        })

    if quiz:
        indice = st.number_input("📌 Seleziona quiz", min_value=0, max_value=len(quiz)-1, step=1)
        st.subheader(f"Quiz {indice + 1}")
        st.write(quiz[indice]['domanda'])
        for i, r in enumerate(quiz[indice]['risposte']):
            st.write(f"{chr(65 + i)}. {r}")
        if st.button("🔍 Mostra risposta corretta"):
            st.success(f"✅ Risposta corretta: **{quiz[indice]['corretta']}**")
    else:
        st.warning("Nessun quiz estratto. Controlla il formato del PDF.")
