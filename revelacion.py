import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Revelación de Género",
    page_icon="🎀",
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
# ANIMACIÓN DE REVELACIÓN (compartida)
# ============================================================
CELEBRATION_SCRIPT = """
<script>
  function celebrate() {
    const overlay = document.createElement('div');
    overlay.style.cssText = `
      position: fixed; inset: 0; z-index: 9998;
      background: radial-gradient(circle, rgba(255,209,227,.85) 0%,
                  rgba(207,228,255,.85) 100%);
      animation: flashFade 1.1s ease-out forwards;
      pointer-events: none;
    `;
    document.body.appendChild(overlay);
    setTimeout(() => overlay.remove(), 1200);

    const EMOJIS = ['🎉','🎀','💙','💗','⭐','✨','🌸','👶','🎈','💖'];
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
      <div style="font-size: 70px; line-height: 1;">🎀</div>
      <div style="font-size: 44px; font-weight: 900;
                  background: linear-gradient(90deg,#c2185b,#2a4d8f);
                  -webkit-background-clip: text;
                  -webkit-text-fill-color: transparent;
                  margin-top: 4px;">¡Es una niña!</div>
      <div style="font-size: 34px; color: #2a4d8f; font-weight: 700;
                  margin-top: 2px;">Amelia</div>
    `;
    msg.style.cssText = `
      position: fixed; z-index: 10000; pointer-events: none;
      left: 50%; top: 50%; transform: translate(-50%, -50%) scale(0);
      text-align: center; font-family: sans-serif;
      background: rgba(255,255,255,.92);
      padding: 30px 48px; border-radius: 24px;
      box-shadow: 0 20px 60px rgba(194,24,91,.35);
      animation: revealPop 1.4s cubic-bezier(.2,1.5,.4,1) forwards;
    `;
    document.body.appendChild(msg);
    setTimeout(() => {
      msg.style.transition = 'opacity .6s';
      msg.style.opacity = '0';
      setTimeout(() => msg.remove(), 700);
    }, 3200);
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
# MEMORAMA + TRAGAMONEDAS DE LETRAS (AMELIA)
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

      /* ---------- MEMORAMA ---------- */
      #game {{
        display: flex; flex-direction: column; align-items: center;
        width: 100%;
        transition: opacity .6s;
      }}
      #game.hide {{ opacity: 0; pointer-events: none; height: 0; overflow: hidden; }}
      #info {{
        margin-top: 6px;
        color: #666;
        font-size: min(14px, 3.5vw);
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
      .face {{
        background: linear-gradient(135deg,#cfe4ff,#ffd1e3);
        color: #fff;
        font-size: min(22px, 5vw);
      }}
      .back {{
        background: #fff; border: 2px solid #cfe4ff;
        transform: rotateY(180deg);
      }}
      .card.matched .back {{ border-color: #ffb3d1; background: #fff0f7; }}
      #msg {{
        margin-top: 14px; font-size: min(20px, 5vw); color: #c2185b;
        min-height: 30px; text-align: center; font-weight: bold;
      }}
      #resetBtn {{
        margin-top: 12px; padding: 8px 22px; border: 1px solid #999;
        background: #fff; cursor: pointer; border-radius: 6px;
        font-size: min(14px, 3.6vw);
      }}

      /* ---------- TRAGAMONEDAS ---------- */
      #slot {{
        display: none;
        flex-direction: column; align-items: center;
        margin-top: 10px;
        animation: fadeIn .6s ease-out;
      }}
      #slot.show {{ display: flex; }}
      @keyframes fadeIn {{
        0% {{ opacity: 0; transform: translateY(20px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}
      #slotTitle {{
        color: #c2185b;
        font-weight: bold;
        font-size: min(20px, 5vw);
        text-align: center;
        margin-bottom: 12px;
      }}
      #reels {{
        display: flex; gap: min(10px, 2vw);
        background: #2a2a2a;
        padding: min(14px, 3vw);
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,.2);
      }}
      .reel {{
        width: min(60px, 13vw);
        height: min(80px, 18vw);
        background: linear-gradient(180deg, #fff 0%, #f0f4ff 50%, #fff 100%);
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: min(40px, 9vw);
        font-weight: 900;
        color: #c2185b;
        box-shadow: inset 0 4px 10px rgba(0,0,0,.15);
        overflow: hidden;
        position: relative;
        font-family: sans-serif;
        letter-spacing: 1px;
      }}
      .reel.spinning {{
        animation: spinBlur 0.12s linear infinite;
      }}
      @keyframes spinBlur {{
        0% {{ transform: translateY(-15%); filter: blur(2px); }}
        50% {{ transform: translateY(15%); filter: blur(3px); }}
        100% {{ transform: translateY(-15%); filter: blur(2px); }}
      }}
      .reel.win {{
        background: linear-gradient(180deg, #ffd1e3, #ff6b9d 50%, #ffd1e3);
        color: #fff;
        box-shadow: inset 0 4px 10px rgba(0,0,0,.15),
                    0 0 25px rgba(255,107,157,.9);
        animation: winPulse .8s ease-out;
      }}
      @keyframes winPulse {{
        0%   {{ transform: scale(1); }}
        40%  {{ transform: scale(1.15); }}
        100% {{ transform: scale(1); }}
      }}
      #spinBtn {{
        margin-top: 16px;
        padding: 10px 28px;
        font-size: min(16px, 4vw);
        font-weight: bold;
        background: linear-gradient(90deg, #c2185b, #2a4d8f);
        color: #fff;
        border: none;
        border-radius: 30px;
        cursor: pointer;
        box-shadow: 0 4px 10px rgba(194,24,91,.4);
        transition: transform .15s;
      }}
      #spinBtn:hover:not(:disabled) {{ transform: scale(1.05); }}
      #spinBtn:disabled {{
        opacity: .5; cursor: not-allowed;
        background: #888;
        box-shadow: none;
      }}
      #slotMsg {{
        margin-top: 14px;
        font-size: min(16px, 4vw);
        color: #2a4d8f;
        font-weight: bold;
        text-align: center;
        min-height: 24px;
      }}
      #slotMsg.final {{
        color: #c2185b;
        font-size: min(22px, 5.5vw);
      }}
      #replayBtn {{
        display: none;
        margin-top: 12px;
        padding: 8px 22px;
        border: 1px solid #999;
        background: #fff;
        border-radius: 6px;
        cursor: pointer;
        font-size: min(14px, 3.6vw);
      }}
      #replayBtn.show {{ display: inline-block; }}
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

      <!-- TRAGAMONEDAS DE LETRAS -->
      <div id="slot">
        <div id="slotTitle">🎰 Ordena las letras 🎰</div>
        <div id="reels">
          <div class="reel" id="r0">?</div>
          <div class="reel" id="r1">?</div>
          <div class="reel" id="r2">?</div>
          <div class="reel" id="r3">?</div>
          <div class="reel" id="r4">?</div>
          <div class="reel" id="r5">?</div>
        </div>
        <button id="spinBtn" onclick="spin()">🎲 Girar letras</button>
        <div id="slotMsg">Pulsa <b>Girar</b> 3 veces para revelar el nombre</div>
        <button id="replayBtn" onclick="reset()">🔄 Jugar de nuevo</button>
      </div>

    {CELEBRATION_SCRIPT}

    <script>
      // ---------- MEMORAMA ----------
      const ICONS = [
        '🎀','⭐','🌸','🍼','🧸','👶','🎈','🌷','💖',
        '🦋','🌈','🍭','🩵','🎁','🐣'
      ];

      let first = null, lock = false, matched = 0, celebrated = false;
      let lastLayout = '';

      const grid = document.getElementById('grid');
      const msg = document.getElementById('msg');
      const pairsEl = document.getElementById('pairs');
      const gameEl = document.getElementById('game');
      const slotEl = document.getElementById('slot');

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
          const rotated = shuffle(ICONS);
          cards = shuffle([...rotated, ...rotated]);
          const fingerprint = cards.join('');
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
            setTimeout(showSlot, 900);
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

      function reset() {{
        // Reset memorama
        gameEl.classList.remove('hide');
        build();
        // Reset tragamonedas
        slotEl.classList.remove('show');
        reels.forEach((r, i) => {{
          r.classList.remove('spinning', 'win');
          r.textContent = '?';
        }});
        spinCount = 0;
        spinBtn.disabled = false;
        spinBtn.textContent = '🎲 Girar letras';
        slotMsg.className = '';
        slotMsg.innerHTML = 'Pulsa <b>Girar</b> 3 veces para revelar el nombre';
        replayBtn.classList.remove('show');
      }}

      // ---------- TRAGAMONEDAS DE LETRAS ----------
      const NAME = 'AMELIA';
      const LETTERS = NAME.split('');
      const reels = [0,1,2,3,4,5].map(i => document.getElementById('r' + i));
      const spinBtn = document.getElementById('spinBtn');
      const slotMsg = document.getElementById('slotMsg');
      const replayBtn = document.getElementById('replayBtn');

      let spinCount = 0;
      let spinning = false;
      let revealed = false;

      function showSlot() {{
        gameEl.classList.add('hide');
        slotEl.classList.add('show');
        // Mostrar las letras desordenadas aleatoriamente
        const shuffled = shuffle(LETTERS);
        reels.forEach((r, i) => {{
          r.textContent = shuffled[i];
        }});
        slotMsg.innerHTML = 'Pulsa <b>Girar</b> para mezclar las letras';
      }}

      function spin() {{
        if (spinning || revealed) return;
        spinning = true;
        spinCount++;
        spinBtn.disabled = true;

        // Animar todos los rodillos
        reels.forEach(r => r.classList.add('spinning'));
        slotMsg.className = '';
        slotMsg.innerHTML = `🎰 Girando... (${{spinCount}} / 3)`;

        // Elegir resultado
        let finalLetters;
        if (spinCount >= 3) {{
          // 3er giro → ordenar como "AMELIA"
          finalLetters = LETTERS.slice();
        }} else {{
          // Giros 1 y 2 → orden aleatorio distinto al correcto
          let attempt = 0;
          do {{
            finalLetters = shuffle(LETTERS);
            attempt++;
          }} while (finalLetters.join('') === NAME && attempt < 20);
        }}

        // Detener rodillos escalonados
        reels.forEach((r, i) => {{
          setTimeout(() => {{
            r.classList.remove('spinning');
            r.textContent = finalLetters[i];
            if (i === reels.length - 1) {{
              finishSpin(finalLetters);
            }}
          }}, 600 + i * 200);
        }});
      }}

      function finishSpin(finalLetters) {{
        spinning = false;

        if (spinCount >= 3) {{
          // Victoria
          revealed = true;
          spinBtn.disabled = true;
          spinBtn.textContent = '✅ ¡AMELIA!';
          reels.forEach(r => r.classList.add('win'));
          slotMsg.className = 'final';
          slotMsg.innerHTML = '🎀 ¡Es una niña! 🎀<br><strong>Amelia</strong>';
          replayBtn.classList.add('show');
          setTimeout(() => celebrate(), 400);
        }} else {{
          spinBtn.disabled = false;
          const remaining = 3 - spinCount;
          slotMsg.innerHTML = `Faltan <b>${{remaining}}</b> giro${{remaining > 1 ? 's' : ''}} más para revelar el nombre`;
        }}
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
st.caption("💙 Hecho con amor para la llegada de Amelia 🎀")
