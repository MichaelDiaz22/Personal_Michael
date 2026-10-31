import streamlit as st

# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(page_title="Revelación de Género - Crucigrama", page_icon="🍼", layout="centered")

# ============================================================
# DATOS DEL ACROSTICO Y POSICIONES
# (respuesta_correcta, índice_letra_acrostico, fila, columna_inicial)
# ============================================================
PALABRAS = [
    ("PIJAMA",  2, 0, 2),  # J
    ("JUGUETE", 1, 1, 2),  # U
    ("CAMA",    1, 2, 1),  # A
    ("LOCIÓN",  5, 3, 2),  # N
    ("MAMÁ",    1, 4, 2),  # A
    ("MANTA",   2, 5, 2),  # N
    ("DIENTE",  0, 6, 0),  # D
    ("ARRULLO", 2, 7, 2),  # R
    ("PAÑALES", 5, 8, 2),  # E
    ("SILLA",   0, 9, 2),  # S
]

COL_ACROSTICO = 2  # La columna donde caen las letras del nombre (0-index)
MAX_FILAS = 10
MAX_COLS = 7

# ============================================================
# ESTADO INICIAL
# ============================================================
if "respuestas" not in st.session_state:
    # Matriz para guardar lo que escribe el usuario en cada celda
    st.session_state.respuestas = [["" for _ in range(MAX_COLS)] for _ in range(MAX_FILAS)]

if "verificado" not in st.session_state:
    st.session_state.verificado = False

# ============================================================
# FUNCIONES DE VALIDACIÓN
# ============================================================
def normalizar(s):
    return s.strip().upper().replace("Á","A").replace("É","E").replace("Í","I")\
            .replace("Ó","O").replace("Ú","U").replace("Ü","U")

def es_palabra_correcta(fila_idx):
    respuesta_correcta = PALABRAS[fila_idx][0]
    palabra_usuario = ""
    
    # Reconstruir la palabra leyendo la fila de la matriz
    for c in range(MAX_COLS):
        if st.session_state.respuestas[fila_idx][c] != "":
            palabra_usuario += st.session_state.respuestas[fila_idx][c]
        else:
            # Rellenar con espacio para mantener las posiciones relativas si se deja en blanco
            palabra_usuario += " "

    # Comparar ignorando espacios extra
    return normalizar(palabra_usuario.replace(" ", "")) == normalizar(respuesta_correcta)

# ============================================================
# ESTILOS CSS
# ============================================================
st.markdown("""
<style>
    /* Ocultar etiquetas de los inputs */
    div[data-testid="stTextInput"] label { display: none; }
    
    /* Estilo base para las cajas de texto */
    div[data-testid="stTextInput"] input {
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
        padding: 0;
        height: 45px;
        border-radius: 0;
        text-transform: uppercase;
    }
    
    /* Colores de los bordes según validación */
    .st-emotion-cache-1vbkxwb { /* Clase base de Streamlit, puede variar */
        border-color: #ccc;
    }
    
    /* Ajustar márgenes de las columnas para simular cuadrícula */
    div[data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
    }

    /* Estilo para los números negros */
    .celda-negra {
        background-color: #1A1A1A;
        color: white;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.2rem;
        border: 1px solid #333;
    }
    
    /* Estilo para las casillas vacías donde no hay palabra */
    .celda-vacia {
        height: 45px;
        border: 1px solid transparent;
    }

    /* Estilo para las celdas de la columna del acróstico */
    .acro-cell div[data-testid="stTextInput"] input {
        background-color: #BBDEFB !important; /* Azul claro */
        border: 1px solid #1976D2 !important;
    }
    
    /* Feedback de color rojo/verde */
    .texto-error { color: #C62828; font-weight: bold; text-align: center; font-size: 0.9rem; margin-top: -10px;}
    .texto-ok { color: #2E7D32; font-weight: bold; text-align: center; font-size: 0.9rem; margin-top: -10px;}
    
    .exito {
        background: linear-gradient(135deg,#A5D6A7,#C8E6C9);
        border: 3px solid #2E7D32; border-radius:15px;
        padding:25px; text-align:center; margin-top:20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;color:#C2185B;'>🍼 Revelación de Género 🍼</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Escribe una letra por casilla para descubrir el nombre oculto.</p>", unsafe_allow_html=True)

# ============================================================
# CONSTRUCCIÓN DE LA CUADRÍCULA (CRUCIGRAMA)
# ============================================================
st.write("---")

for f in range(MAX_FILAS):
    cols = st.columns(MAX_COLS)
    
    # Determinar dónde empieza y termina la palabra de esta fila
    _, _, _, col_inicio = PALABRAS[f]
    longitud_palabra = len(PALABRAS[f][0])
    col_fin = col_inicio + longitud_palabra
    
    for c in range(MAX_COLS):
        
        # 1. ES LA COLUMNA DEL ACRÓSTICO
        if c == COL_ACROSTICO:
            with cols[c]:
                st.markdown("<div class='acro-cell'>", unsafe_allow_html=True)
                val = st.text_input(
                    label=f"celda_{f}_{c}", 
                    value=st.session_state.respuestas[f][c], 
                    max_chars=1, 
                    key=f"input_{f}_{c}"
                )
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Actualizar estado
                if val != st.session_state.respuestas[f][c]:
                    st.session_state.respuestas[f][c] = val.upper()
                    st.session_state.verificado = False

        # 2. CASILLAS DE LA PALABRA HORIZONTAL
        elif col_inicio <= c < col_fin:
            with cols[c]:
                # Si es la primera letra, mostramos el número de la pista
                if c == col_inicio:
                    # Truco visual: usamos un HTML que parece celda negra
                    st.markdown(f"<div class='celda-negra'>{f+1}</div>", unsafe_allow_html=True)
                else:
                    val = st.text_input(
                        label=f"celda_{f}_{c}", 
                        value=st.session_state.respuestas[f][c], 
                        max_chars=1, 
                        key=f"input_{f}_{c}"
                    )
                    if val != st.session_state.respuestas[f][c]:
                        st.session_state.respuestas[f][c] = val.upper()
                        st.session_state.verificado = False
        
        # 3. CASILLAS VACÍAS (Fondo transparente)
        else:
            with cols[c]:
                st.markdown("<div class='celda-vacia'></div>", unsafe_allow_html=True)
                
    # Validación visual por fila (Debajo de la fila)
    if st.session_state.verificado:
        if es_palabra_correcta(f):
            st.markdown(f"<div class='texto-ok'>Fila {f+1}: ¡Correcto! ✅</div>", unsafe_allow_html=True)
        elif any(st.session_state.respuestas[f]): # Solo si escribió algo
            st.markdown(f"<div class='texto-error'>Fila {f+1}: Revisa esta palabra ❌</div>", unsafe_allow_html=True)

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

# Verificar que la columna vertical forme JUAN ANDRES
acrostico_formado = "".join([st.session_state.respuestas[i][COL_ACROSTICO] for i in range(MAX_FILAS)])
acrostico_formado = normalizar(acrostico_formado)
acrostico_correcto = acrostico_formado == "JUANANDRES"

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
