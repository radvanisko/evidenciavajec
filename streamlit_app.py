import streamlit as st
import pandas as pd
from datetime import date
from streamlit_gsheets import GSheetsConnection

# Nastavenie vzhľadu
st.set_page_config(page_title="Radman-Vajce", page_icon="🥚")
st.title("🥚 Evidencia znášky")

# Pripojenie k Google Sheets (vyžaduje URL v Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

# --- PRIHLASOVACIA SEKČIA V BOČNOM PANELI ---
st.sidebar.header("Prihlásenie")
access_code = st.sidebar.text_input("Vstupný kód", type="password")
# Pridáme pole pre zvolený Nickname
user_nickname = st.sidebar.text_input("Váš Nickname (Meno)", placeholder="Napr. Jano")

if access_code == "moje-sliepky-2026" and user_nickname:
    st.success(f"Prihlásený ako: **{user_nickname}**")
    
    # --- FORMULÁR PRE ZÁPIS ---
    with st.form("entry_form", clear_on_submit=True):
        st.subheader("Nový záznam")
        kurin = st.selectbox("Vyberte kurín", ["Horný dvor", "Zadný dvor", "Pri stodole"])
        pocet = st.number_input("Počet vajec", min_value=0, step=1)
        poznamka = st.text_area("Poznámka (nepovinné)")
        
        submitted = st.form_submit_button("Uložiť znášku")
        
        if submitted:
            # Vytvorenie nového riadku dát - MENO SA BERIE Z NICKNAME
            new_data = pd.DataFrame([{
                "Datum": str(date.today()),
                "Kurin": kurin,
                "Pocet": int(pocet),
                "Meno": user_nickname,  # Použije meno zadané pri prihlásení
                "Poznamka": poznamka
            }])
            
            # Načítanie starých dát zo Sheets
            existing_data = conn.read(worksheet="Zaznamy")
            
            # Spojenie dát
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            
            # Odoslanie do Google Sheets
            conn.update(worksheet="Zaznamy", data=updated_df)
            
            st.success(f"Hotovo! {pocet} vajec bolo zapísaných pod menom {user_nickname}.")
            st.balloons()

elif access_code == "moje-sliepky-2026" and not user_nickname:
    st.info("👈 Prosím, zadajte svoj Nickname v bočnom paneli.")
else:
    st.warning("👈 Zadajte prístupový kód pre odomknutie aplikácie.")

# --- VOLITEĽNÉ: ZOBRAZENIE POSLEDNÝCH ZÁPISOV ---
if access_code == "moje-sliepky-2026":
    st.divider()
    st.subheader("Posledné záznamy v tabuľke")
    data = conn.read(worksheet="Zaznamy")
    st.dataframe(data.tail(5)) # Ukáže posledných 5 riadkov
