import streamlit as st

# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(page_title="Revelación de Género", page_icon="🍼", layout="centered")

# ============================================================
# DATOS DEL ACROSTICO
# Cada entrada: (respuesta_correcta, índice_de_letra_del_acrostico)
# La letra del acróstico es respuesta[idx]
# ============================================================
PALABRAS = [
    ("PIJAMA",  2),  # J  -> PIJAMA[2]  = J
    ("JUGUETE", 1),  # U  -> JUGUETE[1] = U
    ("CAMA",    1),  # A  -> CAMA[1]    = A
    ("LOCIÓN",  5),  # N  -> LOCIÓN[5]  = N
    ("MAMÁ",    1),  # A  -> MAMÁ[1]    = A
    ("MANTA",   2),  # N  -> MANTA[2]   = N
    ("DIENTE",  0),  # D  -> DIENTE[0]  = D
    ("ARRULLO", 2),  # R  -> ARRULLO[2] = R
    ("PAÑALES", 5),  # E  -> PAÑALES[5] = E
    ("SILLA",   0),  # S  -> SILLA[0]   = S
]

NOMBRE_ACROSTICO = "JUAN ANDRES"
NOMBRE_BEBE = "JUAN ANDRES DIAZ CORTES"
LETRA_ACROSTICO_POS = [idx for (_, idx) in PALABRAS]
MAX_LEN = max(len(p) for p, _ in PALABRAS)

# ============================================================
# ESTADO INICIAL
# ============================================================
if "respuestas" not in st.session_state:
    st.session_state.respuestas = [""] * len(PALABRAS)
if "verificado" not in st.session_state:
    st.session_state.verificado = False

# ============================================================
# ESTILOS
# ============================================================
st.markdown("""
<style>
    .titulo { text-align:center; color:#C2185B; }
    .subtitulo { text-align:center; color:#7B1FA2; font-size:1.1rem; }
    .stTextInput input { text-align:center; font-weight:bold; letter-spacing:2px; }
    .exito {
        background: linear-gradient(135deg,#A5D6A7,#C8E6C9);
        border: 3px solid #2E7D32; border-radius:15px;
        padding:25px; text-align:center; margin-top:20px;
    }
    .exito h2 { color:#1B5E20; margin:5px; }
    .exito h1 { color:#C2185B; margin:10px; letter-spacing:4px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='titulo'>🍼 Revelación de Género 🍼</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitulo'>Descubre el nombre del bebé completando el acróstico. "
            "Cada palabra empieza con la letra que se forma en la columna resaltada.</p>",
            unsafe_allow_html=True)
st.write("")

# ============================================================
# FUNCIÓN PARA VALIDAR UNA PALABRA
# ============================================================
def normalizar(s):
    return s.strip().upper().replace("Á","A").replace("É","E").replace("Í","I")\
            .replace("Ó","O").replace("Ú","U").replace("Ü","U")

def es_correcta(i):
    return normalizar(st.session_state.respuestas[i]) == PALABRAS[i][0]

# ============================================================
# RENDER DE CADA FILA
# ============================================================
for i, (correcta, idx_letra) in enumerate(PALABRAS):
    cols = st.columns([1, 4])

    # Numeración
    with cols[0]:
        st.markdown(
            f"<div style='background:#F3E5F5;border:2px solid #7B1FA2;"
            f"border-radius:10px;padding:8px;text-align:center;"
            f"font-weight:bold;font-size:1.2rem;color:#4A148C;margin-top:6px;'>"
            f"{i+1}</div>",
            unsafe_allow_html=True)

    # Campo de texto
    with cols[1]:
        valor = st.text_input(
            label=f"Pregunta {i+1}",
            value=st.session_state.respuestas[i],
            max_chars=MAX_LEN,
            key=f"input_{i}",
            label_visibility="collapsed",
            placeholder="Escribe la palabra...",
        )
        if valor != st.session_state.respuestas[i]:
            st.session_state.respuestas[i] = valor
            st.session_state.verificado = False

        # Colorear el campo: verde si correcto, rojo si incorrecto
        if valor.strip():
            if es_correcta(i):
                st.markdown(
                    f"<style>div[data-testid='stTextInput'] input {{}}</style>",
                    unsafe_allow_html=True)
                st.markdown(
                    f"<div style='color:#2E7D32;font-weight:bold;"
                    f"margin-top:-12px;'>✅ Correcto</div>",
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<div style='color:#C62828;font-weight:bold;"
                    f"margin-top:-12px;'>❌ Revisa la palabra</div>",
                    unsafe_allow_html=True)

st.write("")

# ============================================================
# BOTÓN VERIFICAR
# ============================================================
if st.button("🔍 Verificar respuestas", use_container_width=True, type="primary"):
    st.session_state.verificado = True

# ============================================================
# MOSTRAR ACROSTICO FORMADO (columna resaltada)
# ============================================================
st.markdown("---")
st.markdown("<h3 style='text-align:center;color:#7B1FA2;'>"
            "🌟 Columna del acróstico 🌟</h3>", unsafe_allow_html=True)

letras_formadas = []
for i, (correcta, idx_letra) in enumerate(PALABRAS):
    palabra_norm = normalizar(st.session_state.respuestas[i])
    if len(palabra_norm) > idx_letra:
        letras_formadas.append(palabra_norm[idx_letra])
    else:
        letras_formadas.append("?")

cols_acr = st.columns(len(PALABRAS))
for i, letra in enumerate(letras_formadas):
    with cols_acr[i]:
        color_fondo = "#FCE4EC" if letra != "?" else "#EEEEEE"
        color_texto = "#C2185B" if letra != "?" else "#9E9E9E"
        st.markdown(
            f"<div style='background:{color_fondo};border:2px solid #C2185B;"
            f"border-radius:10px;padding:12px;text-align:center;"
            f"font-weight:bold;font-size:1.5rem;color:{color_texto};'>"
            f"{letra}</div>",
            unsafe_allow_html=True)

st.write("")

# ============================================================
# VALIDACIÓN FINAL
# ============================================================
todas_correctas = all(es_correcta(i) for i in range(len(PALABRAS)))
acrostico_correcto = "".join(letras_formadas).replace(" ", "").replace("?", "") == "JUANANDRES"

if st.session_state.verificado and todas_correctas and acrostico_correcto:
    st.balloons()
    st.markdown(
        f"<div class='exito'>"
        f"<h2>🎉 ¡Felicidades! 🎉</h2>"
        f"<p style='font-size:1.2rem;color:#1B5E20;'>"
        f"¡Has completado el acróstico correctamente!</p>"
        f"<h1>El bebé es...</h1>"
        f"<h1 style='font-size:2.2rem;'>{NOMBRE_BEBE}</h1>"
        f"<p style='font-size:1.1rem;color:#2E7D32;'>💙 ¡Bienvenido, pequeño! 💙</p>"
        f"</div>",
        unsafe_allow_html=True)
elif st.session_state.verificado and not todas_correctas:
    st.info("🔎 Aún hay palabras incorrectas. ¡Sigue intentando!")
