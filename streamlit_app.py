import streamlit as st
import pandas as pd
from datetime import date
from streamlit_gsheets import GSheetsConnection

# Nastavenie vzhľadu
st.set_page_config(page_title="Evi-Vajce", page_icon="🥚")
st.title("🥚 Evidencia znášky")

# Pripojenie k Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

access_code = st.sidebar.text_input("Zadajte prístupový kód", type="password")

if access_code == "moje-sliepky-2026":
    st.success("Prístup schválený")
    
    with st.form("entry_form"):
        kurin = st.selectbox("Vyberte kurín", ["Horný dvor", "Zadný dvor", "Pri stodole"])
        pocet = st.number_input("Počet vajec", min_value=0, step=1)
        zapisal = st.text_input("Vaše meno")
        poznamka = st.text_area("Poznámka")
        
        submitted = st.form_submit_button("Uložiť znášku")
        
        if submitted:
            # Vytvorenie nového riadku dát
            new_data = pd.DataFrame([{
                "Datum": str(date.today()),
                "Kurin": kurin,
                "Pocet": int(pocet),
                "Meno": zapisal,
                "Poznamka": poznamka
            }])
            
            # Načítanie starých dát a pridanie nových
            existing_data = conn.read(worksheet="Zaznamy")
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            
            # SKUTOČNÝ ZÁPIS DO GOOGLE SHEETS
            conn.update(worksheet="Zaznamy", data=updated_df)
            
            st.success(f"Dáta boli úspešne uložené do Google tabuľky!")
            st.balloons()
else:
    st.warning("Zadajte prístupový kód.")
