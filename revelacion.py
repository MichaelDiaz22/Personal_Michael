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
st.markdown('<div class="subtitle">Elige un juego para descubrir la sorpresa</div>',
            unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔄 Reiniciar todos los juegos", use_container_width=True):
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
                  margin-top: 2px;">María</div>
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
# 1. RASCA Y GANA
# ============================================================
def juego_rasca():
    scratch_html = f"""
    <!-- seed:{SEED} -->
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      body {{ margin: 0; display: flex; flex-direction: column;
             align-items: center; font-family: sans-serif; background: #fff; }}
      #wrap {{
        position: relative; width: 480px; height: 340px;
        border-radius: 16px; overflow: hidden;
        box-shadow: 0 6px 20px rgba(0,0,0,.18);
        touch-action: none;
      }}
      #reveal {{
        position: absolute; inset: 0;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        background: linear-gradient(135deg, #ffd1e3, #cfe4ff);
        color: #c2185b; text-align: center;
      }}
      #reveal .emoji {{ font-size: 60px; }}
      #reveal h1 {{ margin: 4px 0; font-size: 46px; }}
      #reveal p  {{ margin: 0; font-size: 30px; color: #2a4d8f; font-weight: bold; }}
      #cover {{ position: absolute; inset: 0; background: #b0b0b0; cursor: crosshair; }}
      #hint {{
        position: absolute; top: 8px; left: 50%;
        transform: translateX(-50%);
        background: rgba(0,0,0,.55); color: #fff;
        padding: 4px 12px; border-radius: 12px;
        font-size: 13px; pointer-events: none;
      }}
      #resetBtn {{
        margin-top: 14px; padding: 8px 22px;
        border: 1px solid #999; background: #fff;
        border-radius: 6px; cursor: pointer; font-size: 14px;
      }}
    </style>
    </head>
    <body>
      <div id="wrap">
        <div id="reveal">
          <div class="emoji">🎀</div>
          <h1>¡Es una niña!</h1>
          <p>María</p>
        </div>
        <canvas id="cover" width="480" height="340"></canvas>
        <div id="hint">Rasca al menos 10 segundos 👆</div>
      </div>
      <button id="resetBtn" onclick="reset()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      const canvas = document.getElementById('cover');
      const ctx = canvas.getContext('2d');
      const hint = document.getElementById('hint');
      let drawing = false;
      let scratchingTime = 0;
      let lastTick = 0;
      const MIN_MS = 10000;
      let celebrated = false;

      function paintCover() {{
        ctx.globalCompositeOperation = 'source-over';
        ctx.fillStyle = '#b0b0b0';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#8a8a8a';
        ctx.font = 'bold 20px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('Rasca aquí', canvas.width/2, canvas.height/2 - 10);
        ctx.font = '14px sans-serif';
        ctx.fillText('(mínimo 10 segundos)', canvas.width/2, canvas.height/2 + 16);
        ctx.globalCompositeOperation = 'destination-out';
      }}

      function reset() {{
        scratchingTime = 0;
        lastTick = 0;
        celebrated = false;
        canvas.style.display = 'block';
        canvas.style.opacity = 1;
        canvas.style.transition = 'none';
        hint.style.display = 'block';
        hint.textContent = 'Rasca al menos 10 segundos 👆';
        paintCover();
      }}

      paintCover();

      function pos(e) {{
        const r = canvas.getBoundingClientRect();
        const t = e.touches ? e.touches[0] : e;
        return {{
          x: (t.clientX - r.left) * (canvas.width / r.width),
          y: (t.clientY - r.top) * (canvas.height / r.height)
        }};
      }}

      function scratch(e) {{
        if (!drawing) return;
        const now = performance.now();
        if (lastTick) scratchingTime += now - lastTick;
        lastTick = now;

        const p = pos(e);
        ctx.beginPath();
        ctx.arc(p.x, p.y, 28, 0, Math.PI * 2);
        ctx.fill();

        const remaining = Math.max(0, (MIN_MS - scratchingTime) / 1000).toFixed(1);
        hint.textContent = `Rascando... faltan ${{remaining}}s`;

        const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
        let clear = 0;
        for (let i = 3; i < data.length; i += 4) if (data[i] < 40) clear++;
        const pct = clear / (canvas.width * canvas.height);

        if (pct > 0.55 && scratchingTime >= MIN_MS) {{
          canvas.style.transition = 'opacity .8s';
          canvas.style.opacity = 0;
          hint.style.display = 'none';
          setTimeout(() => canvas.style.display = 'none', 800);
          if (!celebrated) {{
            celebrated = true;
            setTimeout(() => celebrate(), 300);
          }}
        }} else if (pct > 0.55 && scratchingTime < MIN_MS) {{
          hint.textContent = `Sigue rascando... faltan ${{remaining}}s`;
        }}
      }}

      canvas.addEventListener('mousedown', e => {{
        drawing = true; lastTick = performance.now(); scratch(e);
      }});
      canvas.addEventListener('mousemove', scratch);
      window.addEventListener('mouseup', () => {{ drawing = false; lastTick = 0; }});

      canvas.addEventListener('touchstart', e => {{
        e.preventDefault(); drawing = true; lastTick = performance.now(); scratch(e);
      }});
      canvas.addEventListener('touchmove', e => {{ e.preventDefault(); scratch(e); }});
      window.addEventListener('touchend', () => {{ drawing = false; lastTick = 0; }});
    </script>
    </body>
    </html>
    """
    components.html(scratch_html, height=460)


# ============================================================
# 2. MEMORAMA (15 parejas)
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
        font-family: sans-serif; background: #fff;
        width: 100%; overflow-x: hidden;
      }}
      body {{
        display: flex; flex-direction: column; align-items: center;
        padding: 6px 4px; box-sizing: border-box;
      }}
      #grid {{
        display: grid;
        grid-template-columns: repeat(6, min(62px, 14vw));
        grid-template-rows: repeat(5, min(62px, 14vw));
        gap: min(8px, 1.6vw);
        justify-content: center;
        width: 100%;
      }}
      .card {{ width: 100%; height: 100%; perspective: 600px; cursor: pointer; }}
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
        color: #fff; font-size: min(22px, 5vw);
      }}
      .back {{
        background: #fff; border: 2px solid #cfe4ff;
        transform: rotateY(180deg);
      }}
      .card.matched .back {{ border-color: #ffb3d1; background: #fff0f7; }}
      #msg {{
        margin-top: 14px; font-size: min(22px, 5vw); color: #c2185b;
        min-height: 30px; text-align: center;
      }}
      #info {{ margin-top: 6px; color: #666; font-size: min(14px, 3.5vw); }}
      button {{
        margin-top: 12px; padding: 8px 22px; border: 1px solid #999;
        background: #fff; cursor: pointer; border-radius: 6px;
        font-size: min(14px, 3.6vw);
      }}
    </style>
    </head>
    <body>
      <div id="info">Parejas encontradas: <span id="pairs">0</span> / 15</div>
      <div id="grid"></div>
      <div id="msg"></div>
      <button onclick="reset()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      const ICONS = [
        '🎀','⭐','🌸','🍼','🧸','👶','🎈','🌷','💖',
        '🦋','🌈','🍭','🩵','🎁','🐣'
      ];
      let first = null, lock = false, matched = 0, celebrated = false;
      let lastLayout = '';
      const grid = document.getElementById('grid');
      const msg = document.getElementById('msg');
      const pairsEl = document.getElementById('pairs');

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
        let attempt = 0, cards;
        do {{
          const rotated = shuffle(ICONS);
          cards = shuffle([...rotated, ...rotated]);
          const fp = cards.join('');
          if (fp !== lastLayout) {{ lastLayout = fp; break; }}
          attempt++;
        }} while (attempt < 5);
        return cards;
      }}
      function build() {{
        grid.innerHTML = '';
        msg.innerHTML = '';
        matched = 0; first = null; lock = false; celebrated = false;
        pairsEl.textContent = '0';
        generateLayout().forEach((icon, index) => {{
          const c = document.createElement('div');
          c.className = 'card';
          c.dataset.icon = icon;
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
          first.classList.add('matched'); card.classList.add('matched');
          matched++; first = null;
          pairsEl.textContent = matched;
          if (matched === 15 && !celebrated) {{
            celebrated = true;
            msg.innerHTML = '🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
            setTimeout(() => celebrate(), 250);
          }}
        }} else {{
          lock = true;
          setTimeout(() => {{
            first.classList.remove('flipped'); card.classList.remove('flipped');
            first = null; lock = false;
          }}, 700);
        }}
      }}
      function reset() {{ build(); }}
      build();
    </script>
    </body>
    </html>
    """
    components.html(memory_html, height=560)


# ============================================================
# 3. ROMPECABEZAS
# ============================================================
def juego_rompecabezas():
    puzzle_html = f"""
    <!-- seed:{SEED} -->
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      body {{ margin: 0; display: flex; flex-direction: column;
             align-items: center; font-family: sans-serif; background: #fff; }}
      #board {{
        display: grid;
        grid-template-columns: repeat(3, 110px);
        grid-template-rows: repeat(3, 110px);
        gap: 3px; background: #ddd; padding: 4px;
        border-radius: 10px; touch-action: none; user-select: none;
      }}
      .tile {{
        display: flex; align-items: center; justify-content: center;
        font-size: 34px; font-weight: bold; color: #fff;
        cursor: pointer; border-radius: 6px;
        transition: transform .15s;
      }}
      .tile:hover {{ transform: scale(0.96); }}
      .tile.empty {{ background: #f5f5f5 !important; cursor: default; }}
      #msg {{
        margin-top: 18px; font-size: 24px; color: #c2185b;
        min-height: 40px; text-align: center; line-height: 1.3;
      }}
      button {{
        margin-top: 10px; padding: 8px 22px; border: 1px solid #999;
        background: #fff; cursor: pointer; border-radius: 6px; font-size: 14px;
      }}
    </style>
    </head>
    <body>
      <div id="board"></div>
      <div id="msg"></div>
      <button onclick="shuffleBoard()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      const SIZE = 3;
      const COLORS = ['#e63946','#f77f00','#fcbf49','#06a77d','#4c6ef5','#8338ec','#ff6b9d','#00b4d8'];
      let board = [], solved = false;
      function randInt(max) {{
        const buf = new Uint32Array(1);
        crypto.getRandomValues(buf);
        return buf[0] % max;
      }}
      function createSolved() {{
        board = [];
        for (let i = 1; i < SIZE * SIZE; i++) board.push(i);
        board.push(0);
      }}
      function shuffleBoard() {{
        do {{
          board = [...Array(SIZE * SIZE).keys()];
          for (let i = board.length - 1; i > 0; i--) {{
            const j = randInt(i + 1);
            [board[i], board[j]] = [board[j], board[i]];
          }}
        }} while (!isSolvable(board) || isSolved());
        solved = false;
        document.getElementById('msg').innerHTML = '';
        render();
      }}
      function isSolvable(arr) {{
        const a = arr.filter(x => x !== 0);
        let inv = 0;
        for (let i = 0; i < a.length; i++)
          for (let j = i + 1; j < a.length; j++)
            if (a[i] > a[j]) inv++;
        return inv % 2 === 0;
      }}
      function isSolved() {{
        for (let i = 0; i < SIZE * SIZE - 1; i++)
          if (board[i] !== i + 1) return false;
        return board[SIZE * SIZE - 1] === 0;
      }}
      function render() {{
        const b = document.getElementById('board');
        b.innerHTML = '';
        board.forEach((val, idx) => {{
          const d = document.createElement('div');
          d.className = 'tile' + (val === 0 ? ' empty' : '');
          if (val !== 0) {{
            d.textContent = val;
            d.style.background = COLORS[(val - 1) % COLORS.length];
          }}
          d.onclick = () => onClick(idx);
          b.appendChild(d);
        }});
      }}
      function onClick(idx) {{
        if (solved) return;
        const empty = board.indexOf(0);
        const r1 = Math.floor(idx / SIZE), c1 = idx % SIZE;
        const r2 = Math.floor(empty / SIZE), c2 = empty % SIZE;
        if (Math.abs(r1 - r2) + Math.abs(c1 - c2) === 1) {{
          [board[idx], board[empty]] = [board[empty], board[idx]];
          render();
          if (isSolved()) {{
            solved = true;
            document.getElementById('msg').innerHTML =
              '🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
            setTimeout(() => celebrate(), 250);
          }}
        }}
      }}
      createSolved();
      shuffleBoard();
    </script>
    </body>
    </html>
    """
    components.html(puzzle_html, height=580)


# ============================================================
# 4. GLOBO SORPRESA
# ============================================================
def juego_globo():
    balloon_html = f"""
    <!-- seed:{SEED} -->
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      body {{ margin: 0; display: flex; flex-direction: column;
             align-items: center; font-family: sans-serif; background: #fff;
             padding: 10px; }}
      #stage {{
        position: relative; width: 100%; max-width: 480px; height: 340px;
        display: flex; align-items: center; justify-content: center;
        touch-action: manipulation;
      }}
      #balloon {{
        width: 90px; height: 110px;
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        background: radial-gradient(circle at 30% 30%, #ff8fb1, #c2185b);
        cursor: pointer; transition: all .15s ease-out;
        position: relative;
      }}
      #balloon::after {{
        content: ''; position: absolute; bottom: -14px; left: 50%;
        transform: translateX(-50%);
        width: 2px; height: 16px; background: #888;
      }}
      #hint {{ color: #666; font-size: 14px; margin-top: 10px; }}
      #msg {{
        margin-top: 14px; font-size: 24px; color: #c2185b;
        min-height: 40px; text-align: center; line-height: 1.3;
      }}
      button {{
        margin-top: 10px; padding: 8px 22px; border: 1px solid #999;
        background: #fff; cursor: pointer; border-radius: 6px; font-size: 14px;
      }}
      @keyframes pop {{
        0% {{ transform: scale(1); opacity: 1; }}
        100% {{ transform: scale(2.2); opacity: 0; }}
      }}
      .pop {{ animation: pop .4s ease-out forwards; }}
    </style>
    </head>
    <body>
      <div id="stage"><div id="balloon"></div></div>
      <div id="hint">Haz clic/toque el globo para inflarlo (necesitas ~20 toques)</div>
      <div id="msg"></div>
      <button onclick="reset()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      const balloon = document.getElementById('balloon');
      const hint = document.getElementById('hint');
      const msg = document.getElementById('msg');
      const NEED = 20;
      let count = 0, done = false;
      function update() {{
        const scale = 1 + count / NEED * 1.2;
        balloon.style.transform = `scale(${{scale}})`;
        hint.textContent = `Toques: ${{count}} / ${{NEED}}`;
      }}
      balloon.addEventListener('click', () => {{
        if (done) return;
        count++;
        update();
        if (count >= NEED) {{
          done = true;
          balloon.classList.add('pop');
          msg.innerHTML = '🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
          hint.textContent = '¡El globo explotó! 🎉';
          setTimeout(() => celebrate(), 200);
        }}
      }});
      function reset() {{
        count = 0; done = false;
        balloon.classList.remove('pop');
        balloon.style.transform = 'scale(1)';
        msg.innerHTML = '';
        hint.textContent = 'Haz clic/toque el globo para inflarlo (necesitas ~20 toques)';
        update();
      }}
      update();
    </script>
    </body>
    </html>
    """
    components.html(balloon_html, height=560)


# ============================================================
# 5. TRIQUI DE BOMBAS
# ============================================================
def juego_triqui_bombas():
    bombitas_html = f"""
    <!-- seed:{SEED} -->
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      html, body {{ margin: 0; padding: 0; font-family: sans-serif;
        background: #fff; width: 100%; overflow-x: hidden; }}
      body {{ display: flex; flex-direction: column; align-items: center;
        padding: 10px 4px; box-sizing: border-box; }}
      #title {{ color: #c2185b; font-weight: bold;
        font-size: min(18px, 4.5vw); margin-bottom: 10px; text-align: center; }}
      #board {{
        display: grid;
        grid-template-columns: repeat(3, min(110px, 26vw));
        grid-template-rows: repeat(3, min(110px, 26vw));
        gap: min(10px, 2.5vw); background: #f0f4ff;
        padding: min(10px, 2.5vw); border-radius: 16px;
        touch-action: manipulation;
      }}
      .bomb {{
        width: 100%; height: 100%;
        border-radius: 50% 50% 50% 50% / 55% 55% 45% 45%;
        background: radial-gradient(circle at 32% 28%, #ffffff, #ececec 70%, #d8d8d8);
        box-shadow: inset -4px -6px 10px rgba(0,0,0,.08), 0 3px 8px rgba(0,0,0,.12);
        cursor: pointer; position: relative;
        transition: transform .15s ease, box-shadow .25s ease, background .35s ease;
        display: flex; align-items: center; justify-content: center;
        font-size: min(38px, 9vw); user-select: none;
      }}
      .bomb::after {{
        content: ''; position: absolute; bottom: -12%; left: 50%;
        transform: translateX(-50%); width: 12%; height: 18%;
        background: #bbb; clip-path: polygon(50% 0, 100% 100%, 0 100%);
      }}
      .bomb:hover:not(.pink):not(.blue) {{ transform: scale(1.05); }}
      .bomb:active:not(.pink):not(.blue) {{ transform: scale(0.95); }}
      .bomb.pink {{
        background: radial-gradient(circle at 32% 28%, #ffd1e3, #ff6b9d 65%, #c2185b);
        box-shadow: inset -4px -6px 12px rgba(0,0,0,.15), 0 0 20px rgba(255,107,157,.55);
        cursor: default;
      }}
      .bomb.blue {{
        background: radial-gradient(circle at 32% 28%, #cfe4ff, #4c6ef5 65%, #2a4d8f);
        box-shadow: inset -4px -6px 12px rgba(0,0,0,.15), 0 0 20px rgba(76,110,245,.5);
        cursor: default;
      }}
      .bomb.win {{ animation: pop 0.6s ease-out; }}
      @keyframes pop {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.18); }}
        100% {{ transform: scale(1); }}
      }}
      #msg {{
        margin-top: 16px; font-size: min(22px, 5vw); font-weight: bold;
        min-height: 40px; text-align: center; line-height: 1.3;
        color: #2a4d8f; max-width: 480px;
      }}
      #msg.win {{ color: #c2185b; }}
      #counter {{ margin-top: 8px; color: #666; font-size: min(14px, 3.6vw); }}
      button {{
        margin-top: 12px; padding: 8px 22px; border: 1px solid #999;
        background: #fff; border-radius: 6px; cursor: pointer;
        font-size: min(14px, 3.6vw);
      }}
    </style>
    </head>
    <body>
      <div id="title">💗 Presiona las bombas blancas y encuentra el triki rosa 💗</div>
      <div id="board"></div>
      <div id="msg" class="info">Presiona una bomba blanca ⚪</div>
      <div id="counter">Bombas reveladas: <span id="rev">0</span> / 9</div>
      <button onclick="reset()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      const TOTAL = 9;
      const WINS = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
      ];
      let colors = [], revealed = [], winningLine = [];
      let done = false, celebrated = false;
      const boardEl = document.getElementById('board');
      const msg = document.getElementById('msg');
      const revEl = document.getElementById('rev');

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
      function hasLineOf(c, color) {{
        return WINS.some(line => line.every(idx => c[idx] === color));
      }}
      function generateBoard() {{
        let attempts = 0, valid = false;
        while (!valid && attempts < 500) {{
          attempts++;
          const line = WINS[randInt(WINS.length)];
          const c = Array(TOTAL).fill(null);
          line.forEach(i => c[i] = 'pink');
          const libres = [];
          for (let i = 0; i < TOTAL; i++) if (c[i] === null) libres.push(i);
          shuffle(libres).slice(0, 2).forEach(i => c[i] = 'pink');
          for (let i = 0; i < TOTAL; i++) if (c[i] === null) c[i] = 'blue';
          const pinks = c.filter(x => x === 'pink').length;
          const blues = c.filter(x => x === 'blue').length;
          if (pinks === 5 && blues === 4 && hasLineOf(c, 'pink') && !hasLineOf(c, 'blue')) {{
            colors = c;
            winningLine = line;
            valid = true;
          }}
        }}
        if (!valid) {{
          colors = ['pink','pink','pink','blue','pink','blue','blue','pink','blue'];
          winningLine = [0,1,2];
        }}
      }}
      function reset() {{
        generateBoard();
        revealed = Array(TOTAL).fill(false);
        done = false; celebrated = false;
        msg.className = 'info';
        msg.innerHTML = 'Presiona una bomba blanca ⚪';
        revEl.textContent = '0';
        render();
      }}
      function render() {{
        boardEl.innerHTML = '';
        for (let i = 0; i < TOTAL; i++) {{
          const b = document.createElement('div');
          b.className = 'bomb';
          if (revealed[i]) {{
            b.classList.add(colors[i]);
            b.textContent = colors[i] === 'pink' ? '💗' : '💙';
          }}
          b.onclick = () => reveal(i);
          boardEl.appendChild(b);
        }}
      }}
      function findRevealedPinkLine() {{
        for (const line of WINS) {{
          if (line.every(idx => revealed[idx] && colors[idx] === 'pink')) return line;
        }}
        return null;
      }}
      function reveal(i) {{
        if (done || revealed[i]) return;
        revealed[i] = true;
        const count = revealed.filter(x => x).length;
        revEl.textContent = count;
        render();
        const winLine = findRevealedPinkLine();
        if (winLine && !done) {{
          done = true;
          [...boardEl.children].forEach((el, idx) => {{
            if (winLine.includes(idx)) el.classList.add('win');
          }});
          msg.className = 'win';
          msg.innerHTML = '🎉 ¡Tres rosas en línea! 🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
          if (!celebrated) {{
            celebrated = true;
            setTimeout(() => celebrate(), 400);
          }}
        }} else if (count < TOTAL) {{
          const pinksRevealed = revealed.filter((r, idx) => r && colors[idx] === 'pink').length;
          msg.className = 'info';
          msg.innerHTML = `¡Sigue! Rosas descubiertas: <b>${{pinksRevealed}}</b> / 5 🌸`;
        }}
      }}
      reset();
    </script>
    </body>
    </html>
    """
    components.html(bombitas_html, height=580)


# ============================================================
# 6. DARDOS
# ============================================================
def juego_dardos():
    dardos_html = f"""
    <!-- seed:{SEED} -->
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      html, body {{ margin: 0; padding: 0; font-family: sans-serif;
        background: #fff; width: 100%; overflow-x: hidden; }}
      body {{ display: flex; flex-direction: column; align-items: center;
        padding: 10px 4px; box-sizing: border-box; }}
      #title {{ color: #c2185b; font-weight: bold;
        font-size: min(18px, 4.5vw); margin-bottom: 6px; text-align: center; }}
      #info {{ color: #666; font-size: min(13px, 3.5vw);
        margin-bottom: 10px; text-align: center; }}
      #stage {{
        position: relative;
        width: min(340px, 78vw);
        height: min(340px, 78vw);
        touch-action: manipulation;
      }}
      #target {{
        position: absolute; inset: 0;
        border-radius: 50%;
        background: radial-gradient(circle,
          #c2185b 0 18%,
          #ff6b9d 18% 36%,
          #ffffff 36% 54%,
          #4c6ef5 54% 72%,
          #2a4d8f 72% 100%);
        box-shadow: 0 6px 20px rgba(0,0,0,.15), inset 0 0 30px rgba(0,0,0,.1);
        cursor: crosshair;
      }}
      .dart {{
        position: absolute;
        width: 14px; height: 14px;
        background: #ffd400;
        border: 2px solid #333;
        border-radius: 50%;
        transform: translate(-50%, -50%);
        box-shadow: 0 0 8px rgba(255,212,0,.9);
        pointer-events: none;
        animation: dartIn 0.25s ease-out;
      }}
      @keyframes dartIn {{
        0% {{ transform: translate(-50%, -50%) scale(0); }}
        60% {{ transform: translate(-50%, -50%) scale(1.3); }}
        100% {{ transform: translate(-50%, -50%) scale(1); }}
      }}
      #score {{
        margin-top: 14px; font-size: min(20px, 5vw);
        color: #2a4d8f; font-weight: bold;
      }}
      #msg {{
        margin-top: 8px; font-size: min(20px, 5vw); font-weight: bold;
        min-height: 40px; text-align: center;
        color: #2a4d8f; max-width: 480px;
      }}
      #msg.win {{ color: #c2185b; }}
      button {{
        margin-top: 12px; padding: 8px 22px; border: 1px solid #999;
        background: #fff; border-radius: 6px; cursor: pointer;
        font-size: min(14px, 3.6vw);
      }}
    </style>
    </head>
    <body>
      <div id="title">🎯 Tira 3 dardos al centro rosa 🎯</div>
      <div id="info">Acierta <b>3 veces</b> en el círculo rosa central</div>
      <div id="stage">
        <div id="target"></div>
      </div>
      <div id="score">Centro: <span id="hits">0</span> / 3 · Tiros: <span id="shots">0</span> / 10</div>
      <div id="msg"></div>
      <button onclick="reset()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      const target = document.getElementById('target');
      const stage = document.getElementById('stage');
      const hitsEl = document.getElementById('hits');
      const shotsEl = document.getElementById('shots');
      const msg = document.getElementById('msg');

      const NEEDED = 3;
      const MAX_SHOTS = 10;

      let hits = 0, shots = 0, done = false, celebrated = false;

      function reset() {{
        hits = 0; shots = 0; done = false; celebrated = false;
        hitsEl.textContent = '0';
        shotsEl.textContent = '0';
        msg.className = '';
        msg.innerHTML = '';
        [...stage.querySelectorAll('.dart')].forEach(d => d.remove());
      }}

      target.addEventListener('click', e => {{
        if (done || shots >= MAX_SHOTS) return;
        const rect = target.getBoundingClientRect();
        const cx = e.clientX - rect.left;
        const cy = e.clientY - rect.top;
        const nx = cx - rect.width / 2;
        const ny = cy - rect.height / 2;
        const dist = Math.sqrt(nx * nx + ny * ny);
        const radius = rect.width / 2;
        const pct = dist / radius;

        // Crear dardo visual
        const dart = document.createElement('div');
        dart.className = 'dart';
        dart.style.left = cx + 'px';
        dart.style.top = cy + 'px';
        stage.appendChild(dart);

        shots++;
        shotsEl.textContent = shots;

        // El centro rosa está en 0%-18% del radio (bullseye)
        if (pct <= 0.18) {{
          hits++;
          hitsEl.textContent = hits;
          if (hits >= NEEDED && !done) {{
            done = true;
            msg.className = 'win';
            msg.innerHTML = '🎯 ¡En el centro! 🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
            if (!celebrated) {{
              celebrated = true;
              setTimeout(() => celebrate(), 300);
            }}
          }}
        }} else if (shots >= MAX_SHOTS && hits < NEEDED) {{
          done = true;
          msg.innerHTML = `❌ Te quedaste sin tiros (acertaste ${{hits}}/3). Reinicia para intentar.`;
        }}
      }});

      reset();
    </script>
    </body>
    </html>
    """
    components.html(dardos_html, height=560)


# ============================================================
# 7. SIMÓN DICE
# ============================================================
def juego_simon():
    simon_html = f"""
    <!-- seed:{SEED} -->
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      html, body {{ margin: 0; padding: 0; font-family: sans-serif;
        background: #fff; width: 100%; overflow-x: hidden; }}
      body {{ display: flex; flex-direction: column; align-items: center;
        padding: 10px 4px; box-sizing: border-box; }}
      #title {{ color: #c2185b; font-weight: bold;
        font-size: min(18px, 4.5vw); margin-bottom: 6px; text-align: center; }}
      #info {{ color: #666; font-size: min(13px, 3.5vw);
        margin-bottom: 12px; text-align: center; }}
      #grid {{
        display: grid;
        grid-template-columns: repeat(2, min(130px, 32vw));
        grid-template-rows: repeat(2, min(130px, 32vw));
        gap: min(10px, 2.5vw);
      }}
      .pad {{
        border-radius: 16px;
        cursor: pointer;
        transition: transform .1s, filter .1s, box-shadow .15s;
        opacity: .55;
        box-shadow: 0 3px 10px rgba(0,0,0,.15);
      }}
      .pad.active {{
        opacity: 1;
        transform: scale(1.03);
        filter: brightness(1.25);
        box-shadow: 0 0 25px rgba(255,255,255,.9);
      }}
      .pad:hover {{ opacity: .8; }}
      #p0 {{ background: radial-gradient(circle at 30% 30%, #ff9ec4, #c2185b); }}
      #p1 {{ background: radial-gradient(circle at 30% 30%, #9ec6ff, #2a4d8f); }}
      #p2 {{ background: radial-gradient(circle at 30% 30%, #ffd1e3, #ff6b9d); }}
      #p3 {{ background: radial-gradient(circle at 30% 30%, #cfe4ff, #4c6ef5); }}
      #msg {{
        margin-top: 16px; font-size: min(22px, 5vw); font-weight: bold;
        min-height: 40px; text-align: center;
        color: #2a4d8f; max-width: 480px;
      }}
      #msg.win {{ color: #c2185b; }}
      #msg.error {{ color: #d32f2f; }}
      #level {{
        margin-top: 8px; color: #666; font-size: min(15px, 4vw);
      }}
      button {{
        margin-top: 12px; padding: 8px 22px; border: 1px solid #999;
        background: #fff; border-radius: 6px; cursor: pointer;
        font-size: min(14px, 3.6vw);
      }}
    </style>
    </head>
    <body>
      <div id="title">🔢 Simón dice — repite la secuencia 🔢</div>
      <div id="info">Observa la secuencia y repítela. Necesitas <b>8 aciertos</b> seguidos.</div>
      <div id="grid">
        <div class="pad" id="p0"></div>
        <div class="pad" id="p1"></div>
        <div class="pad" id="p2"></div>
        <div class="pad" id="p3"></div>
      </div>
      <div id="level">Nivel: <span id="lvl">0</span> / 8</div>
      <div id="msg"></div>
      <button onclick="reset()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      const LEVELS = 8;
      const pads = [0,1,2,3].map(i => document.getElementById('p' + i));
      const msg = document.getElementById('msg');
      const lvlEl = document.getElementById('lvl');

      let sequence = [];
      let playerIdx = 0;
      let accepting = false;
      let done = false, celebrated = false;

      function randInt(max) {{
        const buf = new Uint32Array(1);
        crypto.getRandomValues(buf);
        return buf[0] % max;
      }}

      function flashPad(i, dur = 400) {{
        pads[i].classList.add('active');
        setTimeout(() => pads[i].classList.remove('active'), dur);
      }}

      function playSequence() {{
        accepting = false;
        msg.className = '';
        msg.innerHTML = '👀 Observa la secuencia...';
        let i = 0;
        const interval = setInterval(() => {{
          flashPad(sequence[i]);
          i++;
          if (i >= sequence.length) {{
            clearInterval(interval);
            setTimeout(() => {{
              accepting = true;
              playerIdx = 0;
              msg.innerHTML = '✋ ¡Tu turno! Repite la secuencia';
            }}, 500);
          }}
        }}, 700);
      }}

      function nextLevel() {{
        if (sequence.length >= LEVELS) {{
          done = true;
          msg.className = 'win';
          msg.innerHTML = '🎉 ¡Completaste los 8 niveles! 🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
          if (!celebrated) {{
            celebrated = true;
            setTimeout(() => celebrate(), 300);
          }}
          return;
        }}
        sequence.push(randInt(4));
        lvlEl.textContent = sequence.length;
        setTimeout(playSequence, 400);
      }}

      pads.forEach((pad, i) => {{
        pad.addEventListener('click', () => {{
          if (!accepting || done) return;
          flashPad(i, 250);
          if (sequence[playerIdx] === i) {{
            playerIdx++;
            if (playerIdx === sequence.length) {{
              accepting = false;
              msg.innerHTML = '✅ ¡Bien! Siguiente nivel...';
              setTimeout(nextLevel, 600);
            }}
          }} else {{
            accepting = false;
            msg.className = 'error';
            msg.innerHTML = '❌ Fallaste... Reinicia para volver a intentar';
            done = true;
          }}
        }});
      }});

      function reset() {{
        sequence = [];
        playerIdx = 0;
        accepting = false;
        done = false; celebrated = false;
        lvlEl.textContent = '0';
        msg.className = '';
        msg.innerHTML = 'Pulsa <b>Iniciar</b> o espera 1 segundo...';
        setTimeout(() => {{
          msg.innerHTML = '';
          nextLevel();
        }}, 1200);
      }}

      reset();
    </script>
    </body>
    </html>
    """
    components.html(simon_html, height=560)


# ============================================================
# 8. SERPIENTE
# ============================================================
def juego_serpiente():
    snake_html = f"""
    <!-- seed:{SEED} -->
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      html, body {{ margin: 0; padding: 0; font-family: sans-serif;
        background: #fff; width: 100%; overflow-x: hidden; }}
      body {{ display: flex; flex-direction: column; align-items: center;
        padding: 10px 4px; box-sizing: border-box; }}
      #title {{ color: #c2185b; font-weight: bold;
        font-size: min(18px, 4.5vw); margin-bottom: 6px; text-align: center; }}
      #info {{ color: #666; font-size: min(13px, 3.5vw);
        margin-bottom: 10px; text-align: center; }}
      #wrap {{
        position: relative;
        width: min(340px, 82vw);
        height: min(340px, 82vw);
      }}
      #board {{
        width: 100%; height: 100%;
        background: #f0f4ff;
        border-radius: 12px;
        display: grid;
        grid-template-columns: repeat(15, 1fr);
        grid-template-rows: repeat(15, 1fr);
        box-shadow: 0 3px 10px rgba(0,0,0,.1);
      }}
      .cell {{ border-radius: 3px; margin: 1px; }}
      .cell.snake {{ background: radial-gradient(circle at 30% 30%, #ff9ec4, #c2185b); }}
      .cell.food {{ background: radial-gradient(circle at 30% 30%, #cfe4ff, #2a4d8f); }}
      #controls {{
        margin-top: 12px;
        display: grid;
        grid-template-columns: repeat(3, 60px);
        grid-template-rows: repeat(2, 60px);
        gap: 6px;
        justify-content: center;
      }}
      #controls button {{
        font-size: 24px; border: 1px solid #999; background: #fff;
        border-radius: 8px; cursor: pointer;
      }}
      #controls button:active {{ background: #eef; }}
      #up {{ grid-column: 2; }}
      #left {{ grid-column: 1; grid-row: 2; }}
      #down {{ grid-column: 2; grid-row: 2; }}
      #right {{ grid-column: 3; grid-row: 2; }}
      #score {{
        margin-top: 12px; font-size: min(18px, 4.5vw);
        color: #2a4d8f; font-weight: bold;
      }}
      #msg {{
        margin-top: 8px; font-size: min(20px, 5vw); font-weight: bold;
        min-height: 40px; text-align: center;
        color: #2a4d8f; max-width: 480px;
      }}
      #msg.win {{ color: #c2185b; }}
      #msg.error {{ color: #d32f2f; }}
      #reset {{
        margin-top: 12px; padding: 8px 22px; border: 1px solid #999;
        background: #fff; border-radius: 6px; cursor: pointer;
        font-size: min(14px, 3.6vw);
      }}
    </style>
    </head>
    <body>
      <div id="title">🐍 Serpiente rosa come 10 frutas azules 🐍</div>
      <div id="info">Usa los botones o las flechas del teclado</div>
      <div id="wrap"><div id="board"></div></div>
      <div id="controls">
        <button id="up">▲</button>
        <button id="left">◀</button>
        <button id="down">▼</button>
        <button id="right">▶</button>
      </div>
      <div id="score">Frutas: <span id="score">0</span> / 10</div>
      <div id="msg"></div>
      <button id="reset" onclick="reset()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      const COLS = 15, ROWS = 15;
      const GOAL = 10;
      const board = document.getElementById('board');
      const scoreEl = document.getElementById('score');
      const msg = document.getElementById('msg');

      let snake, dir, food, score, done, celebrated, intervalId;

      function randInt(max) {{
        const buf = new Uint32Array(1);
        crypto.getRandomValues(buf);
        return buf[0] % max;
      }}

      function idx(x, y) {{ return y * COLS + x; }}

      function placeFood() {{
        let x, y;
        do {{
          x = randInt(COLS);
          y = randInt(ROWS);
        }} while (snake.some(s => s.x === x && s.y === y));
        food = {{ x, y }};
      }}

      function reset() {{
        snake = [{{x: 7, y: 7}}, {{x: 6, y: 7}}, {{x: 5, y: 7}}];
        dir = {{ x: 1, y: 0 }};
        score = 0;
        done = false; celebrated = false;
        scoreEl.textContent = '0';
        msg.className = '';
        msg.innerHTML = '';
        placeFood();
        render();
        if (intervalId) clearInterval(intervalId);
        intervalId = setInterval(tick, 220);
      }}

      function render() {{
        board.innerHTML = '';
        for (let y = 0; y < ROWS; y++) {{
          for (let x = 0; x < COLS; x++) {{
            const c = document.createElement('div');
            c.className = 'cell';
            if (snake.some(s => s.x === x && s.y === y)) c.classList.add('snake');
            else if (food && food.x === x && food.y === y) c.classList.add('food');
            board.appendChild(c);
          }}
        }}
      }}

      function tick() {{
        if (done) return;
        const head = {{ x: snake[0].x + dir.x, y: snake[0].y + dir.y }};
        // Choque con paredes o consigo misma
        if (head.x < 0 || head.x >= COLS || head.y < 0 || head.y >= ROWS ||
            snake.some(s => s.x === head.x && s.y === head.y)) {{
          done = true;
          clearInterval(intervalId);
          msg.className = 'error';
          msg.innerHTML = '❌ ¡Chocaste! Pulsa Reiniciar';
          return;
        }}
        snake.unshift(head);
        if (food && head.x === food.x && head.y === food.y) {{
          score++;
          scoreEl.textContent = score;
          if (score >= GOAL) {{
            done = true;
            clearInterval(intervalId);
            msg.className = 'win';
            msg.innerHTML = '🎉 ¡Comiste 10 frutas! 🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
            if (!celebrated) {{
              celebrated = true;
              setTimeout(() => celebrate(), 250);
            }}
            render();
            return;
          }}
          placeFood();
        }} else {{
          snake.pop();
        }}
        render();
      }}

      function setDir(x, y) {{
        if (done) return;
        // No permitir reversa
        if (dir.x === -x && dir.y === -y) return;
        dir = {{ x, y }};
      }}

      document.getElementById('up').onclick = () => setDir(0, -1);
      document.getElementById('down').onclick = () => setDir(0, 1);
      document.getElementById('left').onclick = () => setDir(-1, 0);
      document.getElementById('right').onclick = () => setDir(1, 0);

      window.addEventListener('keydown', e => {{
        if (e.key === 'ArrowUp') setDir(0, -1);
        else if (e.key === 'ArrowDown') setDir(0, 1);
        else if (e.key === 'ArrowLeft') setDir(-1, 0);
        else if (e.key === 'ArrowRight') setDir(1, 0);
      }});

      reset();
    </script>
    </body>
    </html>
    """
    components.html(snake_html, height=720)


# ============================================================
# 9. ROMPE LADRILLOS
# ============================================================
def juego_rompe_ladrillos():
    breakout_html = f"""
    <!-- seed:{SEED} -->
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      html, body {{ margin: 0; padding: 0; font-family: sans-serif;
        background: #fff; width: 100%; overflow-x: hidden; }}
      body {{ display: flex; flex-direction: column; align-items: center;
        padding: 10px 4px; box-sizing: border-box; }}
      #title {{ color: #c2185b; font-weight: bold;
        font-size: min(18px, 4.5vw); margin-bottom: 6px; text-align: center; }}
      #info {{ color: #666; font-size: min(13px, 3.5vw);
        margin-bottom: 10px; text-align: center; }}
      #wrap {{
        position: relative;
        width: min(360px, 88vw);
        height: min(400px, 96vw);
        touch-action: none;
      }}
      canvas {{
        width: 100%; height: 100%;
        background: #f0f4ff;
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,.1);
        display: block;
        touch-action: none;
      }}
      #score {{
        margin-top: 10px; font-size: min(18px, 4.5vw);
        color: #2a4d8f; font-weight: bold;
      }}
      #msg {{
        margin-top: 8px; font-size: min(20px, 5vw); font-weight: bold;
        min-height: 40px; text-align: center;
        color: #2a4d8f; max-width: 480px;
      }}
      #msg.win {{ color: #c2185b; }}
      #msg.error {{ color: #d32f2f; }}
      button {{
        margin-top: 12px; padding: 8px 22px; border: 1px solid #999;
        background: #fff; border-radius: 6px; cursor: pointer;
        font-size: min(14px, 3.6vw);
      }}
    </style>
    </head>
    <body>
      <div id="title">🧱 Rompe los ladrillos azules 🧱</div>
      <div id="info">Mueve la barra rosa con el mouse o el dedo</div>
      <div id="wrap"><canvas id="c" width="360" height="400"></canvas></div>
      <div id="score">Ladrillos: <span id="score">0</span> / 30</div>
      <div id="msg"></div>
      <button onclick="reset()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      const canvas = document.getElementById('c');
      const ctx = canvas.getContext('2d');
      const scoreEl = document.getElementById('score');
      const msg = document.getElementById('msg');

      const W = canvas.width, H = canvas.height;
      const ROWS = 5, COLS = 6;
      const BRICK_W = W / COLS;
      const BRICK_H = 18;
      const GOAL = ROWS * COLS;

      let paddle, ball, bricks, broken, running, celebrated;
      let animId;

      function reset() {{
        paddle = {{ w: 80, h: 12, x: W / 2 - 40, y: H - 30 }};
        ball = {{ x: W / 2, y: H - 60, r: 7, vx: 3, vy: -3.2 }};
        bricks = [];
        broken = 0;
        for (let r = 0; r < ROWS; r++) {{
          for (let c = 0; c < COLS; c++) {{
            bricks.push({{
              x: c * BRICK_W,
              y: 30 + r * (BRICK_H + 4),
              w: BRICK_W - 4,
              h: BRICK_H,
              alive: true
            }});
          }}
        }}
        running = true;
        celebrated = false;
        scoreEl.textContent = '0';
        msg.className = '';
        msg.innerHTML = '';
        if (animId) cancelAnimationFrame(animId);
        loop();
      }}

      function movePaddle(clientX) {{
        const rect = canvas.getBoundingClientRect();
        const x = (clientX - rect.left) * (W / rect.width);
        paddle.x = Math.max(0, Math.min(W - paddle.w, x - paddle.w / 2));
      }}

      canvas.addEventListener('mousemove', e => movePaddle(e.clientX));
      canvas.addEventListener('touchmove', e => {{
        e.preventDefault();
        movePaddle(e.touches[0].clientX);
      }}, {{ passive: false }});
      canvas.addEventListener('touchstart', e => movePaddle(e.touches[0].clientX));

      function loop() {{
        if (!running) return;
        // Mover bola
        ball.x += ball.vx;
        ball.y += ball.vy;

        // Rebotes paredes
        if (ball.x - ball.r < 0 || ball.x + ball.r > W) ball.vx = -ball.vx;
        if (ball.y - ball.r < 0) ball.vy = -ball.vy;

        // Paddle
        if (ball.y + ball.r >= paddle.y && ball.y + ball.r <= paddle.y + paddle.h + 8 &&
            ball.x >= paddle.x && ball.x <= paddle.x + paddle.w && ball.vy > 0) {{
          ball.vy = -Math.abs(ball.vy);
          // Ángulo según posición
          const rel = (ball.x - (paddle.x + paddle.w / 2)) / (paddle.w / 2);
          ball.vx = rel * 4;
        }}

        // Ladrillos
        for (const b of bricks) {{
          if (!b.alive) continue;
          if (ball.x + ball.r > b.x && ball.x - ball.r < b.x + b.w &&
              ball.y + ball.r > b.y && ball.y - ball.r < b.y + b.h) {{
            b.alive = false;
            broken++;
            scoreEl.textContent = broken;
            ball.vy = -ball.vy;
            if (broken >= GOAL && !celebrated) {{
              running = false;
              celebrated = true;
              msg.className = 'win';
              msg.innerHTML = '🎉 ¡Rompiste todos los ladrillos! 🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
              setTimeout(() => celebrate(), 300);
              return;
            }}
            break;
          }}
        }}

        // Perder
        if (ball.y - ball.r > H) {{
          running = false;
          msg.className = 'error';
          msg.innerHTML = '❌ Se cayó la pelota. Pulsa Reiniciar';
          return;
        }}

        draw();
        animId = requestAnimationFrame(loop);
      }}

      function draw() {{
        ctx.clearRect(0, 0, W, H);

        // Ladrillos
        for (const b of bricks) {{
          if (!b.alive) continue;
          const grad = ctx.createLinearGradient(b.x, b.y, b.x + b.w, b.y + b.h);
          grad.addColorStop(0, '#cfe4ff');
          grad.addColorStop(1, '#4c6ef5');
          ctx.fillStyle = grad;
          ctx.fillRect(b.x, b.y, b.w, b.h);
        }}

        // Paddle rosa
        const pg = ctx.createLinearGradient(paddle.x, 0, paddle.x + paddle.w, 0);
        pg.addColorStop(0, '#ffd1e3');
        pg.addColorStop(1, '#c2185b');
        ctx.fillStyle = pg;
        ctx.beginPath();
        ctx.roundRect(paddle.x, paddle.y, paddle.w, paddle.h, 6);
        ctx.fill();

        // Bola
        const bg = ctx.createRadialGradient(ball.x - 2, ball.y - 2, 1, ball.x, ball.y, ball.r);
        bg.addColorStop(0, '#ff9ec4');
        bg.addColorStop(1, '#c2185b');
        ctx.fillStyle = bg;
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI * 2);
        ctx.fill();
      }}

      reset();
    </script>
    </body>
    </html>
    """
    components.html(rompe_ladrillos_html, height=720)


# ============================================================
# 10. TRAGAMONEDAS
# ============================================================
def juego_tragamonedas():
    tragamonedas_html = f"""
    <!-- seed:{SEED} -->
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      html, body {{ margin: 0; padding: 0; font-family: sans-serif;
        background: #fff; width: 100%; overflow-x: hidden; }}
      body {{ display: flex; flex-direction: column; align-items: center;
        padding: 10px 4px; box-sizing: border-box; }}
      #title {{ color: #c2185b; font-weight: bold;
        font-size: min(18px, 4.5vw); margin-bottom: 6px; text-align: center; }}
      #info {{ color: #666; font-size: min(13px, 3.5vw);
        margin-bottom: 12px; text-align: center; }}
      #machine {{
        display: flex; gap: min(10px, 2vw);
        background: #2a2a2a;
        padding: min(14px, 3vw);
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,.2);
      }}
      .reel {{
        width: min(90px, 22vw);
        height: min(120px, 28vw);
        background: #fff;
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: min(58px, 14vw);
        overflow: hidden;
        box-shadow: inset 0 4px 12px rgba(0,0,0,.15);
        transition: transform .1s;
      }}
      .reel.spinning {{
        animation: spin 0.12s linear infinite;
      }}
      @keyframes spin {{
        0% {{ transform: translateY(-10%); filter: blur(1px); }}
        50% {{ transform: translateY(10%); filter: blur(2px); }}
        100% {{ transform: translateY(-10%); filter: blur(1px); }}
      }}
      #controls {{
        margin-top: 16px;
        display: flex; gap: 12px; align-items: center;
      }}
      #spinBtn {{
        padding: 12px 32px;
        font-size: min(18px, 4.5vw);
        font-weight: bold;
        background: linear-gradient(90deg, #c2185b, #2a4d8f);
        color: #fff;
        border: none;
        border-radius: 30px;
        cursor: pointer;
        box-shadow: 0 4px 10px rgba(194,24,91,.4);
      }}
      #spinBtn:disabled {{
        opacity: .5; cursor: not-allowed;
      }}
      #msg {{
        margin-top: 16px; font-size: min(22px, 5vw); font-weight: bold;
        min-height: 40px; text-align: center;
        color: #2a4d8f; max-width: 480px;
      }}
      #msg.win {{ color: #c2185b; }}
      #msg.error {{ color: #d32f2f; }}
      #tries {{ margin-top: 8px; color: #666; font-size: min(14px, 3.6vw); }}
      #reset {{
        margin-top: 12px; padding: 8px 22px; border: 1px solid #999;
        background: #fff; border-radius: 6px; cursor: pointer;
        font-size: min(14px, 3.6vw);
      }}
    </style>
    </head>
    <body>
      <div id="title">🎰 Tragamonedas — consigue 3 iguales 🎰</div>
      <div id="info">Necesitas sacar <b>💗 💗 💗</b> o <b>🎀 🎀 🎀</b> para ganar</div>
      <div id="machine">
        <div class="reel" id="r0">🎁</div>
        <div class="reel" id="r1">⭐</div>
        <div class="reel" id="r2">🌸</div>
      </div>
      <div id="controls">
        <button id="spinBtn" onclick="spin()">🎲 GIRAR</button>
      </div>
      <div id="tries">Intentos: <span id="tries">0</span></div>
      <div id="msg"></div>
      <button id="reset" onclick="reset()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      const SYMBOLS = ['💗','🎀','💙','⭐','🌸','👶','🎁'];
      const WINNING = ['💗','🎀','👶'];  // símbolos que ganan si salen 3 veces
      const reels = [0,1,2].map(i => document.getElementById('r' + i));
      const msg = document.getElementById('msg');
      const triesEl = document.getElementById('tries');
      const spinBtn = document.getElementById('spinBtn');

      let spinning = false, done = false, celebrated = false, tries = 0;

      function randInt(max) {{
        const buf = new Uint32Array(1);
        crypto.getRandomValues(buf);
        return buf[0] % max;
      }}

      function spin() {{
        if (spinning || done) return;
        spinning = true;
        spinBtn.disabled = true;
        msg.className = '';
        msg.innerHTML = '🎰 Girando...';
        reels.forEach(r => r.classList.add('spinning'));

        // Cada rodillo se detiene en momentos distintos
        const results = [randInt(SYMBOLS.length), randInt(SYMBOLS.length), randInt(SYMBOLS.length)];

        reels.forEach((r, i) => {{
          setTimeout(() => {{
            r.classList.remove('spinning');
            r.textContent = SYMBOLS[results[i]];
            if (i === 2) finishSpin(results);
          }}, 700 + i * 450);
        }});
      }}

      function finishSpin(results) {{
        spinning = false;
        spinBtn.disabled = false;
        tries++;
        triesEl.textContent = tries;

        const syms = results.map(i => SYMBOLS[i]);
        const isWin = syms[0] === syms[1] && syms[1] === syms[2] && WINNING.includes(syms[0]);

        if (isWin) {{
          done = true;
          msg.className = 'win';
          msg.innerHTML = `🎉 ¡${{syms[0]}} ${{syms[0]}} ${{syms[0]}}! 🎀 ¡Es una niña! 🎀<br><strong>María</strong>`;
          if (!celebrated) {{
            celebrated = true;
            setTimeout(() => celebrate(), 300);
          }}
        }} else {{
          msg.innerHTML = `😅 Casi... inténtalo otra vez (${{tries}} intentos)`;
        }}
      }}

      function reset() {{
        spinning = false; done = false; celebrated = false; tries = 0;
        triesEl.textContent = '0';
        msg.className = '';
        msg.innerHTML = '';
        spinBtn.disabled = false;
        reels.forEach((r, i) => {{
          r.classList.remove('spinning');
          r.textContent = ['🎁','⭐','🌸'][i];
        }});
      }}

      reset();
    </script>
    </body>
    </html>
    """
    components.html(tragamonedas_html, height=620)


# ============================================================
# 11. WHACK-A-MOLE (Golpea al bebé)
# ============================================================
def juego_whack():
    whack_html = f"""
    <!-- seed:{SEED} -->
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
      html, body {{ margin: 0; padding: 0; font-family: sans-serif;
        background: #fff; width: 100%; overflow-x: hidden; }}
      body {{ display: flex; flex-direction: column; align-items: center;
        padding: 10px 4px; box-sizing: border-box; }}
      #title {{ color: #c2185b; font-weight: bold;
        font-size: min(18px, 4.5vw); margin-bottom: 6px; text-align: center; }}
      #info {{ color: #666; font-size: min(13px, 3.5vw);
        margin-bottom: 10px; text-align: center; }}
      #hud {{
        display: flex; gap: min(20px, 4vw);
        font-size: min(16px, 4vw); color: #2a4d8f;
        font-weight: bold; margin-bottom: 10px;
      }}
      #board {{
        display: grid;
        grid-template-columns: repeat(3, min(90px, 24vw));
        grid-template-rows: repeat(3, min(90px, 24vw));
        gap: min(8px, 2vw);
        background: #f0f4ff;
        padding: min(10px, 2.5vw);
        border-radius: 16px;
      }}
      .hole {{
        background: radial-gradient(circle at 50% 80%, #d0d8ea, #9aa7c7);
        border-radius: 50% 50% 40% 40% / 70% 70% 30% 30%;
        display: flex; align-items: center; justify-content: center;
        font-size: min(48px, 12vw);
        cursor: pointer;
        overflow: hidden;
        position: relative;
        box-shadow: inset 0 6px 12px rgba(0,0,0,.15);
      }}
      .hole.up {{
        animation: popUp .25s ease-out;
      }}
      @keyframes popUp {{
        0% {{ transform: scale(0.4); }}
        100% {{ transform: scale(1); }}
      }}
      .hole.hit {{
        background: radial-gradient(circle at 50% 80%, #ffd1e3, #c2185b);
      }}
      #msg {{
        margin-top: 14px; font-size: min(20px, 5vw); font-weight: bold;
        min-height: 40px; text-align: center;
        color: #2a4d8f; max-width: 480px;
      }}
      #msg.win {{ color: #c2185b; }}
      #msg.error {{ color: #d32f2f; }}
      button {{
        margin-top: 12px; padding: 8px 22px; border: 1px solid #999;
        background: #fff; border-radius: 6px; cursor: pointer;
        font-size: min(14px, 3.6vw);
      }}
      #startBtn {{
        background: linear-gradient(90deg, #c2185b, #2a4d8f);
        color: #fff; border: none;
        font-weight: bold; padding: 10px 28px;
        font-size: min(16px, 4vw);
      }}
    </style>
    </head>
    <body>
      <div id="title">🐣 ¡Atrapa a los bebés! 🐣</div>
      <div id="info">Toca los 👶 antes de que se escondan. Necesitas <b>15</b> en 30 segundos.</div>
      <div id="hud">
        <div>Atrapados: <span id="score">0</span> / 15</div>
        <div>Tiempo: <span id="time">30</span>s</div>
      </div>
      <div id="board"></div>
      <div id="msg"></div>
      <button id="startBtn" onclick="start()">▶ Iniciar</button>
      <button onclick="reset()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      const GOAL = 15;
      const GAME_TIME = 30;
      const board = document.getElementById('board');
      const scoreEl = document.getElementById('score');
      const timeEl = document.getElementById('time');
      const msg = document.getElementById('msg');
      const startBtn = document.getElementById('startBtn');

      let score = 0, timeLeft = GAME_TIME;
      let running = false, done = false, celebrated = false;
      let spawnInterval, timerInterval;

      function randInt(max) {{
        const buf = new Uint32Array(1);
        crypto.getRandomValues(buf);
        return buf[0] % max;
      }}

      function buildBoard() {{
        board.innerHTML = '';
        for (let i = 0; i < 9; i++) {{
          const h = document.createElement('div');
          h.className = 'hole';
          h.dataset.idx = i;
          h.onclick = () => hit(h);
          board.appendChild(h);
        }}
      }}

      function spawn() {{
        if (!running) return;
        const holes = [...board.children];
        // Cuántos bebés aparecen a la vez: 2-3
        const num = 2 + randInt(2);
        const chosen = new Set();
        while (chosen.size < num) chosen.add(randInt(9));
        chosen.forEach(i => {{
          const h = holes[i];
          if (h.textContent === '👶') return;
          h.textContent = '👶';
          h.classList.remove('up', 'hit');
          // forzar reflow
          void h.offsetWidth;
          h.classList.add('up');
          // Ocultar tras un tiempo aleatorio
          setTimeout(() => {{
            if (h.textContent === '👶') {{
              h.textContent = '';
              h.classList.remove('up', 'hit');
            }}
          }}, 700 + randInt(400));
        }});
      }}

      function hit(h) {{
        if (!running || h.textContent !== '👶') return;
        h.textContent = '💗';
        h.classList.add('hit');
        score++;
        scoreEl.textContent = score;
        if (score >= GOAL && !celebrated) {{
          celebrated = true;
          endGame(true);
        }}
        setTimeout(() => {{
          h.textContent = '';
          h.classList.remove('up', 'hit');
        }}, 200);
      }}

      function start() {{
        if (running) return;
        reset();
        running = true;
        startBtn.disabled = true;
        msg.className = '';
        msg.innerHTML = '¡Atrapa todos los 👶!';
        spawnInterval = setInterval(spawn, 650);
        timerInterval = setInterval(() => {{
          timeLeft--;
          timeEl.textContent = timeLeft;
          if (timeLeft <= 0) endGame(false);
        }}, 1000);
        spawn();
      }}

      function endGame(won) {{
        running = false;
        done = true;
        clearInterval(spawnInterval);
        clearInterval(timerInterval);
        startBtn.disabled = false;
        [...board.children].forEach(h => {{ h.textContent = ''; h.classList.remove('up','hit'); }});

        if (won) {{
          msg.className = 'win';
          msg.innerHTML = '🎉 ¡Atrapaste 15 bebés! 🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
          if (!celebrated) {{
            celebrated = true;
            setTimeout(() => celebrate(), 250);
          }}
        }} else {{
          msg.className = 'error';
          msg.innerHTML = `❌ Se acabó el tiempo. Atrapaste ${{score}} de 15. Pulsa Iniciar para reintentar.`;
        }}
      }}

      function reset() {{
        running = false; done = false; celebrated = false;
        score = 0; timeLeft = GAME_TIME;
        scoreEl.textContent = '0';
        timeEl.textContent = GAME_TIME;
        msg.className = '';
        msg.innerHTML = '';
        startBtn.disabled = false;
        clearInterval(spawnInterval);
        clearInterval(timerInterval);
        buildBoard();
      }}

      reset();
    </script>
    </body>
    </html>
    """
    components.html(whack_html, height=720)


# ============================================================
# PESTAÑAS
# ============================================================
tabs = st.tabs([
    "🎨 Rasca y Gana",
    "🃏 Memorama",
    "🧩 Rompecabezas",
    "🎈 Globo Sorpresa",
    "💗 Triqui de Bombas",
    "🎯 Dardos",
    "🔢 Simón Dice",
    "🐍 Serpiente",
    "🧱 Rompe Ladrillos",
    "🎰 Tragamonedas",
    "🐣 Whack-a-Mole"
])

with tabs[0]:
    st.subheader("Rasca para descubrir")
    st.caption("Rasca el recuadro al menos **10 segundos** y cubre el 55% para revelar 👇")
    juego_rasca()

with tabs[1]:
    st.subheader("Encuentra las 15 parejas")
    st.caption("Voltea las cartas y encuentra los 15 pares 👇")
    juego_memorama()

with tabs[2]:
    st.subheader("Ordena el rompecabezas")
    st.caption("Haz click en las piezas junto al espacio vacío. Ordena del 1 al 8 👇")
    juego_rompecabezas()

with tabs[3]:
    st.subheader("Infla el globo")
    st.caption("Haz click/toque el globo unas 20 veces para que explote 👇")
    juego_globo()

with tabs[4]:
    st.subheader("Triqui de Bombas")
    st.caption("Presiona bombas blancas ⚪ hasta descubrir **3 rosas 💗 en línea** 👇")
    juego_triqui_bombas()

with tabs[5]:
    st.subheader("Tiro al blanco")
    st.caption("Toca 3 veces en el centro rosa 🎯 con máximo 10 tiros 👇")
    juego_dardos()

with tabs[6]:
    st.subheader("Simón Dice")
    st.caption("Repite la secuencia de colores. Necesitas **8 niveles** 👇")
    juego_simon()

with tabs[7]:
    st.subheader("Serpiente")
    st.caption("Come 10 frutas azules sin chocar. Usa botones o flechas 👇")
    juego_serpiente()

with tabs[8]:
    st.subheader("Rompe Ladrillos")
    st.caption("Mueve la barra rosa con el mouse/dedo y rompe los 30 ladrillos azules 👇")
    juego_rompe_ladrillos()

with tabs[9]:
    st.subheader("Tragamonedas")
    st.caption("Gira y consigue 3 iguales (💗, 🎀 o 👶) 👇")
    juego_tragamonedas()

with tabs[10]:
    st.subheader("Whack-a-Mole")
    st.caption("Atrapa 15 bebés 👶 en 30 segundos 👇")
    juego_whack()

st.markdown("---")
st.caption("💙 Hecho con amor para la llegada de María 🎀")
