import streamlit as st

# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(page_title="Revelación de Género - Crucigrama", page_icon="🍼", layout="centered")

# ============================================================
# DEFINICIÓN DEL CRUCIGRAMA
# (respuesta, col_inicio, col_acrostico)
# ============================================================
PALABRAS = [
    ("PIJAMA",  2, 2),  # Fila 1: J
    ("JUGUETE", 2, 2),  # Fila 2: U
    ("CAMA",    1, 2),  # Fila 3: A
    ("LOCIÓN",  2, 2),  # Fila 4: N
    ("MAMÁ",    2, 2),  # Fila 5: A
    ("MANTA",   2, 2),  # Fila 6: N
    ("DIENTE",  0, 6),  # Fila 7: D (empieza en col 0, cruza en col 6)
    ("ARRULLO", 2, 2),  # Fila 8: R
    ("PAÑALES", 2, 2),  # Fila 9: E
    ("SILLA",   2, 2),  # Fila 10: S
]

# El mapa visual exacto de tu imagen (N = Número/Negro, X = Letra, _ = Vacío)
# Esto asegura que las filas largas como ARRULLO (8 letras) y PAÑALES (8 letras) quepan bien.
MAPA_VISUAL = {
    0:  {2: "N", 3: "X", 4: "X", 5: "X", 6: "X", 7: "X"},
    1:  {2: "N", 3: "X", 4: "X", 5: "X", 6: "X", 7: "X", 8: "X"},
    2:  {1: "N", 2: "X", 3: "X", 4: "X"},
    3:  {2: "N", 3: "X", 4: "X", 5: "X", 6: "X", 7: "X"},
    4:  {2: "N", 3: "X", 4: "X", 5: "X"},
    5:  {2: "N", 3: "X", 4: "X", 5: "X", 6: "X"},
    6:  {0: "N", 1: "X", 2: "X", 3: "X", 4: "X", 5: "X", 6: "X"},
    7:  {2: "N", 3: "X", 4: "X", 5: "X", 6: "X", 7: "X", 8: "X", 9: "X"},
    8:  {2: "N", 3: "X", 4: "X", 5: "X", 6: "X", 7: "X", 8: "X", 9: "X"},
    9:  {2: "N", 3: "X", 4: "X", 5: "X", 6: "X", 7: "X"},
}

MAX_FILAS = 10
MAX_COLS = 11  # Ampliado para que quepan las palabras más largas

# ============================================================
# ESTADO INICIAL
# ============================================================
if "respuestas" not in st.session_state:
    st.session_state.respuestas = [["" for _ in range(MAX_COLS)] for _ in range(MAX_FILAS)]
if "verificado" not in st.session_state:
    st.session_state.verificado = False

# ============================================================
# FUNCIONES
# ============================================================
def normalizar(s):
    return s.strip().upper().replace("Á","A").replace("É","E").replace("Í","I")\
            .replace("Ó","O").replace("Ú","U").replace("Ü","U")

def es_palabra_correcta(fila_idx):
    respuesta_correcta = PALABRAS[fila_idx][0]
    col_inicio = PALABRAS[fila_idx][1]
    
    # Extraer solo las letras que pertenecen a la palabra según el mapa
    palabra_usuario = ""
    for c in range(MAX_COLS):
        if MAPA_VISUAL[fila_idx].get(c) == "X":
            palabra_usuario += st.session_state.respuestas[fila_idx][c]
            
    return normalizar(palabra_usuario) == normalizar(respuesta_correcta)

