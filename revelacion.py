import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Revelación", page_icon="🎀")
st.title("💙 Rasca para descubrir 💗")
st.caption("Pasa el mouse (o el dedo) sobre el recuadro gris")

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
  let revealedPercent = 0;

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
    revealedPercent = clear / (canvas.width * canvas.height);
    if (revealedPercent > 0.55) {
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
