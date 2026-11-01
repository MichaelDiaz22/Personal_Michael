import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Revelación de Género", page_icon="🍼", layout="centered")

# ============================================================
# DEFINICIÓN DEL CRUCIGRAMA (Igual a tu imagen)
# ============================================================
# (respuesta_correcta, fila, columna_inicio, columna_acrostico)
PALABRAS = [
    ("PIJAMA",  0, 2, 6),
    ("JUGUETE", 1, 2, 6),
    ("CAMA",    2, 1, 6),
    ("LOCIÓN",  3, 2, 6),
    ("MAMÁ",    4, 2, 6),
    ("MANTA",   5, 2, 6),
    ("DIENTE",  6, 0, 6),
    ("ARRULLO", 7, 2, 6),
    ("PAÑALES", 8, 2, 6),
    ("SILLA",   9, 2, 6),
]

# Construimos la matriz del tablero (10 filas x 10 columnas)
FILAS = 10
COLUMNAS = 10
tablero = [["" for _ in range(COLUMNAS)] for _ in range(FILAS)]

# Llenamos la matriz con los datos visuales (Número, Letra, Acróstico)
for i, (palabra, fila, col_inicio, col_acro) in enumerate(PALABRAS):
    # Ponemos el número en la primera celda de la palabra
    tablero[fila][col_inicio] = str(i + 1)
    
    # Llenamos las letras de la palabra
    for j, letra in enumerate(palabra):
        col_actual = col_inicio + j
        if col_actual == col_acro:
            tablero[fila][col_actual] = "A" # Celda del acróstico (Azul)
        else:
            # Si la celda ya tiene un número (porque otra palabra cruzó primero), no lo borramos
            if not tablero[fila][col_actual].isdigit():
                tablero[fila][col_actual] = "X" # Celda normal (Blanca)

# Convertimos la matriz a un formato JSON para pasarla a JavaScript
import json
tablero_json = json.dumps(tablero)
palabras_json = json.dumps([p[0] for p in PALABRAS])

