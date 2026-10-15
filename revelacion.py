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
# 2. MEMORAMA (15 parejas, layout responsivo)
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
        width: 100%;
        height: 100%;
        perspective: 600px;
        cursor: pointer;
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
        margin-top: 14px; font-size: min(22px, 5vw); color: #c2185b;
        min-height: 30px; text-align: center;
      }}
      #info {{
        margin-top: 6px;
        color: #666;
        font-size: min(14px, 3.5vw);
      }}
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
            msg.innerHTML = '🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
            setTimeout(() => celebrate(), 250);
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
      const COLORS = [
        '#e63946','#f77f00','#fcbf49','#06a77d','#4c6ef5',
        '#8338ec','#ff6b9d','#00b4d8'
      ];
      let board = [];
      let solved = false;

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
      <div id="stage">
        <div id="balloon"></div>
      </div>
      <div id="hint">Haz clic/toque el globo para inflarlo (necesitas ~20 toques)</div>
      <div id="msg"></div>
      <button onclick="reset()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      const balloon = document.getElementById('balloon');
      const hint = document.getElementById('hint');
      const msg = document.getElementById('msg');
      const NEED = 20;
      let count = 0;
      let done = false;

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
# 5. TRIQUI DE BOMBAS (5 rosas / 4 azules, siempre triki rosa)
# ============================================================
def juego_triqui_bombas():
    bombitas_html = f"""
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
        padding: 10px 4px; box-sizing: border-box;
      }}
      #title {{
        color: #c2185b;
        font-weight: bold;
        font-size: min(18px, 4.5vw);
        margin-bottom: 6px;
        text-align: center;
      }}
      #info {{
        color: #666;
        font-size: min(13px, 3.5vw);
        text-align: center;
        max-width: 480px;
        margin-bottom: 10px;
      }}
      #board {{
        display: grid;
        grid-template-columns: repeat(3, min(110px, 26vw));
        grid-template-rows: repeat(3, min(110px, 26vw));
        gap: min(10px, 2.5vw);
        background: #f0f4ff;
        padding: min(10px, 2.5vw);
        border-radius: 16px;
        touch-action: manipulation;
      }}
      .bomb {{
        width: 100%;
        height: 100%;
        border-radius: 50% 50% 50% 50% / 55% 55% 45% 45%;
        background: radial-gradient(circle at 32% 28%, #ffffff, #ececec 70%, #d8d8d8);
        box-shadow: inset -4px -6px 10px rgba(0,0,0,.08),
                    0 3px 8px rgba(0,0,0,.12);
        cursor: pointer;
        position: relative;
        transition: transform .15s ease, box-shadow .25s ease, background .35s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: min(38px, 9vw);
        user-select: none;
      }}
      .bomb::after {{
        content: '';
        position: absolute;
        bottom: -12%;
        left: 50%;
        transform: translateX(-50%);
        width: 12%;
        height: 18%;
        background: #bbb;
        clip-path: polygon(50% 0, 100% 100%, 0 100%);
      }}
      .bomb:hover:not(.pink):not(.blue) {{
        transform: scale(1.05);
      }}
      .bomb:active:not(.pink):not(.blue) {{
        transform: scale(0.95);
      }}
      .bomb.pink {{
        background: radial-gradient(circle at 32% 28%, #ffd1e3, #ff6b9d 65%, #c2185b);
        box-shadow: inset -4px -6px 12px rgba(0,0,0,.15),
                    0 0 20px rgba(255,107,157,.55);
        cursor: default;
      }}
      .bomb.blue {{
        background: radial-gradient(circle at 32% 28%, #cfe4ff, #4c6ef5 65%, #2a4d8f);
        box-shadow: inset -4px -6px 12px rgba(0,0,0,.15),
                    0 0 20px rgba(76,110,245,.5);
        cursor: default;
      }}
      .bomb.win {{
        animation: pop 0.6s ease-out;
      }}
      @keyframes pop {{
        0%   {{ transform: scale(1); }}
        50%  {{ transform: scale(1.18); }}
        100% {{ transform: scale(1); }}
      }}
      #msg {{
        margin-top: 16px; font-size: min(22px, 5vw); font-weight: bold;
        min-height: 40px; text-align: center; line-height: 1.3;
        color: #2a4d8f; max-width: 480px;
      }}
      #msg.win   {{ color: #c2185b; }}
      #msg.info  {{ color: #2a4d8f; }}
      #counter {{
        margin-top: 8px;
        color: #666;
        font-size: min(14px, 3.6vw);
      }}
      button {{
        margin-top: 12px; padding: 8px 22px;
        border: 1px solid #999; background: #fff;
        border-radius: 6px; cursor: pointer;
        font-size: min(14px, 3.6vw);
      }}
    </style>
    </head>
    <body>
      <div id="title">💗 Presiona las bombas blancas y encuentra el triki rosa 💗</div>
      <div id="info">
        Hay <b>5 rosas</b> y <b>4 azules</b>. Las rosas forman
        <b>3 en línea</b> — ¡descúbrelas todas para ganar!
      </div>
      <div id="board" style="margin-top:12px;"></div>
      <div id="msg" class="info">Presiona una bomba blanca ⚪</div>
      <div id="counter">Bombas reveladas: <span id="rev">0</span> / 9</div>
      <button onclick="reset()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      const TOTAL = 9;
      const PINK_COUNT = 5;
      const BLUE_COUNT = 4;

      const WINS = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
      ];

      let colors = [];
      let revealed = [];
      let winningLine = [];
      let done = false;
      let celebrated = false;

      const boardEl = document.getElementById('board');
      const msg = document.getElementById('msg');
      const revEl = document.getElementById('rev');

      function randInt(max) {{
        const buf = new Uint32Array(1);
        crypto.getRandomValues(buf);
        return buf[0] % max;
      }}

      function generateBoard() {{
        // 1. Elegir una línea ganadora aleatoria
        const line = WINS[randInt(WINS.length)];
        winningLine = line;

        // 2. Marcar esas 3 celdas como rosas obligatorias
        colors = Array(TOTAL).fill(null);
        line.forEach(i => colors[i] = 'pink');

        // 3. Las 2 rosas restantes van a celdas aleatorias de las 6 libres
        const remaining = [];
        for (let i = 0; i < TOTAL; i++) if (colors[i] === null) remaining.push(i);

        // Barajar las celdas libres
        for (let i = remaining.length - 1; i > 0; i--) {{
          const j = randInt(i + 1);
          [remaining[i], remaining[j]] = [remaining[j], remaining[i]];
        }}

        // Primeras 2 → rosas
        remaining.slice(0, 2).forEach(i => colors[i] = 'pink');
        // Las 4 restantes → azules
        remaining.slice(2).forEach(i => colors[i] = 'blue');

        // 4. Verificación: exactamente 5 rosas y 4 azules
        const pinks = colors.filter(c => c === 'pink').length;
        const blues = colors.filter(c => c === 'blue').length;
        console.assert(pinks === 5 && blues === 4,
          'Error de reparto: pinks=' + pinks + ' blues=' + blues);
      }}

      function reset() {{
        generateBoard();
        revealed = Array(TOTAL).fill(false);
        done = false;
        celebrated = false;
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

      function reveal(i) {{
        if (done || revealed[i]) return;
        revealed[i] = true;

        const count = revealed.filter(x => x).length;
        revEl.textContent = count;

        render();

        // Verificar si las 3 celdas de la línea ganadora están reveladas
        const lineComplete = winningLine.every(idx => revealed[idx]);

        if (lineComplete && !done) {{
          done = true;
          // Resaltar la línea ganadora
          [...boardEl.children].forEach((el, idx) => {{
            if (winningLine.includes(idx)) el.classList.add('win');
          }});
          msg.className = 'win';
          msg.innerHTML = '🎉 ¡Tres rosas en línea! 🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
          if (!celebrated) {{
            celebrated = true;
            setTimeout(() => celebrate(), 400);
          }}
        }} else if (count < TOTAL) {{
          const missing = winningLine.filter(idx => !revealed[idx]).length;
          msg.className = 'info';
          msg.innerHTML = `¡Sigue! Faltan <b>${{missing}}</b> rosa${{missing > 1 ? 's' : ''}} por descubrir del triki 👀`;
        }} else {{
          msg.className = 'info';
          msg.innerHTML = '😅 Algo salió mal, presiona Reiniciar';
        }}
      }}

      reset();
    </script>
    </body>
    </html>
    """
    components.html(bombitas_html, height=620)


# ============================================================
# PESTAÑAS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎨 Rasca y Gana",
    "🃏 Memorama",
    "🧩 Rompecabezas",
    "🎈 Globo Sorpresa",
    "💗 Triqui de Bombas"
])

with tab1:
    st.subheader("Rasca para descubrir")
    st.caption("Rasca el recuadro al menos **10 segundos** y cubre el 55% para revelar 👇")
    juego_rasca()

with tab2:
    st.subheader("Encuentra las 15 parejas")
    st.caption("Voltea las cartas y encuentra los 15 pares 👇")
    juego_memorama()

with tab3:
    st.subheader("Ordena el rompecabezas")
    st.caption("Haz click en las piezas junto al espacio vacío. Ordena del 1 al 8 👇")
    juego_rompecabezas()

with tab4:
    st.subheader("Infla el globo")
    st.caption("Haz click/toque el globo unas 20 veces para que explote 👇")
    juego_globo()

with tab5:
    st.subheader("Triqui de Bombas")
    st.caption("Presiona bombas blancas ⚪ hasta descubrir **3 rosas 💗 en línea** 👇")
    juego_triqui_bombas()

st.markdown("---")
st.caption("💙 Hecho con amor para la llegada de María 🎀")
