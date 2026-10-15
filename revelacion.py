import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Rompecabezas", page_icon="🧩")
st.title("🧩 Rompecabezas Deslizante")
st.write("Arrastra las piezas (o usa el dedo en móvil) para ordenar la imagen del 1 al 8.")

# HTML+CSS+JS embebido
puzzle_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  body {
    margin: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: sans-serif;
    background: #fafafa;
  }
  #board {
    display: grid;
    grid-template-columns: repeat(3, 100px);
    grid-template-rows: repeat(3, 100px);
    gap: 4px;
    background: #333;
    padding: 4px;
    border-radius: 8px;
    touch-action: none;
    user-select: none;
  }
  .tile {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    font-weight: bold;
    color: #fff;
    cursor: grab;
    border-radius: 6px;
    transition: transform 0.15s ease;
    touch-action: none;
  }
  .tile.selected {
    outline: 4px solid #ffd400;
    transform: scale(0.95);
  }
  .tile.empty {
    background: #1a1a1a !important;
    cursor: default;
  }
  #msg {
    margin-top: 20px;
    font-size: 22px;
    font-weight: bold;
    color: #06a77d;
    min-height: 30px;
    transition: opacity 0.4s;
  }
  button {
    margin-top: 12px;
    padding: 8px 20px;
    font-size: 16px;
    border-radius: 6px;
    border: none;
    background: #4c6ef5;
    color: white;
    cursor: pointer;
  }
  button:hover { background: #3b5bdb; }
  @keyframes confetti {
    0% { transform: translateY(0) rotate(0); opacity: 1; }
    100% { transform: translateY(-200px) rotate(720deg); opacity: 0; }
  }
  .confetti {
    position: fixed;
    width: 10px; height: 10px;
    animation: confetti 1.5s ease-out forwards;
  }
</style>
</head>
<body>
  <div id="board"></div>
  <div id="msg"></div>
  <button onclick="shuffleBoard()">🔀 Mezclar</button>

<script>
  const SIZE = 3;
  const COLORS = ['#e63946','#f1faee','#a8dadc','#457b9d','#1d3557',
                  '#ffb703','#fb8500','#8338ec','#06d6a0'];
  let board = [];
  let selected = null;
  let solved = false;

  function createSolved() {
    board = [];
    for (let i = 1; i < SIZE*SIZE; i++) board.push(i);
    board.push(0); // 0 = empty
  }

  function shuffleBoard() {
    do {
      board = [...Array(SIZE*SIZE).keys()]; // 0..8
      // Fisher-Yates
      for (let i = board.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [board[i], board[j]] = [board[j], board[i]];
      }
    } while (!isSolvable(board) || isSolved());
    selected = null;
    solved = false;
    document.getElementById('msg').textContent = '';
    render();
  }

  function isSolvable(arr) {
    // Cuenta inversiones
    const a = arr.filter(x => x !== 0);
    let inv = 0;
    for (let i = 0; i < a.length; i++)
      for (let j = i + 1; j < a.length; j++)
        if (a[i] > a[j]) inv++;
    return inv % 2 === 0;
  }

  function isSolved() {
    for (let i = 0; i < SIZE*SIZE - 1; i++)
      if (board[i] !== i + 1) return false;
    return board[SIZE*SIZE - 1] === 0;
  }

  function render() {
    const b = document.getElementById('board');
    b.innerHTML = '';
    board.forEach((val, idx) => {
      const d = document.createElement('div');
      d.className = 'tile' + (val === 0 ? ' empty' : '');
      d.style.background = val === 0 ? '#1a1a1a' : COLORS[(val-1) % COLORS.length];
      d.textContent = val === 0 ? '' : val;
      d.dataset.idx = idx;
      if (selected === idx) d.classList.add('selected');
      d.addEventListener('click', () => onClick(idx));
      b.appendChild(d);
    });
  }

  function onClick(idx) {
    if (solved) return;
    const emptyIdx = board.indexOf(0);
    const [r1, c1] = [Math.floor(idx/SIZE), idx % SIZE];
    const [r2, c2] = [Math.floor(emptyIdx/SIZE), emptyIdx % SIZE];
    const dist = Math.abs(r1 - r2) + Math.abs(c1 - c2);

    // Modo click: mueve si es adyacente al hueco
    if (dist === 1) {
      [board[idx], board[emptyIdx]] = [board[emptyIdx], board[idx]];
      selected = null;
      render();
      checkWin();
      return;
    }

    // Modo selección (por si el usuario quiere "arrastrar" tocando dos veces)
    if (selected === null) {
      selected = idx;
    } else if (selected === idx) {
      selected = null;
    } else {
      // Intento de intercambio (solo si uno es el hueco)
      if (selected === emptyIdx || idx === emptyIdx) {
        const a = selected, b = emptyIdx;
        [board[a], board[b]] = [board[b], board[a]];
        selected = null;
      } else {
        selected = idx;
      }
    }
    render();
    checkWin();
  }

  function checkWin() {
    if (isSolved()) {
      solved = true;
      const msg = document.getElementById('msg');
      msg.textContent = '🎉 ¡Felicidades! Rompecabezas resuelto 🎉';
      msg.style.color = '#06a77d';
      launchConfetti();
      // 👇 Enviar mensaje al padre (Streamlit) si quieres reaccionar en Python
      window.parent.postMessage({type: 'puzzle_solved'}, '*');
    }
  }

  function launchConfetti() {
    const colors = ['#e63946','#ffb703','#06d6a0','#4c6ef5','#8338ec'];
    for (let i = 0; i < 40; i++) {
      const c = document.createElement('div');
      c.className = 'confetti';
      c.style.left = Math.random() * 100 + 'vw';
      c.style.top = '60vh';
      c.style.background = colors[Math.floor(Math.random()*colors.length)];
      document.body.appendChild(c);
      setTimeout(() => c.remove(), 1600);
    }
  }

  createSolved();
  shuffleBoard();
</script>
</body>
</html>
"""

components.html(puzzle_html, height=520)

st.markdown("---")
st.caption("💡 También puedes reaccionar en Python al evento si integras un component custom.")
