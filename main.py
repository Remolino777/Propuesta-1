import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import time
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
import toml








#______________________________________________CACHE ELEMENTS FUNCTIONS



@st.cache_resource
def cargar_imagen():    
    return "psa logo.png"

@st.cache_resource
def load_ml():    
    classifier = joblib.load('modelo_entrenado_01.pkl')
    return  classifier

@st.cache_resource
def load_sc():    
    sc = joblib.load('scaler.pkl')
    return  sc


classifier = load_ml()
sc = load_sc()

#______________________________________________VARIABLES



ruta_img = cargar_imagen()
d_registro =[]

ndpb = 0
biopsia_neg = 0  #Biopsia previa
fiebre_si = 0 
itu_si = 0
tc_hyu = 0
tc_u = 0
aa_ecoli = 0
pr_acg =0
pr_asccc = 0
rPSA_entre_7_8 = 0
rPSA_mayor_a_10 = 0

#________________________________________________REGISTER FORM 
with st.form('registro',  clear_on_submit=True):
    
    st.title('Medical record')
    st.subheader("Patient's data:")      
    
    
    nombre, apellido, edad, id = st.columns([2,2,1,3])
    
    with nombre:
        st.text_input('Name', placeholder='Name')
        
    with apellido:
        st.text_input('Lastname', placeholder='Lastname')
        
    with edad:    
        edad = st.number_input('Age', min_value=0, placeholder='Age', step=1)
        
    with id:
        st.number_input('Id', placeholder='Id number', step=1)
    
    st.divider()  # ________________________________________________________    
    st.subheader('Prostate specific antigen (PSA):')  
    
    psa = st.radio('',
                ['PSA 0 - 3.99', 'PSA 4 - 6.99', 'PSA 7 - 7.99', 'PSA 8 - 9.99', 'PSA 10+'],
                index=None, horizontal=True)        
    
    st.divider()  # ________________________________________________________
    
    tDiasPB, nDias = st.columns([3,1])
    
    with tDiasPB:
        st.write('Number of days post biopsy in which the infectius complication occurs:')
        
    with nDias:
        ndpb =   st.number_input('', min_value=0, step=1) 
        
    st.divider()  # ________________________________________________________
        
                
    
    # Positivo para 
    st.subheader('Positive for:')
    hos, fi, diabetes, v_pros= st.columns(4)
    
    with hos:
        hos = st.checkbox('Hospitalization last month')
    with fi:
        fiebre = st.checkbox('Fever')
            
    with diabetes:
        diabetes = st.checkbox('Diabetes')  
    with v_pros:            
        v_pros = st.checkbox('Prostate volume')
        
    ecp, cup, b_p, itu1 = st.columns(4)
            
    with ecp:
        ecp = st.checkbox('Chronic lung disease')
    with cup:
        cup = st.checkbox('CUP')
    with b_p:
        biopsia_previa = st.checkbox('Previous biopsies')
            
    with itu1:
        itu7 = st.checkbox('ITU')            
        
    st.subheader('Lab results :')
    
    TC= st.selectbox('Tipo de cultivo :', ('HEMOCULTIVO Y UROCULTIVO', 'UROCULTIVO'), index=None, placeholder='Select a resistance pattern......')
    
    
    PR = st.selectbox('Resistance pattern', ('AMPI, CIPRO Y GENTA', 'AMPI, SULFA, CEFADROXILO, CEFUROXIMO, CIPRO Y CEFEPIME, CEFOTAXIMA'), index=None, placeholder='Select a resistance pattern......')
    
    
    AA = st.selectbox('Isolated agent', ('No', 'E.Coli', 'Psudomonas aeruginosa'), index=None, placeholder='Select an isolated agent......')
    
    Biopsia = st.selectbox('Biopsy result', ('Negativa','Adenocarcinoma Gleason 6',
                            'Adenocarcinoma Gleason 7',
                            'Adenocarcinoma Gleason 8',
                            'Adenocarcinoma Gleason 9',
                            'Carcinoma indiferenciado de celulas claras',
                            'Prostatitis',
                            'Hiperplasica prostatica'                               
                            ),index=None, placeholder='Test result......' )
    
    ATP = st.selectbox('Antibiotic used in prophylaxis',('Fluoroquinolona aminoglicosido', 
                        'Oroquinolona', 
                        'Cefalosporina aminoglucocido',
                        'Otros',
                        ),index=None, placeholder='Antibiotic sellect......')
    
    
    st.divider()#_______________________________________________
    
    
    
    s_button = st.form_submit_button(label="Save patient's data")
    
    
    
    if s_button:  # ____________________________________________ FORM LOGIC
        
        if itu7:
            itu_si = 1                
        if fiebre:
            fiebre_si = 1
        if biopsia_previa:
            biopsia_neg = 1 
        if psa == 'PSA 7 - 7.99':
            rPSA_entre_7_8 = 1            
        if psa == 'PSA 10+':                
            rPSA_mayor_a_10 = 1
        # Patron de resistencia    
        if PR == 'AMPI, CIPRO Y GENTA':
            pr_acg = 1
        if PR == 'AMPI, SULFA, CEFADROXILO, CEFUROXIMO, CIPRO Y CEFEPIME, CEFOTAXIMA':
            pr_asccc = 1
        if AA == 'E.Coli':
            aa_ecoli = 1
        # Tipo de cultivos
        if TC == 'HEMOCULTIVO Y UROCULTIVO':
            tc_hyu = 1                
        if TC == 'UROCULTIVO':
            tc_u = 1
        
        v_clinicas = [ndpb, biopsia_neg, fiebre_si, itu_si,  tc_hyu,
            tc_u, aa_ecoli, pr_acg, pr_asccc, rPSA_entre_7_8, rPSA_mayor_a_10
                    ]
        # v_clinicas_2d = np.array(v_clinicas).reshape(1,-1)
        
        # prediccion de modelo            
        
        hospitalizacion = classifier.predict(sc.transform([v_clinicas])) 
        
        with st.spinner('Procesando los datos...'):
            time.sleep(2)
        
        if hospitalizacion == 1:
            st.warning(' The patient needs to be hospitalized ', icon="⚠️")
        else:
            st.write('Patient data saved')

#________________________________________________LATERAL BAR





# Si el usuario marca la opción para mostrar la barra lateral
with st.sidebar:
    st.subheader('INFO')
    st.image(cargar_imagen())
    st.write("To register the patient in the clinic's database, please complete all the corresponding fields in the form.")
    st.divider()
    st.write('PSA 2024 - @r3mo')