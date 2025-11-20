# `batara-guru`: Python-based rule 30 cellular automaton analyzer

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![NumPy](https://img.shields.io/badge/NumPy-%23013243.svg?logo=numpy&logoColor=white)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?logo=Matplotlib&logoColor=black)](https://matplotlib.org/)
[![Numba](https://img.shields.io/badge/accelerated-numba-orange.svg)](https://numba.pydata.org/)

High-performance Rule 30 cellular automaton simulator with parallel processing and entropy analysis.

## Context

Rule 30 is an elementary cellular automaton that exhibits chaotic behavior:

**Evolution Rule**: For each cell and its two neighbors, the next state is determined by:
```
111 → 0    110 → 0    101 → 0    100 → 1
011 → 1    010 → 1    001 → 1    000 → 0
```

**Binary representation**: 00011110₂ = 30₁₀

## Features

- **Parallel Numba JIT**: Multi-core optimized evolution
- **Entropy Analysis**: Shannon entropy and complexity with tqdm
- **Full Pyramid Visualization**: Complete non-truncated patterns
- **High-Quality Plots**: Publication-ready figures (350-600 DPI)
- **NetCDF Output**: Compressed data storage
- **4 Test Cases**: Different scales showing complete pyramids

## Installation

```bash
chmod +x setup_batara_guru.sh
./setup_batara_guru.sh
cd batara-guru
pip install -e .
```

## Quick Start

**Command line:**
```bash
# Run single case (uses all CPU cores by default)
batara-guru case1

# Run all cases
batara-guru --all

# Specify CPU cores
batara-guru case1 --cores 4

# Custom DPI
batara-guru case1 --dpi 600
```

**Python API:**
```python
from batara_guru import Rule30Solver

solver = Rule30Solver(width=501, steps=250, n_cores=8)

result = solver.evolve(initial_condition='single')

print(f"Final entropy: {result['entropy'][-1]:.4f}")
print(f"Mean complexity: {result['mean_complexity']:.4f}")
```

## Test Cases

All cases show complete pyramidal patterns:

| Case | Description | Width | Steps | DPI | Pattern |
|------|-------------|-------|-------|-----|---------|
| 1 | Small Pyramid | 251 | 125 | 350 | Complete small-scale |
| 2 | Medium Pyramid | 501 | 250 | 400 | Classic medium-scale |
| 3 | Large Pyramid | 1001 | 500 | 500 | Large-scale detail |
| 4 | Extra Large | 2001 | 1000 | 600 | Maximum resolution |

## Configuration

```text
grid_width = 501           # Number of cells
time_steps = 250           # Evolution steps (< width/2 for full pyramid)
initial_condition = single # Always single center cell
center_position = 250      # Auto-calculated if not specified
plot_dpi = 400            # Output image DPI
save_netcdf = true        # Save NetCDF file
save_plot = true          # Save PNG plot
colormap = binary         # Color scheme
```

## Output

**NetCDF variables:**
- `grid(time,x)`: Complete evolution history
- `entropy(time)`: Shannon entropy per timestep
- `complexity(time)`: Local complexity per timestep

**PNG plots:**
- Clean spatio-temporal evolution
- Full pyramid visualization

## Parallel Processing

By default, uses all available CPU cores. Specify custom core count:

```bash
batara-guru case3 --cores 8
```

Or in Python:
```python
solver = Rule30Solver(width=1001, steps=500, n_cores=8)
```

## Citation

```bibtex
@software{batara_guru_2025,
  author = {Herho, Sandy H. S. and Napitupulu, Gandhi},
  title = {\texttt{batara-guru}: Python-based Rule 30 cellular automaton analyzer},
  year = {2025},
  version = {0.0.1},
  license = {MIT}
}
```

## Authors

- Sandy H. S. Herho (sandy.herho@email.ucr.edu)
- Gandhi Napitupulu

## License

MIT License - See [LICENSE](LICENSE) for details.
