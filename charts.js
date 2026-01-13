function renderLine(canvasId, listData, saleData = null, label) {
  const canvas = document.getElementById(canvasId);
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const padding = 40;
  const width = canvas.width - padding * 2;
  const height = canvas.height - padding * 2;

  let max = Math.max(...listData);
  if(saleData) max = Math.max(max, ...saleData);
  let min = Math.min(...listData);
  if(saleData) min = Math.min(min, ...saleData);

  // Draw axes
  ctx.strokeStyle = "#ccc";
  ctx.beginPath();
  ctx.moveTo(padding, padding);
  ctx.lineTo(padding, canvas.height - padding);
  ctx.lineTo(canvas.width - padding, canvas.height - padding);
  ctx.stroke();

  // Draw median list line
  ctx.strokeStyle = "green";
  ctx.lineWidth = 2;
  ctx.beginPath();
  listData.forEach((v, i) => {
    const x = padding + (i * width) / (listData.length - 1);
    const y = canvas.height - padding - ((v - min) / (max - min)) * height;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();

  // Draw median sale line if exists
  if(saleData){
    ctx.strokeStyle = "blue";
    ctx.lineWidth = 2;
    ctx.beginPath();
    saleData.forEach((v, i) => {
      const x = padding + (i * width) / (saleData.length - 1);
      const y = canvas.height - padding - ((v - min) / (max - min)) * height;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
  }

  // Draw points
  ctx.fillStyle = "green";
  listData.forEach((v, i) => {
    const x = padding + (i * width) / (listData.length - 1);
    const y = canvas.height - padding - ((v - min) / (max - min)) * height;
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, Math.PI * 2);
    ctx.fill();
  });

  if(saleData){
    ctx.fillStyle = "blue";
    saleData.forEach((v, i) => {
      const x = padding + (i * width) / (saleData.length - 1);
      const y = canvas.height - padding - ((v - min) / (max - min)) * height;
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  // Chart title
  ctx.fillStyle = "#1e3a8a";
  ctx.font = "16px Arial";
  ctx.fillText(label, canvas.width / 2 - ctx.measureText(label).width / 2, 20);
}
