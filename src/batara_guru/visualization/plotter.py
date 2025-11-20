"""Clean spatio-temporal visualization for Rule 30 - No subplots, no title."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib as mpl

mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']


class Plotter:
    """Clean plotter for Rule 30 spatio-temporal evolution."""
    
    @staticmethod
    def create_plot(result: dict, filename: str, output_dir: str = "outputs",
                   dpi: int = 350, colormap: str = 'binary'):
        """
        Create clean plot of Rule 30 evolution - ONLY the CA evolution.
        No title, no subplots, no stats boxes.
        
        Args:
            result: Simulation results dictionary
            filename: Output filename (e.g., 'case1.png')
            output_dir: Output directory path
            dpi: Plot resolution (DPI)
            colormap: Colormap name
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        filepath = output_path / filename
        
        grid = result['grid']
        steps, width = grid.shape
        
        # Calculate figure size to avoid truncation
        # Aspect ratio based on grid dimensions
        aspect = width / steps
        
        if aspect > 2:
            # Wide grid
            fig_width = 20
            fig_height = fig_width / aspect
        elif aspect < 0.5:
            # Tall grid
            fig_height = 16
            fig_width = fig_height * aspect
        else:
            # Balanced grid
            fig_width = 16
            fig_height = fig_width / aspect
        
        # Ensure minimum size
        fig_width = max(fig_width, 10)
        fig_height = max(fig_height, 8)
        
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        
        # Use specified colormap
        cmap = plt.cm.get_cmap(colormap)
        
        # Plot with nearest neighbor to preserve sharp pixels
        im = ax.imshow(grid, cmap=cmap, interpolation='nearest', 
                      aspect='auto', origin='upper')
        
        # Clean axes
        ax.set_xlabel('Cell Index', fontsize=14, fontweight='bold')
        ax.set_ylabel('Time Step', fontsize=14, fontweight='bold')
        ax.tick_params(labelsize=12)
        
        # Add subtle colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
        cbar.set_label('State', fontsize=12, fontweight='bold')
        cbar.ax.tick_params(labelsize=11)
        
        # Tight layout to avoid cutting off labels
        plt.tight_layout()
        
        # Save with high DPI and no extra whitespace
        plt.savefig(filepath, dpi=dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='none', pad_inches=0.1)
        plt.close(fig)
        
        file_size_mb = filepath.stat().st_size / 1024 / 1024
        print(f"       ✓ Saved: {filepath} ({file_size_mb:.1f} MB, {dpi} DPI)")
