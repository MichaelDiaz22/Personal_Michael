import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Rompecabezas", page_icon="🧩")
st.title("🧩 Rompecabezas")

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
    background: #ffffff;
    color: #222;
  }
  #board {
    display: grid;
    grid-template-columns: repeat(3, 90px);
    grid-template-rows: repeat(3, 90px);
    gap: 2px;
    background: #ddd;
    padding: 2px;
    touch-action: none;
    user-select: none;
  }
  .tile {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    background: #f0f0f0;
    cursor: pointer;
    touch-action: none;
  }
  .tile.empty {
    background: #ffffff;
    cursor: default;
  }
  #msg {
    margin-top: 16px;
    font-size: 18px;
    color: #2a7;
    min-height: 24px;
  }
  button {
    margin-top: 12px;
    padding: 6px 16px;
    font-size: 14px;
    border: 1px solid #999;
    background: #fff;
    cursor: pointer;
  }
</style>
</head>
<body>
  <div id="board"></div>
  <div id="msg"></div>
  <button onclick="shuffleBoard()">Mezclar</button>

<script>
  const SIZE = 3;
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
      d.textContent = val === 0 ? '' : val;
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
        document.getElementById('msg').textContent = '¡Resuelto!';
      }
    }
  }

  createSolved();
  shuffleBoard();
</script>
</body>
</html>
"""

components.html(puzzle_html, height=450)
