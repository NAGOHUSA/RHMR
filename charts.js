// Global tooltip
const tooltip = document.createElement('div');
tooltip.id = 'chart-tooltip';
tooltip.style.position = 'absolute';
tooltip.style.padding = '10px 14px';
tooltip.style.background = 'rgba(30, 41, 59, 0.95)';
tooltip.style.color = '#f1f5f9';
tooltip.style.borderRadius = '8px';
tooltip.style.pointerEvents = 'none';
tooltip.style.fontSize = '13px';
tooltip.style.display = 'none';
tooltip.style.zIndex = '1000';
tooltip.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
tooltip.style.border = '1px solid #334155';
tooltip.style.maxWidth = '250px';
tooltip.style.backdropFilter = 'blur(4px)';
document.body.appendChild(tooltip);

/**
 * Render a responsive line chart
 */
function renderLine(canvasId, listData, saleData = null, label) {
    const canvas = document.getElementById(canvasId);
    const ctx = canvas.getContext('2d');
    const container = canvas.parentElement;
    
    // Set responsive dimensions
    canvas.width = container.clientWidth - 60;
    canvas.height = 300;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    const padding = { top: 30, right: 30, bottom: 50, left: 60 };
    const width = canvas.width - padding.left - padding.right;
    const height = canvas.height - padding.top - padding.bottom;
    
    // Calculate min/max for scaling
    let max = Math.max(...listData);
    if(saleData) max = Math.max(max, ...saleData);
    let min = Math.min(...listData);
    if(saleData) min = Math.min(min, ...saleData);
    
    // Add some padding to Y axis
    const range = max - min;
    max += range * 0.1;
    min = Math.max(0, min - range * 0.1);
    
    // Draw grid
    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 1;
    
    // Vertical grid
    const xSteps = listData.length - 1;
    for(let i = 0; i <= xSteps; i++) {
        const x = padding.left + (i * width) / xSteps;
        ctx.beginPath();
        ctx.moveTo(x, padding.top);
        ctx.lineTo(x, canvas.height - padding.bottom);
        ctx.stroke();
    }
    
    // Horizontal grid
    const ySteps = 5;
    for(let i = 0; i <= ySteps; i++) {
        const y = padding.top + (i * height) / ySteps;
        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(canvas.width - padding.right, y);
        ctx.stroke();
        
        // Y axis labels
        const value = max - (i * (max - min)) / ySteps;
        ctx.fillStyle = '#64748b';
        ctx.font = '12px Arial';
        ctx.textAlign = 'right';
        ctx.fillText(
            label.includes('Price') ? `$${Math.round(value).toLocaleString()}` : Math.round(value).toLocaleString(),
            padding.left - 10,
            y + 4
        );
    }
    
    // Draw axes
    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(padding.left, padding.top);
    ctx.lineTo(padding.left, canvas.height - padding.bottom);
    ctx.lineTo(canvas.width - padding.right, canvas.height - padding.bottom);
    ctx.stroke();
    
    // X axis labels
    ctx.fillStyle = '#64748b';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    listData.forEach((_, i) => {
        const x = padding.left + (i * width) / (listData.length - 1);
        ctx.fillText(`Period ${i + 1}`, x, canvas.height - padding.bottom + 20);
    });
    
    // Store points for hover detection
    const points = [];
    
    // Draw median list line
    ctx.strokeStyle = '#10b981';
    ctx.lineWidth = 3;
    ctx.lineJoin = 'round';
    ctx.beginPath();
    
    listData.forEach((v, i) => {
        const x = padding.left + (i * width) / (listData.length - 1);
        const y = canvas.height - padding.bottom - ((v - min) / (max - min)) * height;
        points.push({
            x, y, value: v,
            type: 'Median List',
            period: i + 1,
            color: '#10b981'
        });
        
        if(i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();
    
    // Draw median sale line if exists
    if(saleData && saleData.length > 0) {
        ctx.strokeStyle = '#3b82f6';
        ctx.lineWidth = 3;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        
        saleData.forEach((v, i) => {
            const x = padding.left + (i * width) / (saleData.length - 1);
            const y = canvas.height - padding.bottom - ((v - min) / (max - min)) * height;
            points.push({
                x, y, value: v,
                type: 'Median Sale',
                period: i + 1,
                color: '#3b82f6'
            });
            
            if(i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.stroke();
        ctx.setLineDash([]);
    }
    
    // Draw points
    points.forEach(point => {
        ctx.fillStyle = point.color;
        ctx.beginPath();
        ctx.arc(point.x, point.y, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = 'white';
        ctx.lineWidth = 2;
        ctx.stroke();
    });
    
    // Chart title
    ctx.fillStyle = '#1e3a8a';
    ctx.font = 'bold 16px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(label, canvas.width / 2, 20);
    
    // Legend
    if(saleData && saleData.length > 0) {
        const legendY = 40;
        ctx.fillStyle = '#10b981';
        ctx.fillRect(canvas.width - 180, legendY, 12, 3);
        ctx.fillStyle = '#475569';
        ctx.font = '12px Arial';
        ctx.textAlign = 'left';
        ctx.fillText('List Price', canvas.width - 160, legendY + 8);
        
        ctx.fillStyle = '#3b82f6';
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.moveTo(canvas.width - 180, legendY + 20);
        ctx.lineTo(canvas.width - 168, legendY + 20);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = '#475569';
        ctx.fillText('Sale Price', canvas.width - 160, legendY + 23);
    }
    
    // Mouse interaction
    let activePoint = null;
    
    canvas.onmousemove = function(e) {
        const rect = canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;
        
        let hoveredPoint = null;
        let minDistance = 15;
        
        points.forEach(p => {
            const dx = p.x - mouseX;
            const dy = p.y - mouseY;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if(distance < minDistance) {
                minDistance = distance;
                hoveredPoint = p;
            }
        });
        
        if(hoveredPoint && hoveredPoint !== activePoint) {
            activePoint = hoveredPoint;
            
            tooltip.style.display = 'block';
            tooltip.style.left = `${e.clientX + 15}px`;
            tooltip.style.top = `${e.clientY - 50}px`;
            
            tooltip.innerHTML = `
                <div style="margin-bottom: 4px; font-weight: bold; color: ${hoveredPoint.color}">
                    ${hoveredPoint.type}
                </div>
                <div style="margin-bottom: 2px;">Period: <strong>${hoveredPoint.period}</strong></div>
                <div>Value: <strong>${label.includes('Price') ? '$' : ''}${hoveredPoint.value.toLocaleString()}</strong></div>
            `;
            
            // Highlight point
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            renderLine(canvasId, listData, saleData, label); // Re-render
            ctx.fillStyle = '#fbbf24';
            ctx.beginPath();
            ctx.arc(hoveredPoint.x, hoveredPoint.y, 8, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = hoveredPoint.color;
            ctx.lineWidth = 2;
            ctx.stroke();
        } else if(!hoveredPoint && activePoint) {
            activePoint = null;
            tooltip.style.display = 'none';
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            renderLine(canvasId, listData, saleData, label);
        }
    };
    
    canvas.onmouseleave = function() {
        tooltip.style.display = 'none';
        activePoint = null;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        renderLine(canvasId, listData, saleData, label);
    };
}

// Make function globally available
window.renderLine = renderLine;
