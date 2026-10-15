import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Revelación de Género",
    page_icon="🎀",
    layout="centered"
)

# ---------- Estilos globales ----------
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
    margin-bottom: 1.5rem;
  }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎀 Revelación de Género 💙</div>',
            unsafe_allow_html=True)
st.markdown('<div class="subtitle">Elige un juego para descubrir la sorpresa</div>',
            unsafe_allow_html=True)


# ============================================================
# OPCIÓN 1: RASCA Y GANA
# ============================================================
def juego_rasca():
    scratch_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      body { margin: 0; display: flex; flex-direction: column;
             align-items: center; font-family: sans-serif; background: #fff; }
      #wrap {
        position: relative; width: 320px; height: 220px;
        border-radius: 12px; overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,.15);
        touch-action: none;
      }
      #reveal {
        position: absolute; inset: 0;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        background: linear-gradient(135deg, #ffd1e3, #cfe4ff);
        color: #c2185b;
        text-align: center;
      }
      #reveal h1 { margin: 0; font-size: 40px; }
      #reveal p  { margin: 6px 0 0; font-size: 22px; color: #2a4d8f; }
      #cover {
        position: absolute; inset: 0;
        background: #b0b0b0;
        cursor: crosshair;
      }
    </style>
    </head>
    <body>
      <div id="wrap">
        <div id="reveal">
          <h1>🎀 ¡Es una niña! 🎀</h1>
          <p>María</p>
        </div>
        <canvas id="cover" width="320" height="220"></canvas>
      </div>

    <script>
      const canvas = document.getElementById('cover');
      const ctx = canvas.getContext('2d');
      let drawing = false;

      function paintCover() {
        ctx.fillStyle = '#b0b0b0';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#888';
        ctx.font = '16px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('Rasca aquí 👆', canvas.width/2, canvas.height/2);
      }
      paintCover();
      ctx.globalCompositeOperation = 'destination-out';

      function pos(e) {
        const r = canvas.getBoundingClientRect();
        const t = e.touches ? e.touches[0] : e;
        return { x: t.clientX - r.left, y: t.clientY - r.top };
      }

      function scratch(e) {
        if (!drawing) return;
        const { x, y } = pos(e);
        ctx.beginPath();
        ctx.arc(x, y, 22, 0, Math.PI * 2);
        ctx.fill();
        checkProgress();
      }

      function checkProgress() {
        const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
        let clear = 0;
        for (let i = 3; i < data.length; i += 4) if (data[i] < 40) clear++;
        if (clear / (canvas.width * canvas.height) > 0.55) {
          canvas.style.transition = 'opacity .6s';
          canvas.style.opacity = 0;
          setTimeout(() => canvas.style.display = 'none', 600);
        }
      }

      canvas.addEventListener('mousedown', e => { drawing = true; scratch(e); });
      canvas.addEventListener('mousemove', scratch);
      window.addEventListener('mouseup', () => drawing = false);

      canvas.addEventListener('touchstart', e => { e.preventDefault(); drawing = true; scratch(e); });
      canvas.addEventListener('touchmove',  e => { e.preventDefault(); scratch(e); });
      window.addEventListener('touchend', () => drawing = false);
    </script>
    </body>
    </html>
    """
    components.html(scratch_html, height=300)


# ============================================================
# OPCIÓN 2: MEMORAMA
# ============================================================
def juego_memorama():
    memory_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      body { margin: 0; display: flex; flex-direction: column;
             align-items: center; font-family: sans-serif; background: #fff; }
      #grid {
        display: grid; grid-template-columns: repeat(3, 90px);
        gap: 10px; margin-top: 10px;
      }
      .card {
        width: 90px; height: 90px; perspective: 600px; cursor: pointer;
      }
      .inner {
        position: relative; width: 100%; height: 100%;
        transition: transform .4s; transform-style: preserve-3d;
      }
      .card.flipped .inner, .card.matched .inner { transform: rotateY(180deg); }
      .face, .back {
        position: absolute; inset: 0; border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 34px; backface-visibility: hidden;
      }
      .face { background: linear-gradient(135deg,#cfe4ff,#ffd1e3); color: #fff; }
      .back { background: #9aa7b8; transform: rotateY(180deg); }
      #msg {
        margin-top: 20px; font-size: 22px; color: #c2185b;
        min-height: 30px; text-align: center;
      }
    </style>
    </head>
    <body>
      <div id="grid"></div>
      <div id="msg"></div>

    <script>
      const icons = ['💙','🎀','💙','🎀','⭐','⭐'];
      let first = null, lock = false, matched = 0;

      const grid = document.getElementById('grid');
      icons.sort(() => Math.random() - 0.5).forEach((icon) => {
        const c = document.createElement('div');
        c.className = 'card';
        c.innerHTML = `<div class="inner">
            <div class="face">?</div>
            <div class="back">${icon}</div>
          </div>`;
        c.onclick = () => flip(c);
        grid.appendChild(c);
      });

      function flip(card) {
        if (lock || card.classList.contains('flipped') ||
            card.classList.contains('matched')) return;
        card.classList.add('flipped');
        if (!first) { first = card; return; }
        if (first.querySelector('.back').textContent ===
            card.querySelector('.back').textContent) {
          first.classList.add('matched'); card.classList.add('matched');
          matched++; first = null;
          if (matched === 3) {
            document.getElementById('msg').innerHTML =
              '🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
          }
        } else {
          lock = true;
          setTimeout(() => {
            first.classList.remove('flipped');
            card.classList.remove('flipped');
            first = null; lock = false;
          }, 800);
        }
      }
    </script>
    </body>
    </html>
    """
    components.html(memory_html, height=420)


