import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import time
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler

#______________________________________________LOAD FILE
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    

#______________________________________________CACHE ELEMENTS
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


#______________________________________________FUNCIONES




#______________________________________________AUTENTICATOR
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],    
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

#Render de loggin widget
fields_01 = ['login', 'main']
name, authentication_status, username = authenticator.login(fields=fields_01)




        
if st.session_state["authentication_status"]:
    
    authenticator.logout()
    with st.spinner('Wait for it...'): # Pantalla de carga
        time.sleep(2)
    st.write(f'Welcome *{st.session_state["name"]}*')    
    
    with st.form('registro', clear_on_submit=True):
        
        st.title('Registro medico')
        st.subheader('Datos del paciente:')      
        
        
        nombre, apellido, edad, id = st.columns([2,2,1,3])
        
        with nombre:
            st.text_input('Nombre', placeholder='Nombre')
            
        with apellido:
            st.text_input('Apellido', placeholder='Apellido')
            
        with edad:    
            edad = st.number_input('Edad', min_value=0, placeholder='Edad', step=1)
            
        with id:
            st.number_input('Id', placeholder='Numero de Identificacion', step=1)
        
        st.divider()  # ________________________________________________________    
        st.subheader('Niveles Antigeno Prostatico (PSA):')  
        
        psa = st.radio('',
                 ['PSA 0 - 3.99', 'PSA 4 - 6.99', 'PSA 7 - 7.99', 'PSA 8 - 9.99', 'PSA 10+'],
                 index=None, horizontal=True)        
        
        st.divider()  # ________________________________________________________
        
        tDiasPB, nDias = st.columns([3,1])
        
        with tDiasPB:
            st.write('NUMERO DE DIAS POST BIOPSIA EN QUE SE PRESENTA LA COMPLICACIÓN INFECCIOSA')
            
        with nDias:
            ndpb =   st.number_input('', min_value=0, step=1) 
            
        st.divider()  # ________________________________________________________
            
                   
        
        # Positivo para 
        st.subheader('Positivo para :')
        hos, fi, diabetes, v_pros= st.columns(4)
        
        with hos:
            hos = st.checkbox('Hospitalizacion ultimo mes')
        with fi:
            fiebre = st.checkbox('Fiebre')
              
        with diabetes:
            diabetes = st.checkbox('Diabetes')  
        with v_pros:            
            v_pros = st.checkbox('Volumen prostatico')
            
        ecp, cup, b_p, itu1 = st.columns(4)
                
        with ecp:
            ecp = st.checkbox('Enfermedad cronica pulmonar')
        with cup:
            cup = st.checkbox('CUP')
        with b_p:
            biopsia_previa = st.checkbox('Biopsias previas')
                
        with itu1:
            itu7 = st.checkbox('ITU')            
            
        st.subheader('resultados laboratorio :')
        
        TC= st.selectbox('Tipo de cultivo :', ('HEMOCULTIVO Y UROCULTIVO', 'UROCULTIVO'), index=None, placeholder='Seleccione un patrón de resistencia......')
        
        
        PR = st.selectbox('Patron de resistencia', ('AMPI, CIPRO Y GENTA', 'AMPI, SULFA, CEFADROXILO, CEFUROXIMO, CIPRO Y CEFEPIME, CEFOTAXIMA'), index=None, placeholder='Seleccione un patrón de resistencia......')
        
        
        AA = st.selectbox('Agente aislado', ('No', 'E.Coli', 'Psudomonas aeruginosa'), index=None, placeholder='Seleccione un agente aislado......')
        
        Biopsia = st.selectbox('Resultado biopsia', ('Negativa','Adenocarcinoma Gleason 6',
                               'Adenocarcinoma Gleason 7',
                               'Adenocarcinoma Gleason 8',
                               'Adenocarcinoma Gleason 9',
                               'Carcinoma indiferenciado de celulas claras',
                               'Prostatitis',
                               'Hiperplasica prostatica'                               
                               ),index=None, placeholder='Seleccione un resultado......' )
        
        ATP = st.selectbox('Antibiotico utilizado en la profilaxis',('Fluoroquinolona aminoglicosido', 
                           'Oroquinolona', 
                           'Cefalosporina aminoglucocido',
                           'Otros',
                           ),index=None, placeholder='Seleccione un antibiotico......')
        
        
        st.divider()#_______________________________________________
        
        
        
        s_button = st.form_submit_button(label='Registrar')
        
        
        
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
                st.warning('El pasiente nesecita ser hospitalizado', icon="⚠️")
            else:
                st.write('Paciente registrado')
    
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
    
    
elif st.session_state["authentication_status"] is None:
    logout_completed = True
    with st.spinner('Wait for it...'): # Pantalla de carga
        time.sleep(3)
        
    col1, col2, col3 = st.columns(3)
    with col1:
        pass  
    with col2:   
        st.write("")
        st.image(ruta_img)
        st.write("")        
    with col3:
        pass
    st.subheader("LABORATORIO EXPERIMENTAL DEL CANCER DE PROSTATA")     




