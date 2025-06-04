# graph_manager.py
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

class GraphManager:
    def __init__(self):
        self.fig = None
        self.ax1 = None  # deceleration axis
        self.ax2 = None  # distance axis

    def initialize_graphs(self, test_params):
        """Set up dual-plot layout with shared x-axis"""
        self.fig = plt.figure(figsize=(12, 8))
        gs = GridSpec(2, 1, height_ratios=[2, 1])  
        
        self.ax1 = self.fig.add_subplot(gs[0])  # top plot (deceleration)
        self.ax2 = self.fig.add_subplot(gs[1])  # bottom plot (distance)
        
        # parameter box
        param_text = self.format_params(test_params)
        self.fig.text(0.07, 0.86, param_text, 
                    bbox=dict(facecolor='white', alpha=0.8),
                    fontsize=9, ha='left')

    def format_params(self, params):
        """Format test parameters for display"""
        return (
            f"Test Parameters:\n"
            f"• Mass: {params['mass']:.1f} tonnes\n"
            f"• Speed: {params['speed']} km/h\n"
            f"• Env: {params['env']} (μ={params['adhesion']:.2f})\n"
            f"• Brakes: {params['cylinders']}x{params['piston_area']}m²\n"
            f"• μ={params['friction']} | Wear: {params['wear']:.0f}%"
        )

    def plot_deceleration(self, phases, decels, passes, env_condition):
        """Plot deceleration results with TSI standards"""
        bars = self.ax1.bar(phases, decels, 
                        color=['green' if p else 'red' for p in passes],
                        edgecolor='black', alpha=0.8)
        
        # reference lines
        self.ax1.axhline(0.8, color='blue', linestyle='--')
        if env_condition != 'dry':
            self.ax1.axhline(0.3, color='orange', linestyle=':')
        
        # annotate bars
        for bar in bars:
            height = bar.get_height()
            self.ax1.text(bar.get_x() + bar.get_width()/2, height,
                        f'{height:.2f}', ha='center', va='bottom')
        
        # set grid and labels
        self.ax1.set_ylabel('Deceleration (m/s²)')
        self.ax1.grid(axis='y', linestyle=':')

    def plot_stopping_distances(self, phases, distances):
        """Plot stopping distances below deceleration graph"""
        lines = self.ax2.plot(phases, distances, 'ko-', markerfacecolor='none')
        
        # annotate distances
        for x, dist in zip(phases, distances):
            self.ax2.text(x, dist, f'{dist:.1f}m', 
                        ha='center', va='bottom')
        
        self.ax2.set_xlabel('Brake Demand (bar)')
        self.ax2.set_ylabel('Distance (m)')
        self.ax2.grid(axis='y', linestyle=':')
        
        # highlight dangerous distances
        if max(distances) > 50:
            self.ax2.axhline(50, color='red', linestyle='--', alpha=0.3)

    def finalize(self):
        """Apply final formatting and display"""
        plt.tight_layout()
        plt.show()