# ============================================================
# ESTILOS CSS (Para simular el crucigrama)
# ============================================================
st.markdown("""
<style>
    /* Ocultar etiquetas de los inputs */
    div[data-testid="stTextInput"] label { display: none; }
    
    /* Estilo de las casillas de texto (blancas) */
    div[data-testid="stTextInput"] input {
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        padding: 0;
        height: 40px;
        border-radius: 0;
        text-transform: uppercase;
        border: 1px solid #999;
    }
    
    /* Quitar márgenes a las columnas para que se toquen */
    div[data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
    }

    /* Cuadros negros con el número */
    .celda-negra {
        background-color: #1A1A1A;
        color: white;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.1rem;
        border: 1px solid #333;
    }
    
    /* Espacios vacíos */
    .celda-vacia {
        height: 40px;
        border: 1px solid transparent;
    }

    /* Forzar que la columna del acróstico sea azul */
    .acro-col div[data-testid="stTextInput"] input {
        background-color: #94B8D6 !important; /* Azul del crucigrama */
        border: 1px solid #3A6A94 !important;
    }
    
    /* Mensajes de validación */
    .texto-error { color: #C62828; font-weight: bold; text-align: center; font-size: 0.85rem; margin-top: 2px; margin-bottom: 10px;}
    .texto-ok { color: #2E7D32; font-weight: bold; text-align: center; font-size: 0.85rem; margin-top: 2px; margin-bottom: 10px;}
    
    .exito {
        background: linear-gradient(135deg,#A5D6A7,#C8E6C9);
        border: 3px solid #2E7D32; border-radius:15px;
        padding:25px; text-align:center; margin-top:20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;color:#C2185B;'>🍼 Revelación de Género 🍼</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Escribe una letra por casilla para descubrir el nombre oculto.</p>", unsafe_allow_html=True)
st.write("---")

# ============================================================
# RENDERIZAR LA CUADRÍCULA
# ============================================================
for f in range(MAX_FILAS):
    cols = st.columns(MAX_COLS)
    
    for c in range(MAX_COLS):
        tipo_celda = MAPA_VISUAL[f].get(c, "_")
        
        with cols[c]:
            # 1. CUADRO NEGRO (Número)
            if tipo_celda == "N":
                # El número es f+1 (Fila 1, Fila 2, etc.)
                st.markdown(f"<div class='celda-negra'>{f+1}</div>", unsafe_allow_html=True)
                
            # 2. LETRA (Input)
            elif tipo_celda == "X":
                # Si es la columna del acróstico (columna 6), le ponemos la clase azul
                es_acrostico = (c == 6)
                clase_extra = "acro-col" if es_acrostico else ""
                
                if clase_extra:
                    st.markdown("<div class='acro-col'>", unsafe_allow_html=True)
                
                val = st.text_input(
                    label=f"celda_{f}_{c}", 
                    value=st.session_state.respuestas[f][c], 
                    max_chars=1, 
                    key=f"input_{f}_{c}"
                )
                
                if clase_extra:
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Guardar en memoria
                if val != st.session_state.respuestas[f][c]:
                    st.session_state.respuestas[f][c] = val.upper()
                    st.session_state.verificado = False
                    
            # 3. VACÍO
            else:
                st.markdown("<div class='celda-vacia'></div>", unsafe_allow_html=True)
                
    # Feedback por fila (debajo de cada palabra)
    if st.session_state.verificado:
        if es_palabra_correcta(f):
            st.markdown(f"<div class='texto-ok'>Fila {f+1} correcta ✅</div>", unsafe_allow_html=True)
        elif any(st.session_state.respuestas[f]): # Solo si el usuario escribió algo
            st.markdown(f"<div class='texto-error'>Fila {f+1}: Revisa esta palabra ❌</div>", unsafe_allow_html=True)
        else:
            st.write("") # Espacio para mantener la alineación

st.write("---")

# ============================================================
# BOTÓN VERIFICAR
# ============================================================
if st.button("🔍 Verificar respuestas", use_container_width=True, type="primary"):
    st.session_state.verificado = True

# ============================================================
# VALIDACIÓN FINAL
# ============================================================
todas_correctas = all(es_palabra_correcta(i) for i in range(len(PALABRAS)))

# Verificar que la columna 6 forme JUAN ANDRES
acrostico_formado = "".join([st.session_state.respuestas[i][6] for i in range(MAX_FILAS)])
acrostico_correcto = normalizar(acrostico_formado) == "JUANANDRES"

if st.session_state.verificado and todas_correctas and acrostico_correcto:
    st.balloons()
    st.markdown(
        f"<div class='exito'>"
        f"<h2>🎉 ¡Felicidades! 🎉</h2>"
        f"<p style='font-size:1.2rem;color:#1B5E20;'>¡Has completado el crucigrama!</p>"
        f"<h1>El bebé es...</h1>"
        f"<h1 style='font-size:2.2rem;color:#C2185B;'>JUAN ANDRES DIAZ CORTES</h1>"
        f"<p style='font-size:1.1rem;color:#2E7D32;'>💙 ¡Bienvenido, pequeño! 💙</p>"
        f"</div>",
        unsafe_allow_html=True)
elif st.session_state.verificado and not todas_correctas:
    st.info("🔎 Aún hay palabras incorrectas. Revisa los recuadros en rojo.")