# ============================================================
# OPCIÓN 3: ROMPECABEZAS DESLIZANTE
# ============================================================
def juego_rompecabezas():
    puzzle_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      body { margin: 0; display: flex; flex-direction: column;
             align-items: center; font-family: sans-serif; background: #fff; }
      #board {
        display: grid;
        grid-template-columns: repeat(3, 110px);
        grid-template-rows: repeat(3, 110px);
        gap: 2px; background: #eee; padding: 4px;
        border-radius: 8px; touch-action: none; user-select: none;
      }
      .tile {
        background-size: 330px 330px;
        cursor: pointer; border-radius: 4px;
        transition: transform .15s;
      }
      .tile:hover { transform: scale(0.97); }
      .tile.empty { background: #fff; cursor: default; }
      #msg {
        margin-top: 18px; font-size: 22px; color: #c2185b;
        min-height: 30px; text-align: center;
      }
      button {
        margin-top: 10px; padding: 6px 16px; border: 1px solid #999;
        background: #fff; cursor: pointer; border-radius: 6px;
      }
    </style>
    </head>
    <body>
      <div id="board"></div>
      <div id="msg"></div>
      <button onclick="shuffleBoard()">Mezclar</button>

    <script>
      const SIZE = 3;
      const svg = `
        <svg xmlns='http://www.w3.org/2000/svg' width='330' height='330'>
          <defs>
            <linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>
              <stop offset='0' stop-color='#cfe4ff'/>
              <stop offset='1' stop-color='#ffd1e3'/>
            </linearGradient>
          </defs>
          <rect width='330' height='330' fill='url(%23g)'/>
          <text x='165' y='150' font-size='42' text-anchor='middle'
                font-family='sans-serif' fill='#c2185b'>🎀</text>
          <text x='165' y='200' font-size='30' text-anchor='middle'
                font-family='sans-serif' fill='#2a4d8f'>¡Es niña!</text>
          <text x='165' y='240' font-size='28' text-anchor='middle'
                font-family='sans-serif' font-weight='bold'
                fill='#c2185b'>María</text>
        </svg>`;
      const IMG = 'data:image/svg+xml;utf8,' + encodeURIComponent(svg);

      let board = [];
      let solved = false;

      function createSolved() {
        board = [];
        for (let i = 1; i < SIZE * SIZE; i++) board.push(i);
        board.push(0);
      }

      function shuffleBoard() {
        do {
          board = [...Array(SIZE * SIZE).keys()];
          for (let i = board.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [board[i], board[j]] = [board[j], board[i]];
          }
        } while (!isSolvable(board) || isSolved());
        solved = false;
        document.getElementById('msg').textContent = '';
        render();
      }

      function isSolvable(arr) {
        const a = arr.filter(x => x !== 0);
        let inv = 0;
        for (let i = 0; i < a.length; i++)
          for (let j = i + 1; j < a.length; j++)
            if (a[i] > a[j]) inv++;
        return inv % 2 === 0;
      }

      function isSolved() {
        for (let i = 0; i < SIZE * SIZE - 1; i++)
          if (board[i] !== i + 1) return false;
        return board[SIZE * SIZE - 1] === 0;
      }

      function render() {
        const b = document.getElementById('board');
        b.innerHTML = '';
        board.forEach((val, idx) => {
          const d = document.createElement('div');
          d.className = 'tile' + (val === 0 ? ' empty' : '');
          if (val !== 0) {
            const row = Math.floor((val - 1) / SIZE);
            const col = (val - 1) % SIZE;
            d.style.backgroundImage = `url("${IMG}")`;
            d.style.backgroundPosition = `-${col * 110}px -${row * 110}px`;
          }
          d.onclick = () => onClick(idx);
          b.appendChild(d);
        });
      }

      function onClick(idx) {
        if (solved) return;
        const empty = board.indexOf(0);
        const r1 = Math.floor(idx / SIZE), c1 = idx % SIZE;
        const r2 = Math.floor(empty / SIZE), c2 = empty % SIZE;
        if (Math.abs(r1 - r2) + Math.abs(c1 - c2) === 1) {
          [board[idx], board[empty]] = [board[empty], board[idx]];
          render();
          if (isSolved()) {
            solved = true;
            document.getElementById('msg').innerHTML =
              '🎀 ¡Es una niña! 🎀<br><strong>María</strong>';
          }
        }
      }

      createSolved();
      shuffleBoard();
    </script>
    </body>
    </html>
    """
    components.html(puzzle_html, height=520)


# ============================================================
# PESTAÑAS
# ============================================================
tab1, tab2, tab3 = st.tabs(["🎨 Rasca y Gana", "🃏 Memorama", "🧩 Rompecabezas"])

with tab1:
    st.subheader("Rasca para descubrir")
    st.caption("Pasa el mouse (o el dedo) sobre el recuadro gris 👇")
    juego_rasca()

with tab2:
    st.subheader("Encuentra las parejas")
    st.caption("Voltea las cartas y encuentra los 3 pares 👇")
    juego_memorama()

with tab3:
    st.subheader("Ordena el rompecabezas")
    st.caption("Haz click en las piezas junto al espacio vacío para moverlas 👇")
    juego_rompecabezas()

st.markdown("---")
st.caption("💙 Hecho con amor para la llegada de María 🎀")
