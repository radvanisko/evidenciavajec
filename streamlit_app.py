import streamlit as st
import pandas as pd
from datetime import date

# Nastavenie vzhľadu
st.set_page_config(page_title="Evi-Vajce", page_icon="🥚")
st.title("🥚 Evidencia znášky")

# Jednoduchý systém "hesla" pre prístup (nahrádza zložité schvaľovanie)
access_code = st.sidebar.text_input("Zadajte prístupový kód", type="password")

if access_code == "moje-sliepky-2026":  # Tu si nastavíte svoje heslo
    st.success("Prístup schválený")
    
    # Formulár pre zápis
    with st.form("entry_form"):
        kurin = st.selectbox("Vyberte kurín", ["Horný dvor", "Zadný dvor", "Pri stodole"])
        pocet = st.number_input("Počet vajec", min_value=0, step=1)
        zapisal = st.text_input("Vaše meno")
        poznamka = st.text_area("Poznámka")
        
        submitted = st.form_submit_button("Uložiť znášku")
        
        if submitted:
            # Tu sa dáta odošlú do vašej Google tabuľky (cez st.connection)
            st.info(f"Zápis: {kurin}, {pocet} ks, zapísal {zapisal} dňa {date.today()}")
            st.balloons()
else:
    st.warning("Prosím, zadajte kód, ktorý vám poskytol majiteľ farmy.")
