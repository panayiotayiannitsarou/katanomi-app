import streamlit as st
import pandas as pd
import random
import io

st.set_page_config(page_title="Κατανομή Μαθητών", layout="centered")

st.title("📚 Εφαρμογή Κατανομής Μαθητών")

uploaded_file = st.file_uploader("🧾 Ανεβάστε το αρχείο Excel με τους μαθητές", type=["xlsx"])

def assign_sections(df, num_sections=2):
    df["Τμήμα"] = ""
    sections = [f"Α{i+1}" for i in range(num_sections)]
    grouped = df.groupby("Φύλο")
    results = []

    for name, group in grouped:
        group = group.sample(frac=1, random_state=1).reset_index(drop=True)
        chunks = [group.iloc[i::num_sections] for i in range(num_sections)]
        for i, chunk in enumerate(chunks):
            chunk["Τμήμα"] = sections[i]
            results.append(chunk)
    
    return pd.concat(results).reset_index(drop=True)

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("📋 Προεπισκόπηση δεδομένων")
        st.dataframe(df)

        if st.button("🔀 Εκτέλεση Κατανομής"):
            if "Φύλο" not in df.columns:
                st.error("Το πεδίο 'Φύλο' είναι απαραίτητο.")
            else:
                result = assign_sections(df)
                st.success("✅ Η κατανομή ολοκληρώθηκε!")
                st.dataframe(result)

                # Λήψη αρχείου Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    result.to_excel(writer, index=False, sheet_name="Κατανομή")
                    writer.close()
                st.download_button("📥 Λήψη Excel", data=output.getvalue(), file_name="katanomi.xlsx")
    except Exception as e:
        st.error(f"⚠️ Σφάλμα κατά την ανάγνωση του αρχείου: {e}")
