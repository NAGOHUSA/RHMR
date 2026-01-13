function renderLine(canvasId, data, label) {
  const canvas = document.getElementById(canvasId);
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const padding = 40;
  const width = canvas.width - padding * 2;
  const height = canvas.height - padding * 2;
  const max = Math.max(...data);
  const min = Math.min(...data);

  // Draw axes
  ctx.strokeStyle = "#ccc";
  ctx.beginPath();
  ctx.moveTo(padding, padding);
  ctx.lineTo(padding, canvas.height - padding);
  ctx.lineTo(canvas.width - padding, canvas.height - padding);
  ctx.stroke();

  // Plot line
  ctx.strokeStyle = "#1e3a8a";
  ctx.lineWidth = 2;
  ctx.beginPath();
  data.forEach((v, i) => {
    const x = padding + (i * width) / (data.length - 1);
    const y = canvas.height - padding - ((v - min) / (max - min)) * height;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();

  // Draw points + tooltips
  ctx.fillStyle = "#1e3a8a";
  data.forEach((v, i) => {
    const x = padding + (i * width) / (data.length - 1);
    const y = canvas.height - padding - ((v - min) / (max - min)) * height;
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, Math.PI * 2);
    ctx.fill();

    // Label
    ctx.fillStyle = "#333";
    ctx.font = "12px Arial";
    ctx.fillText(v.toLocaleString(), x - 15, y - 10);
    ctx.fillStyle = "#1e3a8a";
  });

  // Chart title
  ctx.fillStyle = "#1e3a8a";
  ctx.font = "16px Arial";
  ctx.fillText(label, canvas.width / 2 - ctx.measureText(label).width / 2, 20);
}
