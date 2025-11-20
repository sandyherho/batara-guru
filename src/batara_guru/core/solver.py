"""
Rule 30 Cellular Automaton Solver with Parallel Processing
Implements Rule 30: 00011110 in binary
"""

import numpy as np
from numba import jit, prange
import numba
import os
from typing import Dict, Any, Optional
from tqdm import tqdm


@jit(nopython=True, cache=True)
def apply_rule30(state: np.ndarray) -> np.ndarray:
    """
    Apply Rule 30 to current state.
    Rule 30: 111→0, 110→0, 101→0, 100→1, 011→1, 010→1, 001→1, 000→0
    """
    n = len(state)
    new_state = np.zeros(n, dtype=np.int8)
    
    for i in range(n):
        left = state[(i - 1) % n]
        center = state[i]
        right = state[(i + 1) % n]
        
        # Rule 30 lookup
        pattern = left * 4 + center * 2 + right
        
        if pattern == 0:    # 000
            new_state[i] = 0
        elif pattern == 1:  # 001
            new_state[i] = 1
        elif pattern == 2:  # 010
            new_state[i] = 1
        elif pattern == 3:  # 011
            new_state[i] = 1
        elif pattern == 4:  # 100
            new_state[i] = 1
        elif pattern == 5:  # 101
            new_state[i] = 0
        elif pattern == 6:  # 110
            new_state[i] = 0
        elif pattern == 7:  # 111
            new_state[i] = 0
    
    return new_state


@jit(nopython=True, parallel=True, cache=True)
def compute_metrics_parallel(grid: np.ndarray) -> tuple:
    """
    Compute entropy and complexity for all timesteps in parallel.
    """
    steps, width = grid.shape
    entropy_values = np.zeros(steps)
    complexity_values = np.zeros(steps)
    
    for t in prange(steps):
        state = grid[t]
        
        # Shannon entropy
        n_ones = np.sum(state)
        n_zeros = width - n_ones
        
        if n_ones > 0 and n_zeros > 0:
            p_one = n_ones / width
            p_zero = n_zeros / width
            entropy = -p_one * np.log2(p_one) - p_zero * np.log2(p_zero)
        else:
            entropy = 0.0
        
        entropy_values[t] = entropy
        
        # Local complexity (transitions)
        transitions = 0
        for i in range(width - 1):
            if state[i] != state[i + 1]:
                transitions += 1
        if state[-1] != state[0]:
            transitions += 1
        
        complexity_values[t] = transitions / width
    
    return entropy_values, complexity_values


class Rule30Solver:
    """Rule 30 cellular automaton solver with parallel processing."""
    
    def __init__(self, width: int = 501, steps: int = 250, 
                 verbose: bool = True, logger: Optional[Any] = None,
                 n_cores: Optional[int] = None):
        """
        Initialize Rule 30 solver with parallel processing.
        
        Args:
            width: Grid width (number of cells)
            steps: Number of time steps
            verbose: Print progress messages
            logger: Optional logger instance
            n_cores: Number of CPU cores (None = all available)
        """
        self.width = width
        self.steps = steps
        self.verbose = verbose
        self.logger = logger
        
        # Set number of threads
        if n_cores is None:
            n_cores = os.cpu_count()
        numba.set_num_threads(n_cores)
        
        if verbose:
            print(f"  Grid: {width} cells")
            print(f"  Steps: {steps}")
            print(f"  Rule: 30 (00011110)")
            print(f"  CPU cores: {n_cores}")
    
    def evolve(self, initial_condition: str = 'single',
               center_position: Optional[int] = None,
               show_progress: bool = True) -> Dict[str, Any]:
        """
        Evolve Rule 30 cellular automaton.
        
        Args:
            initial_condition: Always 'single' for pyramid patterns
            center_position: Position for single cell (auto if None)
            show_progress: Show progress bar
        
        Returns:
            Dictionary with results
        """
        width = self.width
        steps = self.steps
        
        # Initialize state
        state = np.zeros(width, dtype=np.int8)
        if center_position is None:
            center_position = width // 2
        state[center_position] = 1
        
        # Storage
        grid = np.zeros((steps + 1, width), dtype=np.int8)
        grid[0] = state
        
        if self.verbose:
            print(f"  Initial condition: single center cell")
            print(f"  Center position: {center_position}")
        
        # Evolution loop
        if show_progress:
            pbar = tqdm(range(steps), desc="  Evolving CA", unit=" steps")
        else:
            pbar = range(steps)
        
        for t in pbar:
            state = apply_rule30(state)
            grid[t + 1] = state
        
        if show_progress and isinstance(pbar, tqdm):
            pbar.close()
        
        # Compute metrics in parallel
        if self.verbose:
            print("  Computing entropy & complexity...")
        
        entropy_values, complexity_values = compute_metrics_parallel(grid)
        
        # Compute statistics
        mean_entropy = np.mean(entropy_values)
        std_entropy = np.std(entropy_values)
        mean_complexity = np.mean(complexity_values)
        std_complexity = np.std(complexity_values)
        final_density = np.sum(grid[-1]) / width
        
        if self.verbose:
            print(f"  Final entropy: {entropy_values[-1]:.4f}")
            print(f"  Mean entropy: {mean_entropy:.4f} ± {std_entropy:.4f}")
            print(f"  Mean complexity: {mean_complexity:.4f} ± {std_complexity:.4f}")
            print(f"  Final density: {final_density:.4f}")
        
        return {
            'grid': grid,
            'entropy': entropy_values,
            'complexity': complexity_values,
            'mean_entropy': mean_entropy,
            'std_entropy': std_entropy,
            'mean_complexity': mean_complexity,
            'std_complexity': std_complexity,
            'final_density': final_density,
            'params': {
                'width': width,
                'steps': steps,
                'initial_condition': initial_condition,
                'center_position': center_position
            }
        }
