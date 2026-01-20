import streamlit as st
import pandas as pd
from datetime import date
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Evi-Vajce", page_icon="🥚")
st.title("🥚 Evidencia znášky")

conn = st.connection("gsheets", type=GSheetsConnection)

# Prihlásenie
st.sidebar.header("Prihlásenie")
access_code = st.sidebar.text_input("Vstupný kód", type="password")
user_nickname = st.sidebar.text_input("Váš Nickname", placeholder="napr. Jano")

if access_code == "moje-sliepky-2026" and user_nickname:
    st.success(f"Prihlásený: {user_nickname}")
    
    with st.form("entry_form", clear_on_submit=True):
        kurin = st.selectbox("Vyberte kurín", ["Stare sliepky", "Nove sliepky", "Volny vybeh"])
        pocet = st.number_input("Počet vajec", min_value=0, step=1)
        poznamka = st.text_area("Poznámka")
        submitted = st.form_submit_button("Uložiť")
        
        if submitted:
            new_row = pd.DataFrame([{
                "Datum": str(date.today()),
                "Kurin": kurin,
                "Pocet": int(pocet),
                "Meno": user_nickname,
                "Poznamka": poznamka
            }])
            
            try:
                # Načítanie dát s ošetrením prázdnej tabuľky
                existing_data = conn.read(worksheet="Zaznamy")
                if existing_data.empty:
                    updated_df = new_row
                else:
                    updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                
                conn.update(worksheet="Zaznamy", data=updated_df)
                st.success("Uložené!")
                st.balloons()
            except Exception as e:
                st.error(f"Chyba pri zápise: Skontrolujte, či sa hárok volá 'Zaznamy' a či je zdieľaný ako Editor.")

    # Zobrazenie histórie
    try:
        data = conn.read(worksheet="Zaznamy")
        if not data.empty:
            st.divider()
            st.subheader("História")
            st.dataframe(data.tail(10))
    except:
        st.info("Zatiaľ žiadne dáta na zobrazenie.")

else:
    st.info("Zadajte kód a meno v bočnom paneli.")
