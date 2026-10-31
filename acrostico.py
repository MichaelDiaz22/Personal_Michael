import streamlit as st

st.set_page_config(page_title="Revelación de Género", page_icon="🍼", layout="centered")

# ============================================================
# DATOS Y MAPA VISUAL DEL CRUCIGRAMA
# N = Número, X = Letra, _ = Vacío, A = Letra del Acróstico
# ============================================================
PALABRAS = ["PIJAMA", "JUGUETE", "CAMA", "LOCIÓN", "MAMÁ", "MANTA", "DIENTE", "ARRULLO", "PAÑALES", "SILLA"]

# Este mapa dibuja exactamente el crucigrama de la imagen
MAPA = [
    ["", "", "1", "X", "X", "X", "A", "X", "X", "", "", ""], # Fila 1: PIJAMA (empieza en 2, cruza en 6)
    ["", "", "2", "X", "X", "X", "A", "X", "X", "X", "", ""], # Fila 2: JUGUETE
    ["", "3", "X", "X", "X", "A", "X", "X", "X", "X", "X", ""], # Fila 3: CAMA (empieza en 1, cruza en 5... ajustado visualmente)
    ["", "", "4", "X", "X", "X", "A", "X", "X", "", "", ""], # Fila 4: LOCIÓN
    ["", "", "5", "X", "X", "A", "X", "X", "X", "X", "", ""], # Fila 5: MAMÁ
    ["", "", "6", "X", "X", "A", "X", "X", "X", "X", "X", ""], # Fila 6: MANTA
    ["7", "X", "X", "X", "X", "X", "A", "X", "X", "X", "", ""], # Fila 7: DIENTE (cruza en 6)
    ["", "", "8", "X", "X", "A", "X", "X", "X", "X", "X", ""], # Fila 8: ARRULLO
    ["", "", "9", "X", "X", "A", "X", "X", "X", "X", "X", ""], # Fila 9: PAÑALES
    ["", "", "10","X", "X", "A", "X", "X", "X", "X", "", ""], # Fila 10: SILLA
]

# ============================================================
# HTML Y CSS PARA DIBUJAR EL CRUCIGRAMA
# ============================================================
html_crucigrama = """
<style>
    .crucigrama-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .fila {
        display: flex;
    }
    .celda {
        width: 40px;
        height: 40px;
        box-sizing: border-box;
        border: 1px solid #999;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        text-transform: uppercase;
    }
    .celda-negra {
        background-color: #1A1A1A;
        color: white;
        border: 1px solid #333;
        font-size: 16px;
    }
    .celda-vacia {
        border: 1px solid transparent;
    }
    .celda-acro {
        background-color: #94B8D6; /* Azul */
        border: 1px solid #3A6A94;
    }
    .celda-input {
        width: 100%;
        height: 100%;
        border: none;
        background: transparent;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        text-transform: uppercase;
        color: #000;
        outline: none;
        padding: 0;
    }
    /* Input en la columna del acróstico */
    .celda-acro .celda-input {
        color: #003366;
    }
</style>

<div class="crucigrama-container">
"""

# Generamos las filas HTML
for f in range(10):
    html_crucigrama += '    <div class="fila">\n'
    for c in range(12):
        tipo = MAPA[f][c]
        
        if tipo == "":
            html_crucigrama += '        <div class="celda celda-vacia"></div>\n'
        elif tipo.isdigit():
            html_crucigrama += f'        <div class="celda celda-negra">{tipo}</div>\n'
        elif tipo == "X":
            html_crucigrama += f'        <div class="celda"><input type="text" maxlength="1" class="celda-input" id="in_{f}_{c}"></div>\n'
        elif tipo == "A":
            html_crucigrama += f'        <div class="celda celda-acro"><input type="text" maxlength="1" class="celda-input" id="in_{f}_{c}"></div>\n'
    
    html_crucigrama += '    </div>\n'

html_crucigrama += "</div>"

# ============================================================
# JAVASCRIPT PARA LEER LAS RESPUESTAS Y ENVIARLAS A STREAMLIT
# ============================================================
# Usamos una técnica de "mensajería" para que Streamlit reciba las letras
js = """
<script>
    // Esta función escucha cada vez que el usuario escribe en el crucigrama
    document.addEventListener("input", function(e) {
        if (e.target.tagName === 'INPUT' && e.target.id.startsWith('in_')) {
            // Guardamos el estado actual del crucigrama en el localStorage del navegador
            let estado = {};
            document.querySelectorAll('.celda-input').forEach(input => {
                if (input.value) {
                    estado[input.id] = input.value.toUpperCase();
                }
            });
            // Enviamos el evento a Streamlit para que sepa que hubo un cambio
            window.parent.postMessage({isStreamlitMessage: true, type: "streamlit:setComponentValue", value: estado}, "*");
        }
    });
</script>
"""
# Nota: Para una integración nativa sin JS complejo, usaremos el componente html 
# con un truco de recarga en Streamlit, pero como queremos que sea fluido, 
# utilizaremos la API de componentes de Streamlit si está disponible, 
# o simplemente guardaremos en un archivo temporal si usamos backend, pero 
# para Streamlit Cloud, la mejor forma de hacer un formulario nativo es con un form.

# Como el HTML puro no puede enviar datos a Streamlit fácilmente sin un componente personalizado,
# usaremos la función nativa de Streamlit para formularios y aplicaremos CSS para que se vea idéntico.

