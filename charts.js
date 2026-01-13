// Create a global tooltip div
const tooltip = document.createElement('div');
tooltip.style.position = 'absolute';
tooltip.style.padding = '6px 10px';
tooltip.style.background = 'rgba(0,0,0,0.7)';
tooltip.style.color = '#fff';
tooltip.style.borderRadius = '4px';
tooltip.style.pointerEvents = 'none';
tooltip.style.fontSize = '14px';
tooltip.style.display = 'none';
document.body.appendChild(tooltip);

/**
 * Render a line chart on canvas with hover tooltips.
 * listData: median list or inventory
 * saleData: median sale (optional)
 * label: chart title
 */
function renderLine(canvasId, listData, saleData = null, label) {
  const canvas = document.getElementById(canvasId);
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const padding = 40;
  const width = canvas.width - padding * 2;
  const height = canvas.height - padding * 2;

  // Determine min/max for scaling
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

  // Store points for tooltip detection
  const points = [];

  // Draw median list line
  ctx.strokeStyle = "green";
  ctx.lineWidth = 2;
  ctx.beginPath();
  listData.forEach((v, i) => {
    const x = padding + (i * width) / (listData.length - 1);
    const y = canvas.height - padding - ((v - min) / (max - min)) * height;
    points.push({x, y, value: v, type: 'List', period: i + 1});
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
      points.push({x, y, value: v, type: 'Sale', period: i + 1});
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
  }

  // Draw points for median list
  ctx.fillStyle = "green";
  listData.forEach((v, i) => {
    const x = padding + (i * width) / (listData.length - 1);
    const y = canvas.height - padding - ((v - min) / (max - min)) * height;
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, Math.PI * 2);
    ctx.fill();
  });

  // Draw points for sale
  if(saleData){
    ctx.fillStyle = "blue";
    saleData.forEach((v, i) => {
      const x = padding + (i * width) / (saleData.length - 1);
      const y = canvas.height - padding - ((v - min) / (max - min)) * height;
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  // Draw points for inventory with color based on trend
  if(label.toLowerCase().includes('inventory')) {
    ctx.fillStyle = "gray"; // default first point
    listData.forEach((v, i) => {
      const x = padding + (i * width) / (listData.length - 1);
      const y = canvas.height - padding - ((v - min) / (max - min)) * height;
      if(i > 0){
        const prev = listData[i-1];
        if(v > prev) ctx.fillStyle = "green";       // rising
        else if(v < prev) ctx.fillStyle = "red";    // falling
        else ctx.fillStyle = "gray";                // flat
      }
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.fill();
      points.push({x, y, value: v, type: 'Inventory', period: i + 1});
    });
  }

  // Chart title
  ctx.fillStyle = "#1e3a8a";
  ctx.font = "16px Arial";
  ctx.fillText(label, canvas.width / 2 - ctx.measureText(label).width / 2, 20);

  // Mousemove for tooltip
  canvas.onmousemove = function(e) {
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    let found = false;

    points.forEach(p => {
      const dx = p.x - mouseX;
      const dy = p.y - mouseY;
      if(Math.sqrt(dx*dx + dy*dy) < 6) { // hover radius
        tooltip.style.display = 'block';
        tooltip.style.left = (e.clientX + 10) + 'px';
        tooltip.style.top = (e.clientY + 10) + 'px';
        if(p.type === 'Inventory')
          tooltip.innerHTML = `${p.type} (Period ${p.period}): ${p.value}`;
        else
          tooltip.innerHTML = `${p.type} (Period ${p.period}): $${p.value.toLocaleString()}`;
        found = true;
      }
    });

    if(!found) tooltip.style.display = 'none';
  };

  canvas.onmouseleave = function() {
    tooltip.style.display = 'none';
  };
}
