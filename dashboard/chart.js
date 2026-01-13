function renderLine(canvasId, data) {
  const canvas = document.getElementById(canvasId);
  const ctx = canvas.getContext('2d');

  const max = Math.max(...data);
  const min = Math.min(...data);

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
  ctx.strokeStyle = "#1e3a8a";
  ctx.lineWidth = 2;

  data.forEach((v, i) => {
    const x = i * (canvas.width / (data.length - 1));
    const y = canvas.height - ((v - min) / (max - min)) * canvas.height;

    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });

  ctx.stroke();
}
