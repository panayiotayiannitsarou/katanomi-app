import streamlit as st
import pandas as pd

st.set_page_config(page_title="Εργαλείο Κατανομής Μαθητών", layout="centered")

st.title("📚 Εργαλείο Κατανομής Μαθητών")
st.markdown("Ανεβάστε το αρχείο Excel με τα στοιχεία των μαθητών.")

uploaded_file = st.file_uploader("Αρχείο Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Προεπισκόπηση δεδομένων:")
    st.dataframe(df)

    st.success("Τα δεδομένα φορτώθηκαν επιτυχώς!")
