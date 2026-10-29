import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Revelación de Género",
    page_icon="👶",
    layout="centered"
)

if "reset_seed" not in st.session_state:
    st.session_state.reset_seed = 0

st.markdown("""
<style>
  .main-title {
    text-align: center;
    font-size: 2.2rem;
    background: linear-gradient(90deg, #2a4d8f, #c2185b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
  }
  .subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 1rem;
  }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎀 Revelación de Género 💙</div>',
            unsafe_allow_html=True)
st.markdown('<div class="subtitle">Encuentra las parejas para descubrir la sorpresa</div>',
            unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔄 Reiniciar juego", use_container_width=True):
        st.session_state.reset_seed += 1
        st.rerun()

SEED = st.session_state.reset_seed


# ============================================================
# MEMORAMA MIXTO + ENLACE A REVELACIÓN EXTERNA
# ============================================================
def juego_memorama():
    memory_html = f"""
    <!-- seed:{SEED} -->
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      html, body {{
        margin: 0; padding: 0;
        font-family: sans-serif;
        background: #fff;
        width: 100%;
        overflow-x: hidden;
      }}
      body {{
        display: flex; flex-direction: column; align-items: center;
        padding: 6px 4px;
        box-sizing: border-box;
      }}

      #game {{
        display: flex; flex-direction: column; align-items: center;
        width: 100%;
        transition: opacity .6s;
      }}
      #game.hide {{ opacity: 0; pointer-events: none; height: 0; overflow: hidden; }}

      #info {{
        margin-top: 6px;
        color: #6a5acd;
        font-size: min(14px, 3.5vw);
        font-weight: 600;
      }}
      #grid {{
        display: grid;
        grid-template-columns: repeat(6, min(62px, 14vw));
        grid-template-rows: repeat(5, min(62px, 14vw));
        gap: min(8px, 1.6vw);
        justify-content: center;
        width: 100%;
        max-width: 100%;
      }}
      .card {{
        width: 100%; height: 100%;
        perspective: 600px; cursor: pointer;
      }}
      .inner {{
        position: relative; width: 100%; height: 100%;
        transition: transform .4s; transform-style: preserve-3d;
      }}
      .card.flipped .inner,
      .card.matched .inner {{ transform: rotateY(180deg); }}

      .face, .back {{
        position: absolute; inset: 0; border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: min(30px, 7vw);
        backface-visibility: hidden;
        -webkit-backface-visibility: hidden;
      }}
      /* Carta boca abajo: gradiente AZUL → ROSA (neutro) */
      .face {{
        background: linear-gradient(135deg,#cfe4ff 0%, #ffd1e3 100%);
        color: #fff;
        font-size: min(22px, 5vw);
        box-shadow: 0 2px 6px rgba(100,100,150,.18);
      }}
      .back {{
        background: #fff;
        border: 2px solid #d4c5f0;
        transform: rotateY(180deg);
      }}
      .card.matched .back {{
        border-color: #b8a4d6;
        background: linear-gradient(135deg, #eef5ff 0%, #fff0f7 100%);
        animation: matchPulse .5s ease-out;
      }}
      @keyframes matchPulse {{
        0%   {{ transform: rotateY(180deg) scale(1); }}
        50%  {{ transform: rotateY(180deg) scale(1.08); }}
        100% {{ transform: rotateY(180deg) scale(1); }}
      }}

      #msg {{
        margin-top: 14px; font-size: min(20px, 5vw); color: #6a5acd;
        min-height: 30px; text-align: center; font-weight: bold;
      }}
      #resetBtn {{
        margin-top: 12px; padding: 8px 22px;
        border: 1px solid #999;
        background: #fff;
        cursor: pointer; border-radius: 6px;
        font-size: min(14px, 3.6vw);
      }}

      /* ---------- RECUADRO CON ENLACE A REVELACIÓN ---------- */
      #reveal {{
        display: none;
        flex-direction: column; align-items: center;
        margin-top: 10px;
        padding: 30px 32px;
        border-radius: 20px;
        background: linear-gradient(135deg, #cfe4ff 0%, #ffd1e3 100%);
        box-shadow: 0 12px 40px rgba(106,90,205,.3);
        animation: revealIn .8s cubic-bezier(.2,1.5,.4,1);
        text-align: center;
        max-width: min(480px, 92vw);
        box-sizing: border-box;
      }}
      #reveal.show {{ display: flex; }}
      @keyframes revealIn {{
        0%   {{ opacity: 0; transform: scale(0.6); }}
        60%  {{ opacity: 1; transform: scale(1.06); }}
        100% {{ opacity: 1; transform: scale(1); }}
      }}
      #revealEmoji {{
        font-size: min(70px, 18vw);
        line-height: 1;
        animation: floatUpDown 1.6s ease-in-out infinite;
      }}
      @keyframes floatUpDown {{
        0%, 100% {{ transform: translateY(0); }}
        50%      {{ transform: translateY(-10px); }}
      }}
      #revealTitle {{
        font-size: min(26px, 6.5vw);
        font-weight: 900;
        margin-top: 10px;
        color: #4a3a8f;
        letter-spacing: .5px;
      }}
      #revealSub {{
        margin-top: 8px;
        font-size: min(15px, 3.8vw);
        color: #5a4a9f;
        font-weight: 500;
        line-height: 1.4;
      }}
      #revealLink {{
        display: inline-block;
        margin-top: 18px;
        padding: 12px 28px;
        border: none;
        background: linear-gradient(90deg, #2a4d8f, #c2185b);
        color: #fff;
        border-radius: 30px;
        cursor: pointer;
        font-size: min(16px, 4vw);
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(106,90,205,.4);
        text-decoration: none;
        transition: transform .15s;
      }}
      #revealLink:hover {{ transform: scale(1.05); }}
      #replayBtn {{
        margin-top: 14px;
        padding: 8px 22px;
        border: 1px solid #999;
        background: #fff;
        color: #555;
        border-radius: 6px;
        cursor: pointer;
        font-size: min(13px, 3.4vw);
      }}
    </style>
    </head>
    <body>

      <!-- MEMORAMA -->
      <div id="game">
        <div id="info">Parejas encontradas: <span id="pairs">0</span> / 15</div>
        <div id="grid"></div>
        <div id="msg"></div>
        <button id="resetBtn" onclick="reset()">🔄 Reiniciar</button>
      </div>

      <!-- RECUADRO CON ENLACE A LA REVELACIÓN -->
      <div id="reveal">
        <div id="revealEmoji">🎁</div>
        <div id="revealTitle">¡Completaste el memorama!</div>
        <div id="revealSub">
          Haz clic en el botón para descubrir<br>
          la revelación de género del bebé 💙🎀
        </div>
        <a id="revealLink"
           href="https://drive.google.com/drive/u/0/folders/1e5KHCM0RWav939qaWnXrFyUGS6c2v9go"
           target="_blank"
           rel="noopener noreferrer">
          🎬 Ver revelación
        </a>
        <button id="replayBtn" onclick="reset()">🔄 Jugar de nuevo</button>
      </div>

    <script>
      // ---------- 15 PAREJAS MIXTAS (niño + niña + bebé) ----------
      const ICONS = [
        // Cosas de niño
        '🚗','⚽','🦖','🚀','🎮',
        // Cosas de niña
        '🎀','🌸','👗','🦄','💖',
        // Neutros / bebé
        '🧸','👶','🍼','🎈','☁️'
      ];

      let first = null, lock = false, matched = 0, celebrated = false;
      let lastLayout = '';

      const grid = document.getElementById('grid');
      const msg = document.getElementById('msg');
      const pairsEl = document.getElementById('pairs');
      const gameEl = document.getElementById('game');
      const revealEl = document.getElementById('reveal');

      function randInt(max) {{
        const buf = new Uint32Array(1);
        crypto.getRandomValues(buf);
        return buf[0] % max;
      }}

      function shuffle(arr) {{
        const a = arr.slice();
        for (let i = a.length - 1; i > 0; i--) {{
          const j = randInt(i + 1);
          [a[i], a[j]] = [a[j], a[i]];
        }}
        return a;
      }}

      function generateLayout() {{
        let attempt = 0;
        let cards;
        do {{
          const doubled = [];
          ICONS.forEach(icon => {{
            doubled.push(icon);
            doubled.push(icon);
          }});
          cards = shuffle(doubled);
          const fingerprint = cards.join('|');
          if (fingerprint !== lastLayout) {{
            lastLayout = fingerprint;
            break;
          }}
          attempt++;
        }} while (attempt < 5);
        return cards;
      }}

      function build() {{
        grid.innerHTML = '';
        msg.innerHTML = '';
        matched = 0; first = null; lock = false; celebrated = false;
        pairsEl.textContent = '0';

        const cards = generateLayout();
        cards.forEach((icon, index) => {{
          const c = document.createElement('div');
          c.className = 'card';
          c.dataset.icon = icon;
          c.dataset.pos = index;
          c.innerHTML = `<div class="inner">
              <div class="face">?</div>
              <div class="back">${{icon}}</div>
            </div>`;
          c.onclick = () => flip(c);
          grid.appendChild(c);
        }});
      }}

      function flip(card) {{
        if (lock || card.classList.contains('flipped') ||
            card.classList.contains('matched')) return;
        card.classList.add('flipped');
        if (!first) {{ first = card; return; }}
        if (first.dataset.icon === card.dataset.icon) {{
          first.classList.add('matched');
          card.classList.add('matched');
          matched++; first = null;
          pairsEl.textContent = matched;
          if (matched === 15 && !celebrated) {{
            celebrated = true;
            msg.innerHTML = '🎉 ¡Completaste todas las parejas!';
            setTimeout(showReveal, 900);
          }}
        }} else {{
          lock = true;
          setTimeout(() => {{
            first.classList.remove('flipped');
            card.classList.remove('flipped');
            first = null; lock = false;
          }}, 700);
        }}
      }}

      function showReveal() {{
        gameEl.classList.add('hide');
        revealEl.classList.add('show');
      }}

      function reset() {{
        gameEl.classList.remove('hide');
        revealEl.classList.remove('show');
        build();
      }}

      // Init
      build();
    </script>
    </body>
    </html>
    """
    components.html(memory_html, height=620)


# ============================================================
# APP PRINCIPAL
# ============================================================
st.markdown("### 🃏 Memorama")

juego_memorama()

st.markdown("---")
st.caption("💙 Hecho con amor 🎀")