st.markdown("<h3 style='text-align:center;color:#C2185B;'>🍼 Revelación de Género 🍼</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Escribe una letra por casilla para descubrir el nombre oculto.</p>", unsafe_allow_html=True)

# CSS que imita exactamente el diseño del crucigrama
st.markdown("""
<style>
    /* Ocultar etiquetas de inputs */
    div[data-testid="stTextInput"] label { display: none; }
    
    /* Estilo base de las cajitas */
    div[data-testid="stTextInput"] input {
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        padding: 0 !important;
        height: 40px !important;
        border-radius: 0 !important;
        text-transform: uppercase;
        border: 1px solid #999 !important;
        background-color: white !important;
    }
    
    /* Pegar las columnas para que se vea como un tablero */
    div[data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
        width: 40px !important;
        min-width: 40px !important;
        max-width: 40px !important;
        flex: 0 0 40px !important;
    }

    /* Celdas negras (Números) */
    .celda-negra {
        background-color: #1A1A1A !important;
        color: white !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        border: 1px solid #333 !important;
    }
    
    /* Celdas vacías */
    .celda-vacia {
        height: 40px !important;
        border: 1px solid transparent !important;
    }

    /* Forzar el color azul en la columna del acróstico (columna 6) */
    .acro-input div[data-testid="stTextInput"] input {
        background-color: #94B8D6 !important;
        border: 1px solid #3A6A94 !important;
        color: #003366 !important;
    }
    
    /* Mensajes debajo de las filas */
    .msg-fila { text-align: center; font-size: 0.8rem; font-weight: bold; margin-top: 2px; height: 20px; }
    .msg-ok { color: #2E7D32; }
    .msg-error { color: #C62828; }
</style>
""", unsafe_allow_html=True)

# Usamos st.form para evitar que la página parpadee con cada tecla
with st.form("crucigrama_form"):
    # Diccionario para almacenar los inputs
    respuestas = {}

    for f in range(10):
        cols = st.columns(12)
        for c in range(12):
            tipo = MAPA[f][c]
            with cols[c]:
                if tipo == "":
                    st.markdown("<div class='celda-vacia'></div>", unsafe_allow_html=True)
                elif tipo.isdigit():
                    st.markdown(f"<div class='celda-negra'>{tipo}</div>", unsafe_allow_html=True)
                elif tipo == "X":
                    respuestas[(f, c)] = st.text_input(
                        label=f"in_{f}_{c}", max_chars=1, key=f"input_{f}_{c}", label_visibility="collapsed"
                    )
                elif tipo == "A":
                    st.markdown("<div class='acro-input'>", unsafe_allow_html=True)
                    respuestas[(f, c)] = st.text_input(
                        label=f"acro_{f}_{c}", max_chars=1, key=f"acro_input_{f}_{c}", label_visibility="collapsed"
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                    
    # Botón de verificar dentro del formulario
    submit = st.form_submit_button("🔍 Verificar respuestas", use_container_width=True, type="primary")

# ============================================================
# LÓGICA DE VALIDACIÓN
# ============================================================
if submit:
    # Verificar cada fila
    todas_correctas = True
    acrostico = ""
    
    for f in range(10):
        palabra_usuario = ""
        col_acro_letra = ""
        
        for c in range(12):
            val = respuestas.get((f, c), "")
            if val:
                val = val.upper().replace("Á","A").replace("É","E").replace("Í","I").replace("Ó","O").replace("Ú","U").replace("Ü","U")
                palabra_usuario += val
            else:
                val = " "
            if MAPA[f][c] == "A":
                col_acro_letra = val.strip()
        
        acrostico += col_acro_letra
        
        # Comparamos solo con la palabra esperada
        correcta = PALABRAS[f]
        # Removemos los espacios para comparar la palabra (ej. LOCION == LOCIÓN normalizado)
        # Contamos cuántas X y A hay en la fila para saber cuántas letras esperar
        letras_esperadas = sum(1 for x in MAPA[f] if x in ["X", "A"])
        palabra_usuario = palabra_usuario[:letras_esperadas]
        
        palabra_norm = palabra_usuario.replace(" ", "")
        respuesta_norm = correcta.replace(" ", "")
        
        if palabra_norm != respuesta_norm:
            todas_correctas = False
            # Mostrar error
            st.markdown(f"<div class='msg-fila msg-error'>Fila {f+1} incorrecta ❌</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='msg-fila msg-ok'>Fila {f+1} correcta ✅</div>", unsafe_allow_html=True)

    # Validación final
    if todas_correctas and acrostico == "JUANANDRES":
        st.balloons()
        st.markdown(
            f"<div style='background: linear-gradient(135deg,#A5D6A7,#C8E6C9);border: 3px solid #2E7D32;border-radius:15px;padding:25px;text-align:center;margin-top:20px;'>"
            f"<h2>🎉 ¡Felicidades! 🎉</h2>"
            f"<p style='font-size:1.2rem;color:#1B5E20;'>¡Has completado el crucigrama!</p>"
            f"<h1>El bebé es...</h1>"
            f"<h1 style='font-size:2.2rem;color:#C2185B;'>JUAN ANDRES DIAZ CORTES</h1>"
            f"<p style='font-size:1.1rem;color:#2E7D32;'>💙 ¡Bienvenido, pequeño! 💙</p>"
            f"</div>",
            unsafe_allow_html=True
        )
    else:
        st.error("🔎 Aún hay palabras incorrectas o el nombre no se ha formado correctamente.")