# ============================================================
# COMPONENTE HTML / CSS / JAVASCRIPT
# ============================================================
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: transparent;
        margin: 0;
        padding: 10px;
    }}
    .grid {{
        display: grid;
        grid-template-columns: repeat({COLUMNAS}, 42px);
        grid-template-rows: repeat({FILAS}, 42px);
        gap: 0;
        border: 2px solid #333;
        background-color: #fff;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    .cell {{
        width: 42px;
        height: 42px;
        box-sizing: border-box;
        border: 1px solid #999;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }}
    .cell.empty {{
        border: 1px solid transparent;
        background-color: transparent;
    }}
    .cell.black {{
        background-color: #1A1A1A;
        color: white;
        border: 1px solid #333;
        font-weight: bold;
        font-size: 16px;
    }}
    .cell.blue {{
        background-color: #94B8D6;
        border: 1px solid #3A6A94;
    }}
    input {{
        width: 100%;
        height: 100%;
        border: none;
        background: transparent;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        text-transform: uppercase;
        color: #000;
        outline: none;
        padding: 0;
        caret-color: transparent; /* Ocultar cursor para que parezca tablero */
    }}
    .cell.blue input {{
        color: #003366;
    }}
    /* Botón de verificar */
    button {{
        background-color: #FF4B4B;
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        cursor: pointer;
        width: 100%;
        max-width: 400px;
        transition: background 0.3s;
    }}
    button:hover {{
        background-color: #E03C3C;
    }}
    /* Modal de éxito */
    .modal {{
        display: none;
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.6);
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }}
    .modal-content {{
        background: linear-gradient(135deg,#A5D6A7,#C8E6C9);
        border: 4px solid #2E7D32;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        max-width: 500px;
        animation: pop 0.5s ease-out;
    }}
    @keyframes pop {{
        0% {{ transform: scale(0.5); opacity: 0; }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    .modal h1 {{ color: #1B5E20; margin: 10px 0; }}
    .modal h2 {{ color: #C2185B; font-size: 2.5rem; margin: 20px 0; letter-spacing: 2px; }}
    .error-msg {{
        color: #C62828;
        font-weight: bold;
        margin-bottom: 15px;
        min-height: 20px;
        text-align: center;
    }}
</style>
</head>
<body>

<div id="error-msg" class="error-msg"></div>
<div class="grid" id="grid"></div>
<button onclick="verificar()">🔍 Verificar respuestas</button>

<div class="modal" id="modal-exito">
    <div class="modal-content">
        <h1>🎉 ¡Felicidades! 🎉</h1>
        <p>¡Has completado el crucigrama!</p>
        <h2>JUAN ANDRES DIAZ CORTES</h2>
        <p>💙 ¡Bienvenido, pequeño! 💙</p>
    </div>
</div>

<script>
    const tablero = {tablero_json};
    const respuestasCorrectas = {palabras_json};
    const filas = {FILAS};
    const columnas = {COLUMNAS};
    const colAcro = 6;

    const grid = document.getElementById('grid');
    const inputs = [];

    // Dibujar el tablero
    for (let r = 0; r < filas; r++) {{
        inputs[r] = [];
        for (let c = 0; c < columnas; c++) {{
            const val = tablero[r][c];
            const cell = document.createElement('div');
            cell.className = 'cell';
            
            if (val === "") {{
                cell.classList.add('empty');
            }} else if (!isNaN(val) && val !== "") {{
                cell.classList.add('black');
                cell.innerText = val;
            }} else {{
                if (c === colAcro) cell.classList.add('blue');
                
                const input = document.createElement('input');
                input.type = 'text';
                input.maxLength = 1;
                input.dataset.row = r;
                input.dataset.col = c;
                
                // Evento para saltar a la siguiente casilla de la misma palabra
                input.addEventListener('input', (e) => {{
                    e.target.value = e.target.value.toUpperCase();
                    if (e.target.value.length === 1) {{
                        // Buscar la siguiente casilla en la misma fila que no sea negra ni vacía
                        let nextC = parseInt(e.target.dataset.col) + 1;
                        if (nextC < columnas && inputs[r][nextC]) {{
                            inputs[r][nextC].focus();
                        }}
                    }}
                }});
                
                // Borrar hacia atrás
                input.addEventListener('keydown', (e) => {{
                    if (e.key === 'Backspace' && e.target.value === '') {{
                        let prevC = parseInt(e.target.dataset.col) - 1;
                        if (prevC >= 0 && inputs[r][prevC]) {{
                            inputs[r][prevC].focus();
                        }}
                    }}
                }});

                cell.appendChild(input);
                inputs[r][c] = input;
            }}
            grid.appendChild(cell);
        }}
    }}

    // Función Verificar
    function verificar() {{
        let todoCorrecto = true;
        let acrostico = "";
        const errorDiv = document.getElementById('error-msg');
        
        // Recorrer cada palabra
        for (let i = 0; i < respuestasCorrectas.length; i++) {{
            let palabraFormada = "";
            let filaActual = i; // Como están en orden, la fila i corresponde a la palabra i
            let letraAcro = "";
            
            for (let c = 0; c < columnas; c++) {{
                if (inputs[filaActual][c]) {{
                    let val = inputs[filaActual][c].value || " ";
                    palabraFormada += val;
                    if (c === colAcro) letraAcro = val;
                }}
            }}
            
            acrostico += letraAcro;
            
            // Normalizar (quitar tildes para comparar)
            let pForm = palabraFormada.replace(/ /g, "").normalize("NFD").replace(/[\u0300-\u036f]/g, "");
            let pCorr = respuestasCorrectas[i].normalize("NFD").replace(/[\u0300-\u036f]/g, "");
            
            if (pForm !== pCorr) {{
                todoCorrecto = false;
                // Pintar de rojo las celdas de esta palabra
                for (let c = 0; c < columnas; c++) {{
                    if (inputs[filaActual][c]) inputs[filaActual][c].parentElement.style.backgroundColor = "#ffcccc";
                }}
            }} else {{
                // Pintar de verde si está bien
                for (let c = 0; c < columnas; c++) {{
                    if (inputs[filaActual][c]) inputs[filaActual][c].parentElement.style.backgroundColor = "#d4edda";
                }}
            }}
        }}
        
        let acroForm = acrostico.replace(/ /g, "");
        if (todoCorrecto && acroForm === "JUANANDRES") {{
            errorDiv.innerText = "";
            document.getElementById('modal-exito').style.display = 'flex';
        }} else {{
            errorDiv.innerText = "Hay palabras incorrectas o el nombre no se ha formado. Revisa las casillas rojas.";
        }}
    }}
</script>
</body>
</html>
"""

# Renderizar el componente
components.html(html_code, height=650, scrolling=False)
