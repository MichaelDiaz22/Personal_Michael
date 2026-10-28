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
# ANIMACIÓN DE REVELACIÓN (azul, niño)
# ============================================================
CELEBRATION_SCRIPT = """
<script>
  function celebrate() {
    const overlay = document.createElement('div');
    overlay.style.cssText = `
      position: fixed; inset: 0; z-index: 9998;
      background: radial-gradient(circle, rgba(207,228,255,.92) 0%,
                  rgba(155,190,255,.92) 100%);
      animation: flashFade 1.1s ease-out forwards;
      pointer-events: none;
    `;
    document.body.appendChild(overlay);
    setTimeout(() => overlay.remove(), 1200);

    const EMOJIS = ['🎉','💙','🩵','⭐','✨','🚀','🚗','⚽','👶','🎈'];
    const N = 70;
    for (let i = 0; i < N; i++) {
      const p = document.createElement('div');
      const emoji = EMOJIS[Math.floor(Math.random() * EMOJIS.length)];
      p.textContent = emoji;
      const startX = 50 + (Math.random() - 0.5) * 30;
      const startY = 50 + (Math.random() - 0.5) * 20;
      const dx = (Math.random() - 0.5) * 140;
      const dy = (Math.random() - 0.5) * 140;
      const rot = Math.random() * 720 - 360;
      const size = 16 + Math.random() * 22;
      const delay = Math.random() * 0.25;
      p.style.cssText = `
        position: fixed; z-index: 9999; pointer-events: none;
        left: ${startX}%; top: ${startY}%;
        font-size: ${size}px;
        transform: translate(-50%, -50%);
        opacity: 0;
        animation: burst 1.6s ease-out ${delay}s forwards;
        --dx: ${dx}vw; --dy: ${dy}vh; --rot: ${rot}deg;
      `;
      document.body.appendChild(p);
      setTimeout(() => p.remove(), 2200);
    }

    const msg = document.createElement('div');
    msg.innerHTML = `
      <div style="font-size: 70px; line-height: 1;">💙</div>
      <div style="font-size: 44px; font-weight: 900;
                  background: linear-gradient(90deg,#2a4d8f,#4c6ef5);
                  -webkit-background-clip: text;
                  -webkit-text-fill-color: transparent;
                  margin-top: 4px;">¡Es un niño!</div>
    `;
    msg.style.cssText = `
      position: fixed; z-index: 10000; pointer-events: none;
      left: 50%; top: 50%; transform: translate(-50%, -50%) scale(0);
      text-align: center; font-family: sans-serif;
      background: rgba(255,255,255,.95);
      padding: 30px 48px; border-radius: 24px;
      box-shadow: 0 20px 60px rgba(42,77,143,.45);
      animation: revealPop 1.4s cubic-bezier(.2,1.5,.4,1) forwards;
    `;
    document.body.appendChild(msg);
    setTimeout(() => {
      msg.style.transition = 'opacity .6s';
      msg.style.opacity = '0';
      setTimeout(() => msg.remove(), 700);
    }, 3500);
  }
</script>

<style>
  @keyframes flashFade {
    0% { opacity: 0; }
    25% { opacity: 1; }
    100% { opacity: 0; }
  }
  @keyframes burst {
    0% {
      opacity: 0;
      transform: translate(-50%, -50%) scale(0.3) rotate(0);
    }
    15% { opacity: 1; }
    100% {
      opacity: 0;
      transform: translate(calc(-50% + var(--dx)), calc(-50% + var(--dy)))
                 scale(1) rotate(var(--rot));
    }
  }
  @keyframes revealPop {
    0%   { transform: translate(-50%, -50%) scale(0) rotate(-15deg); }
    55%  { transform: translate(-50%, -50%) scale(1.15) rotate(4deg); }
    75%  { transform: translate(-50%, -50%) scale(0.95) rotate(-2deg); }
    100% { transform: translate(-50%, -50%) scale(1) rotate(0); }
  }
</style>
"""


# ============================================================
# MEMORAMA MIXTO CON REVELACIÓN DIRECTA
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
      /* Pareja encontrada: borde lila suave + fondo mixto */
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

      /* ---------- REVELACIÓN INLINE (reemplaza al tragamonedas) ---------- */
      #reveal {{
        display: none;
        flex-direction: column; align-items: center;
        margin-top: 10px;
        padding: 30px 40px;
        border-radius: 20px;
        background: linear-gradient(135deg, #cfe4ff 0%, #9bbfff 100%);
        box-shadow: 0 12px 40px rgba(42,77,143,.35);
        animation: revealIn .8s cubic-bezier(.2,1.5,.4,1);
        text-align: center;
      }}
      #reveal.show {{ display: flex; }}
      @keyframes revealIn {{
        0%   {{ opacity: 0; transform: scale(0.5) rotate(-10deg); }}
        60%  {{ opacity: 1; transform: scale(1.1) rotate(3deg); }}
        100% {{ opacity: 1; transform: scale(1) rotate(0); }}
      }}
      #revealEmoji {{
        font-size: min(80px, 20vw);
        line-height: 1;
        animation: floatUpDown 1.6s ease-in-out infinite;
      }}
      @keyframes floatUpDown {{
        0%, 100% {{ transform: translateY(0); }}
        50%      {{ transform: translateY(-12px); }}
      }}
      #revealTitle {{
        font-size: min(46px, 11vw);
        font-weight: 900;
        margin-top: 8px;
        background: linear-gradient(90deg, #2a4d8f, #4c6ef5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
      }}
      #revealSub {{
        margin-top: 6px;
        font-size: min(18px, 4.5vw);
        color: #2a4d8f;
        font-weight: 600;
        opacity: .85;
      }}
      #replayBtn {{
        margin-top: 18px;
        padding: 10px 26px;
        border: none;
        background: linear-gradient(90deg, #2a4d8f, #4c6ef5);
        color: #fff;
        border-radius: 30px;
        cursor: pointer;
        font-size: min(15px, 3.8vw);
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(42,77,143,.4);
      }}
      #replayBtn:hover {{ transform: scale(1.05); }}
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

      <!-- REVELACIÓN DIRECTA -->
      <div id="reveal">
        <div id="revealEmoji">👶</div>
        <div id="revealTitle">¡Es un niño!</div>
        <div id="revealSub">¡Felicidades! 💙</div>
        <button id="replayBtn" onclick="reset()">🔄 Jugar de nuevo</button>
      </div>

    {CELEBRATION_SCRIPT}

    <script>
      // ---------- 15 PAREJAS MIXTAS (niño + niña + bebé) ----------
      // Sin duplicados, sin dos corazones azules
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
        setTimeout(() => celebrate(), 400);
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
