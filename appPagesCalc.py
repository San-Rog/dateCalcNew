import streamlit as st
import os
from datetime import date

def main():
    #Define the pages
    pages = {
    "Opções": [st.Page("contaDiasNew.py", title="Tela de entrada de dados", icon="📆"), 
              st.Page("calDaysCurrentNew.py", title="Cálculo de dias corridos", icon="📑"), 
              st.Page("calDaysUsefulNew.py", title="Cálculo de dias úteis", icon="📙")]   
    }
    pg = st.navigation(pages)
    pg.run()    

if __name__ == '__main__':
    main()