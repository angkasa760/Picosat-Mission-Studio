const canvas = document.createElement('canvas');
canvas.id = 'waterfall-canvas';
const ctx = canvas.getContext('2d');
const container = document.getElementById('plotly-chart').parentElement; // Place near chart
container.appendChild(canvas);

canvas.width = container.clientWidth;
canvas.height = 300;

const scrollSpeed = 2;
const rows = canvas.height / scrollSpeed;
const cols = canvas.width;
let data = new Uint8Array(cols);

function drawWaterfall() {
    // Copy pixels down
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height - scrollSpeed);
    ctx.putImageData(imageData, 0, scrollSpeed);

    // Generate new top row
    for(let i=0; i<cols; i++) {
        // Base noise
        let val = Math.random() * 50;
        
        // Signal simulation (UHF Peak at 437.2 MHz)
        const center = cols / 2;
        const drift = 50 * Math.sin(Date.now() * 0.001); // Doppler sim
        const dist = Math.abs(i - (center + drift));
        if(dist < 5) val += 200; // Strong signal
        else if(dist < 15) val += 100; // Sidebands
        
        data[i] = val;
    }

    // Draw new row
    for(let i=0; i<cols; i++) {
        const val = data[i];
        ctx.fillStyle = `rgb(${val/5}, ${val}, ${val/2})`;
        ctx.fillRect(i, 0, 1, scrollSpeed);
    }

    requestAnimationFrame(drawWaterfall);
}

// Handle resize
window.addEventListener('resize', () => {
    canvas.width = container.clientWidth;
});

drawWaterfall();
console.log("SDR Waterfall Active.");
