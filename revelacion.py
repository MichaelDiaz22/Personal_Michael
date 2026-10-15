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
# 2. MEMORAMA (10 parejas)
# ============================================================
def juego_memorama():
    memory_html = f"""
    <!-- seed:{SEED} -->
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      html, body {{
        margin: 0; padding: 0;
        font-family: sans-serif;
        background: #fff;
        width: 100%;
      }}
      body {{
        display: flex; flex-direction: column; align-items: center;
        padding: 8px 0;
      }}
      #grid {{
        display: grid;
        grid-template-columns: repeat(5, 96px);
        grid-template-rows: repeat(4, 96px);
        gap: 10px;
        justify-content: center;
      }}
      .card {{
        width: 96px; height: 96px;
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
        font-size: 38px; backface-visibility: hidden;
        -webkit-backface-visibility: hidden;
      }}
      .face {{
        background: linear-gradient(135deg,#cfe4ff,#ffd1e3);
        color: #fff; font-size: 28px;
      }}
      .back {{
        background: #fff; border: 2px solid #cfe4ff;
        transform: rotateY(180deg);
      }}
      .card.matched .back {{ border-color: #ffb3d1; background: #fff0f7; }}
      #msg {{
        margin-top: 16px; font-size: 22px; color: #c2185b;
        min-height: 30px; text-align: center;
      }}
      #info {{ margin-top: 8px; color: #666; font-size: 14px; }}
      button {{
        margin-top: 12px; padding: 8px 22px; border: 1px solid #999;
        background: #fff; cursor: pointer; border-radius: 6px; font-size: 14px;
      }}
    </style>
    </head>
    <body>
      <div id="info">Parejas encontradas: <span id="pairs">0</span> / 10</div>
      <div id="grid"></div>
      <div id="msg"></div>
      <button onclick="reset()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      // 10 íconos únicos y visualmente distintos
      const ICONS = [
        '🎀','⭐','🌸','🍼','🧸','👶','🎈','🌷','💖','🦋'
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
          if (matched === 10 && !celebrated) {{
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
    components.html(memory_html, height=600)


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
# 5. BUSCA EL BEBÉ
# ============================================================
def juego_buscaminas():
    mines_html = f"""
    <!-- seed:{SEED} -->
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      body {{ margin: 0; display: flex; flex-direction: column;
             align-items: center; font-family: sans-serif; background: #fff; }}
      #grid {{
        display: grid; grid-template-columns: repeat(6, 60px);
        gap: 4px; margin-top: 10px;
      }}
      .cell {{
        width: 60px; height: 60px;
        background: linear-gradient(135deg,#cfe4ff,#ffd1e3);
        border-radius: 6px; cursor: pointer;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px; transition: transform .1s;
        user-select: none;
      }}
      .cell:active {{ transform: scale(0.94); }}
      .cell.safe {{ background: #f5f5f5; cursor: default; }}
      .cell.safe.bad {{ background: #ffe1e1; }}
      .cell.safe.good {{ background: #e2ffe9; }}
      #info {{ color: #666; font-size: 14px; margin-top: 8px; }}
      #msg {{
        margin-top: 14px; font-size: 24px; color: #c2185b;
        min-height: 40px; text-align: center; line-height: 1.3;
        font-weight: bold;
      }}
      #msg.error {{ color: #d32f2f; }}
      #msg.win   {{ color: #c2185b; }}
      button {{
        margin-top: 10px; padding: 8px 22px; border: 1px solid #999;
        background: #fff; cursor: pointer; border-radius: 6px; font-size: 14px;
      }}
    </style>
    </head>
    <body>
      <div id="info">
        Encuentra las 3 celdas con 👶 · Fallos restantes:
        <span id="lives">10</span>
      </div>
      <div id="grid"></div>
      <div id="msg"></div>
      <button onclick="reset()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      const COLS = 6, ROWS = 5;
      const TOTAL = COLS * ROWS;
      const GIFTS = 3;
      const MAX_ERRORS = 10;
      let grid, lives, found, done, celebrated;

      const gridEl = document.getElementById('grid');
      const livesEl = document.getElementById('lives');
      const msg = document.getElementById('msg');

      function randInt(max) {{
        const buf = new Uint32Array(1);
        crypto.getRandomValues(buf);
        return buf[0] % max;
      }}

      function reset() {{
        grid = Array(TOTAL).fill(false);
        let placed = 0;
        while (placed < GIFTS) {{
          const i = randInt(TOTAL);
          if (!grid[i]) {{ grid[i] = true; placed++; }}
        }}
        lives = MAX_ERRORS;
        found = 0;
        done = false;
        celebrated = false;
        livesEl.textContent = lives;
        msg.innerHTML = '';
        msg.className = '';
        render();
      }}

      function render() {{
        gridEl.innerHTML = '';
        for (let i = 0; i < TOTAL; i++) {{
          const c = document.createElement('div');
          c.className = 'cell';
          c.dataset.idx = i;
          c.onclick = () => reveal(i, c);
          gridEl.appendChild(c);
        }}
      }}

      function reveal(i, el) {{
        if (done || el.classList.contains('safe')) return;
        el.classList.add('safe');

        if (grid[i]) {{
          el.classList.add('good');
          el.textContent = '👶';
          found++;

          if (found === GIFTS) {{
            done = true;
            msg.className = 'win';
            msg.innerHTML = '🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
            if (!celebrated) {{
              celebrated = true;
              setTimeout(() => celebrate(), 250);
            }}
          }}
        }} else {{
          el.classList.add('bad');
          el.textContent = '✖';
          lives--;
          livesEl.textContent = lives;

          if (lives <= 0) {{
            done = true;
            msg.className = 'error';
            msg.innerHTML = '❌ ¡Se acabaron los intentos!<br>Vuelve a empezar...';
            setTimeout(() => reset(), 2000);
          }}
        }}
      }}

      reset();
    </script>
    </body>
    </html>
    """
    components.html(mines_html, height=600)


# ============================================================
# 6. TRIQUI
# ============================================================
def juego_triqui():
    triqui_html = f"""
    <!-- seed:{SEED} -->
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      body {{ margin: 0; display: flex; flex-direction: column;
             align-items: center; font-family: sans-serif; background: #fff;
             padding: 10px; }}
      #board {{
        display: grid;
        grid-template-columns: repeat(3, 100px);
        grid-template-rows: repeat(3, 100px);
        gap: 6px; background: #cfe4ff; padding: 6px;
        border-radius: 12px;
      }}
      .cell {{
        width: 100px; height: 100px;
        background: #fff; border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 52px; font-weight: bold;
        cursor: pointer; user-select: none;
        transition: transform .12s;
      }}
      .cell:hover {{ transform: scale(1.04); }}
      .cell.x {{ color: #2a4d8f; }}
      .cell.o {{ color: #c2185b; }}
      .cell.win {{ background: #ffeaa7; }}
      #msg {{
        margin-top: 14px; font-size: 22px; color: #2a4d8f;
        min-height: 34px; text-align: center; font-weight: bold;
      }}
      #msg.error {{ color: #d32f2f; }}
      #msg.draw  {{ color: #e67e22; }}
      #msg.win   {{ color: #c2185b; }}
      button {{
        margin-top: 10px; padding: 8px 22px; border: 1px solid #999;
        background: #fff; cursor: pointer; border-radius: 6px; font-size: 14px;
      }}
    </style>
    </head>
    <body>
      <div id="board"></div>
      <div id="msg"></div>
      <button onclick="reset()">🔄 Reiniciar</button>

    {CELEBRATION_SCRIPT}

    <script>
      const USER = 'X';
      const CPU  = 'O';
      const WINS = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
      ];
      let board, done, celebrated;

      const boardEl = document.getElementById('board');
      const msg = document.getElementById('msg');

      function randInt(max) {{
        const buf = new Uint32Array(1);
        crypto.getRandomValues(buf);
        return buf[0] % max;
      }}

      function reset() {{
        board = Array(9).fill('');
        done = false;
        celebrated = false;
        msg.className = '';
        msg.innerHTML = 'Tu turno — juegas con ❌';
        render();
      }}

      function render() {{
        boardEl.innerHTML = '';
        board.forEach((v, i) => {{
          const c = document.createElement('div');
          c.className = 'cell' + (v ? ' ' + v.toLowerCase() : '');
          c.textContent = v;
          c.onclick = () => play(i);
          boardEl.appendChild(c);
        }});
      }}

      function winner(b) {{
        for (const line of WINS) {{
          const [a, c, d] = line;
          if (b[a] && b[a] === b[c] && b[a] === b[d])
            return {{ player: b[a], line: line }};
        }}
        if (b.every(x => x)) return {{ player: 'draw', line: [] }};
        return null;
      }}

      function highlight(line) {{
        [...boardEl.children].forEach((el, i) => {{
          if (line.includes(i)) el.classList.add('win');
        }});
      }}

      function play(i) {{
        if (done || board[i]) return;
        board[i] = USER;
        render();
        let w = winner(board);
        if (w) return finish(w);
        msg.innerHTML = 'Turno de la CPU...';
        setTimeout(cpuMove, 350);
      }}

      function bestMove(player) {{
        for (const line of WINS) {{
          const vals = line.map(i => board[i]);
          const countP = vals.filter(v => v === player).length;
          const countEmpty = vals.filter(v => v === '').length;
          if (countP === 2 && countEmpty === 1) {{
            return line[vals.indexOf('')];
          }}
        }}
        return null;
      }}

      function cpuMove() {{
        if (done) return;
        let move = bestMove(CPU);
        if (move === null) move = bestMove(USER);
        if (move === null && board[4] === '') move = 4;
        if (move === null) {{
          const corners = [0,2,6,8].filter(i => board[i] === '');
          if (corners.length) {{
            if (Math.random() < 0.7) {{
              move = corners[randInt(corners.length)];
            }}
          }}
        }}
        if (move === null) {{
          const libres = board.map((v,i) => v === '' ? i : -1).filter(i => i >= 0);
          move = libres[randInt(libres.length)];
        }}
        board[move] = CPU;
        render();
        let w = winner(board);
        if (w) return finish(w);
        msg.innerHTML = 'Tu turno — juegas con ❌';
      }}

      function finish(w) {{
        done = true;
        if (w.player === 'draw') {{
          msg.className = 'draw';
          msg.innerHTML = '😅 Empate... intenta de nuevo';
          return;
        }}
        highlight(w.line);
        if (w.player === USER) {{
          msg.className = 'win';
          msg.innerHTML = '🎉 ¡Ganaste! 🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
          if (!celebrated) {{
            celebrated = true;
            setTimeout(() => celebrate(), 300);
          }}
        }} else {{
          msg.className = 'error';
          msg.innerHTML = '❌ Perdiste... inténtalo otra vez';
        }}
      }}

      reset();
    </script>
    </body>
    </html>
    """
    components.html(triqui_html, height=600)


# ============================================================
# 7. ACRÓSTICO
# ============================================================
def juego_acrostico():
    acrostico_html = f"""
    <!-- seed:{SEED} -->
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      body {{ margin: 0; display: flex; flex-direction: column;
             align-items: center; font-family: sans-serif; background: #fff;
             padding: 16px; }}
      #intro {{
        max-width: 560px; text-align: center;
        color: #555; font-size: 15px; margin-bottom: 12px;
      }}
      #acrostic {{
        display: flex; flex-direction: column; gap: 12px;
        width: 100%; max-width: 560px;
      }}
      .row {{
        display: flex; align-items: flex-start; gap: 12px;
        background: #f9fafc; padding: 10px 14px;
        border-radius: 10px; border-left: 4px solid #cfe4ff;
      }}
      .letter {{
        font-size: 36px; font-weight: 900;
        width: 44px; text-align: center;
        background: linear-gradient(90deg,#c2185b,#2a4d8f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        flex-shrink: 0;
      }}
      .content {{ flex: 1; }}
      .question {{
        font-size: 15px; color: #333; margin-bottom: 6px;
      }}
      .answer-row {{
        display: flex; gap: 8px; align-items: center;
      }}
      input {{
        flex: 1; padding: 8px 12px; font-size: 15px;
        border: 1px solid #cfe4ff; border-radius: 6px;
        outline: none; transition: border .2s;
      }}
      input:focus {{ border-color: #c2185b; }}
      input.ok {{ border-color: #06a77d; background: #f0fff8; }}
      input.bad {{ border-color: #d32f2f; background: #fff5f5; }}
      .status {{
        font-size: 18px; width: 22px; text-align: center;
      }}
      #msg {{
        margin-top: 18px; font-size: 22px; color: #c2185b;
        min-height: 34px; text-align: center; font-weight: bold;
      }}
      #msg.error {{ color: #d32f2f; }}
      button {{
        margin-top: 12px; padding: 8px 22px; border: 1px solid #999;
        background: #fff; cursor: pointer; border-radius: 6px; font-size: 14px;
      }}
      #check {{
        background: #c2185b; color: #fff; border-color: #c2185b;
        font-weight: bold;
      }}
    </style>
    </head>
    <body>
      <div id="intro">
        Resuelve el siguiente acróstico. Cada respuesta empieza con la
        letra de la columna izquierda. ¡Si aciertas todas, verás el nombre!
      </div>
      <div id="acrostic"></div>
      <div style="display:flex; gap:10px; margin-top:14px;">
        <button id="check" onclick="checkAll()">✅ Comprobar</button>
        <button onclick="reset()">🔄 Reiniciar</button>
      </div>
      <div id="msg"></div>

    {CELEBRATION_SCRIPT}

    <script>
      const DATA = [
        {{ letter: 'M', q: 'Fruto rojo pequeño y dulce, típico del verano.',
           a: 'mora',
           hint: 'Empieza con M, tiene 4 letras' }},
        {{ letter: 'A', q: 'Ave rapaz que vuela alto y caza.',
           a: 'aguila',
           hint: 'Empieza con A, 6 letras' }},
        {{ letter: 'R', q: 'Animal pequeño con orejas largas y salta.',
           a: 'rana',
           hint: 'Empieza con R, 4 letras' }},
        {{ letter: 'I', q: 'Isla pequeña en medio del mar.',
           a: 'isla',
           hint: 'Empieza con I, 4 letras' }},
        {{ letter: 'A', q: 'Ave nocturna que gira la cabeza 180°.',
           a: 'ave',
           hint: 'Empieza con A, 3 letras' }}
      ];

      const container = document.getElementById('acrostic');
      const msg = document.getElementById('msg');
      let solved = false;

      function normalize(s) {{
        return s.trim().toLowerCase()
          .normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');
      }}

      function build() {{
        container.innerHTML = '';
        msg.innerHTML = '';
        msg.className = '';
        solved = false;
        DATA.forEach((item, i) => {{
          const row = document.createElement('div');
          row.className = 'row';
          row.innerHTML = `
            <div class="letter">${{item.letter}}</div>
            <div class="content">
              <div class="question">${{item.q}}<br>
                <small style="color:#888">${{item.hint}}</small>
              </div>
              <div class="answer-row">
                <input type="text" id="in${{i}}" placeholder="Tu respuesta..."
                       autocomplete="off" />
                <div class="status" id="st${{i}}"></div>
              </div>
            </div>`;
          container.appendChild(row);
        }});
      }}

      function checkAll() {{
        if (solved) return;
        let allOk = true;
        DATA.forEach((item, i) => {{
          const input = document.getElementById('in' + i);
          const status = document.getElementById('st' + i);
          const val = normalize(input.value);
          const ok = val === item.a;
          input.classList.remove('ok', 'bad');
          input.classList.add(ok ? 'ok' : 'bad');
          status.textContent = ok ? '✅' : '❌';
          if (!ok) allOk = false;
        }});
        if (allOk) {{
          solved = true;
          msg.className = '';
          msg.innerHTML = '🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
          setTimeout(() => celebrate(), 250);
        }} else {{
          msg.className = 'error';
          msg.innerHTML = '❌ Algunas respuestas no son correctas. ¡Inténtalo otra vez!';
        }}
      }}

      function reset() {{ build(); }}
      build();
    </script>
    </body>
    </html>
    """
    components.html(acrostico_html, height=680)


# ============================================================
# PESTAÑAS
# ============================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🎨 Rasca y Gana",
    "🃏 Memorama",
    "🧩 Rompecabezas",
    "🎈 Globo Sorpresa",
    "👶 Busca el Bebé",
    "⭕ Triqui",
    "🔤 Acróstico"
])

with tab1:
    st.subheader("Rasca para descubrir")
    st.caption("Rasca el recuadro al menos **10 segundos** y cubre el 55% para revelar 👇")
    juego_rasca()

with tab2:
    st.subheader("Encuentra las 10 parejas")
    st.caption("Voltea las cartas y encuentra los 10 pares 👇")
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
    st.subheader("Encuentra a los bebés")
    st.caption("Encuentra 3 👶 antes de agotar los 10 fallos. Si pierdes, se reinicia 👇")
    juego_buscaminas()

with tab6:
    st.subheader("Juega Triqui (Tres en línea)")
    st.caption("Tú juegas con ❌. Debes **ganar** para ver la revelación. Si pierdes o empatas, se reinicia 👇")
    juego_triqui()

with tab7:
    st.subheader("Resuelve el acróstico")
    st.caption("Contesta las 5 preguntas. Las iniciales forman un nombre secreto 👇")
    juego_acrostico()

st.markdown("---")
st.caption("💙 Hecho con amor para la llegada de María 🎀")
