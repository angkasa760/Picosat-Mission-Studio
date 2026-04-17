// --- MISSION DATA ENGINE ---
let missionData = {
    frequency_target_mhz: 437.2,
    s11_simulated_db: -20.5,
    gain_dbi: 2.06,
    bandwidth_10db_mhz: 38.0
};

// 1. Initial Mission Specs Sync
fetch('../mission_data.json')
    .then(r => r.json())
    .then(data => {
        missionData = data;
        initS11Chart();
    });

// 2. LIVE TELEMETRY LOOP (Physics from Tracker)
function pollLiveTelemetry() {
    fetch('live_coords.json')
        .then(r => r.json())
        .then(data => {
            // Update UI Elements
            const marginEl = document.getElementById('margin');
            if (marginEl) {
                const margin = data.live_link_margin;
                marginEl.innerText = margin > -90 ? `${margin > 0 ? '+' : ''}${margin.toFixed(1)} dB` : "OFF-LINK";
                marginEl.className = margin > 0 ? 'green-text' : 'red-text';
            }

            // Sunlight Status
            const sunlit = data.is_sunlit;
            document.body.style.borderColor = sunlit ? '#ffd700' : '#1a2a3a';
            
            // Battery Sync
            const batteryEl = document.getElementById('rx-power'); // Reuse slot for SoC
            if (batteryEl) {
                batteryEl.innerText = `SoC: ${data.battery_soc}%`;
            }
        });
}

setInterval(pollLiveTelemetry, 5000);

function initS11Chart() {
    // Generate resonance curve matched to CST report
    const peak_f = missionData.frequency_target_mhz;
    const peak_s11 = missionData.s11_simulated_db;
    const bw = missionData.bandwidth_10db_mhz;

    const freqs = [];
    const vals = [];
    for(let f = peak_f - 40; f <= peak_f + 40; f += 2) {
        freqs.push(f);
        const v = -2.0 + (peak_s11 + 2.0) / (1 + Math.pow((f - peak_f)/(bw/4), 2));
        vals.push(v);
    }

    const trace = {
        x: freqs, y: vals,
        mode: 'lines',
        line: { color: '#00f2ff', width: 3, shape: 'spline' },
        fill: 'tozeroy',
        fillcolor: 'rgba(0, 242, 255, 0.1)'
    };

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#8892b0', family: 'Roboto Mono' },
        margin: { t: 30, r: 20, l: 40, b: 40 },
        xaxis: { title: 'Frequency (MHz)', gridcolor: '#1a2a3a' },
        yaxis: { title: 'S11 (dB)', gridcolor: '#1a2a3a' }
    };

    Plotly.newPlot('plotly-chart', [trace], layout);
}

// --- Jakarta Pass Map ---
function initMap() {
    const jakartaPos = [-6.2088, 106.8456];
    const map = L.map('map', { attributionControl: false }).setView(jakartaPos, 4);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png').addTo(map);
}

document.addEventListener('DOMContentLoaded', () => {
    initS11Chart();
    initMap();
    pollLiveTelemetry();
});
