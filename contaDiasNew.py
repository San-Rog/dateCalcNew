import streamlit as st 
import streamlit.components.v1 as components
import datetime
import time
import os
import datetime
from datetime import date
from datetime import timedelta
import warnings
warnings.filterwarnings("ignore")

def dateFullLang(date):
    dateStr = date.strftime("%d/%m/%Y")
    weekNum = date.weekday()
    weekStr = weeks[weekNum]
    dateFull = f'{dateStr} ({weekStr})'
    return dateFull

def findCurFul():
    time.sleep(timeDay*1.1)
    dateIni = st.session_state[listKeys[0]]
    num = int(st.session_state[listKeys[1]])
    val = checkDate(dateIni, num)
    if not val:
        return
    for mode in [0, 1]:
        daySeq = []
        count = 0 
        n = 0 
        while count < num:
            dateNew = dateIni + datetime.timedelta(days=n)
            weekNum = dateNew.weekday()
            if n == 0:
                pass
            else: 
                if mode == 0:
                    if count == num - 1: 
                        if any ([weekNum == 5 or weekNum == 6]):
                            pass
                        else:
                            count += 1
                    else:
                        count += 1
                else:
                    if any ([weekNum == 5 or weekNum == 6]):
                        pass
                    else:
                        count += 1
            daySeq.append(dateNew)    
            n += 1
        dateFinal = max(daySeq)
        dateStr = dateFullLang(dateFinal)
        if dateStr not in valuesStr:
            valuesStr.append(dateStr)
    st.session_state[listKeys[3]] = valuesStr[0]
    st.session_state[listKeys[4]] = valuesStr[1]
    st.session_state[listKeys[1]] = num        
        
def zeraWidget():
    iniFinally(1)
    
def iniFinally(mode):
    if mode == 0:
        for key in listKeys:
            if key not in st.session_state:
                try:
                    st.session_state[key] = keyNames[key]
                except:
                    pass        
    else:
        try:
            for key in listKeys:
                del st.session_state[key]
        except:
            pass
        iniFinally(0)
    try:
        st.rerun()
    except:
        pass
    st.session_state['acesso'] = [st.session_state.calendar, 
                                  st.session_state.days]
    
def changeDays():
    time.sleep(timeDay)
    nDays = st.session_state[listKeys[2]]
    nPlus = st.session_state[listKeys[1]]
    del st.session_state[listKeys[2]]
    st.session_state[listKeys[1]] = nPlus + nDays
    
def changeDate():
    valCal = st.session_state[listKeys[0]]
    del st.session_state[listKeys[0]]
    if valCal is None: 
        st.session_state[listKeys[0]] = date.today()
    else:
        try:
            st.session_state[listKeys[0]] = valCal
        except:
            st.session_state[listKeys[0]] = date.today()
            
def checkDate(dateSel, nDays):
    time.sleep(timeDay*1.1)    
    if nDays <= 0:
        block = f"Não se fará cálculo de datas, pois o número de dias é igual a {nDays}!"
        endor = False
    else:
        novaData = dateSel + datetime.timedelta(days=nDays)
        block = f"O cálculo leva em conta data de {dateSel.strftime('%d/%m/%Y')} e {nDays} dia(s)!"
        endor = True
    st.toast(f"⚠️ {block}")
    time.sleep(0.2)
    return endor

def changeSlCalend():
    time.sleep(timeDay)
    nDays = st.session_state[listKeys[5]]
    dateCalend = st.session_state[listKeys[0]] 
    newDate = dateCalend + timedelta(days=nDays)
    if newDate < dateMin: 
        newDate = dateMin
    if newDate > dateMax:
        newDate = dateMax
    st.session_state[listKeys[0]] = newDate
    del st.session_state[listKeys[5]]
    
def listFiles():
    try:
        @st.dialog('📁 Arquivos nesta sessão de trabalho (pasta Downloads)')
        def lista(files):
            nFiles = len(files)
            if nFiles > 0:
                filesStr = f'{nFiles} arquivo(s): '
                for f, file in enumerate(files): 
                    filesStr += f'#{f+1} 💾{file} '
            else:
                fileStr = 'Não há download de arquivos nesta sessão de trabalho'
            st.markdown(filesStr)
        lista(st.session_state.files)
    except:
        pass

def main():
    iniFinally(0)
    with st.container(border=6):    
        colCalendar, sldDate, colDays, sldDays = st.columns([2.7, 2.5, 2.8, 2.5], gap='medium', 
                                                            vertical_alignment="center")
        dateSel = colCalendar.date_input(label='Data inicial', value='today', 
                                        key=listKeys[0], format="DD/MM/YYYY", on_change=changeDate)
        nSlDate = sldDate.slider(label='Incremento de dias', min_value=0, max_value=6000, 
                                 key=listKeys[5], step=1, on_change=changeSlCalend, label_visibility="hidden")                         
        nDays = colDays.number_input(label='Número de dias', step=1, key=listKeys[1])  
        nPlus = sldDays.slider(label='Incremento de dias', min_value=0, max_value=6000, 
                               key=listKeys[2], step=1, on_change=changeDays, label_visibility="hidden")        
        colCurrent, colUseful = st.columns(2)
        dateCurrent = colCurrent.text_input(label='Data final (dias corridos)', value=st.session_state[listKeys[3]], 
                          disabled=True, key=listKeys[3], help='É preenchido única e automaticamente quando se calcula a data.')
        dateUseful = colUseful.text_input(label='Data final (dias úteis)', value=st.session_state[listKeys[4]], 
                          disabled=True, key=listKeys[4], help='É preenchido única e automaticamente se calcula a data.')        
        colCal, colFiles, colClear = st.columns(3, gap='small', vertical_alignment='center')
    colClear.button(label='Limpeza', use_container_width=True, icon=":material/refresh:", 
                    on_click=zeraWidget)
    colFiles.button(label='Arquivos', use_container_width=True, icon=":material/calculate:", on_click=listFiles)
    colCal.button(label='Cálculo', use_container_width=True, icon=":material/calculate:", on_click=findCurFul)
            
if __name__ == '__main__':
    st.markdown("# Tela de entrada de dados 📆")
    global dictKeys, listKeys, timeDay
    global months, weeks
    global dateMin, dateMax
    global valuesStr, valCalc
    keyNames = {'calendar': date.today(), 
                'days': 0, 
                'plus': 0, 
                'current': "", 
                'useful': "", 
                'sldata': 0}
    listKeys = list(keyNames.keys())
    #st.session_state[listKeys[3]] = ""
    #st.session_state[listKeys[4]] = ""    
    timeDay = float(0.50)    
    months = {1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril', 5:'maio', 6: 'junho', 
              7: 'julho', 8: 'agosto', 9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'}
    weeks = {6: 'domingo', 0: 'segunda-feira', 1: 'terça-feira', 
             2: 'quarta-feira', 3: 'quinta-feira', 4: 'sexta-feira', 
             5: 'sábado'}
    dateMin = date(1960, 1, 1)
    dateMax = date(2100, 12, 31)
    valuesStr = []
    valCalc = [False]
    if 'acesso' not in st.session_state:
        st.session_state['acesso'] = []
    if 'files' not in st.session_state:
        st.session_state['files'] = []    
    main()