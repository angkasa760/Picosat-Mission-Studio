import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate_rf_transmission():
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Antenna coordinates (Cross dipole)
    x_coords = [-1, 1, 0, 0]
    y_coords = [0, 0, -1, 1]
    ax.scatter(x_coords, y_coords, color='red', label='Turnstile Feed Points')
    
    # Grid for radiation pattern
    r = np.linspace(0.1, 5, 100)
    theta = np.linspace(0, 2*np.pi, 200)
    R, THETA = np.meshgrid(r, theta)
    
    # Mock Farfield pattern (Omnidirectional turnover)
    Z = np.abs(np.sin(THETA)) + 1.0
    
    line, = ax.plot([], [], 'b-', lw=2, alpha=0.5)
    
    def init():
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        return line,

    def update(frame):
        # Sine wave expansion
        phase = frame / 10.0
        wave = np.sin(R * 5 - phase) * np.exp(-R/2)
        
        # Radiation pattern
        pattern = (1 + 0.2 * np.sin(THETA + phase))
        
        if frame % 10 == 0:
            ax.clear()
            ax.set_xlim(-6, 6)
            ax.set_ylim(-6, 6)
            ax.set_aspect('equal')
            ax.scatter(x_coords, y_coords, color='red', s=100, label='Picosat Antenna (Turnstile)')
            
            # Draw chassis
            rect = plt.Rectangle((-0.5, -0.5), 1, 1, facecolor='gray', alpha=0.8)
            ax.add_patch(rect)
            
            # Calculate radiation contour
            X = pattern * np.cos(THETA) * (2 + 0.5 * np.sin(phase))
            Y = pattern * np.sin(THETA) * (2 + 0.5 * np.sin(phase))
            ax.plot(X, Y, 'b--', alpha=0.3)
            
            # Fill wave
            # This is a simplified 2D representation
            circles = [plt.Circle((0, 0), radius=r_val, fill=False, color='cyan', alpha=max(0, 1 - r_val/5)) 
                       for r_val in [(frame/5 % 5), (frame/5 % 5) - 2] if r_val > 0]
            for c in circles:
                ax.add_patch(c)
                
            ax.set_title(f'Picosatellite RF Propagation (UHF 437.2 MHz)\nPhase: {frame:.1f}')
            ax.grid(True, linestyle=':', alpha=0.6)

    ani = FuncAnimation(fig, update, frames=100, init_func=init, interval=50)
    ani.save('rf_propagation.gif', writer='pillow')
    print("Exported: rf_propagation.gif")

if __name__ == "__main__":
    animate_rf_transmission()
