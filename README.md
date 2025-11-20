# `batara-guru`: Python-based rule 30 cellular automaton analyzer

[![DOI](https://zenodo.org/badge/1100222381.svg)](https://doi.org/10.5281/zenodo.17656053)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/batara-guru.svg)](https://pypi.org/project/batara-guru/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![NumPy](https://img.shields.io/badge/NumPy-%23013243.svg?logo=numpy&logoColor=white)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?logo=Matplotlib&logoColor=black)](https://matplotlib.org/)
[![Numba](https://img.shields.io/badge/accelerated-numba-orange.svg)](https://numba.pydata.org/)

A fundamental implementation of Rule 30 cellular automaton with parallel processing for educational and research purposes.

## Context

Rule 30 is an elementary cellular automaton introduced by Stephen Wolfram that exhibits complex, chaotic behavior from simple deterministic rules.

**Mathematical Definition**: Let $s_i^t \in \{0,1\}$ denote the state of cell $i$ at time $t$. The evolution rule is:

$$s_i^{t+1} = s_{i-1}^t \oplus (s_i^t \lor s_{i+1}^t),$$

where $\oplus$ is XOR, $\lor$ is OR.

**Binary representation**: $00011110_2 = 30_{10}$

The system exhibits:
- **Chaos**: Sensitive dependence on initial conditions
- **Irreversibility**: Information loss over time
- **Complexity**: Wolfram Class III behavior

## Features

This implementation provides basic tools for studying Rule 30:

- **Parallel Numba JIT**: Multi-core evolution for computational efficiency
- **Entropy Analysis**: Shannon entropy $H = -\sum p_i \log_2 p_i$ and local complexity
- **Complete Pyramids**: Non-truncated patterns for boundary-free analysis
- **NetCDF & CSV Output**: Standard formats for data archiving and analysis
- **Publication Figures**: High-resolution plots (350-600 DPI)

## Installation

**From PyPI:**
```bash
pip install batara-guru
```

**From source:**
```bash
git clone https://github.com/sandyherho/batara-guru.git
cd batara-guru
pip install -e .
```

## Quick Start

**Command line:**
```bash
# Run single case (uses all CPU cores by default)
batara-guru case1

# Run all test cases
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

Provided test cases for pedagogical purposes:

| Case | Description | Width | Steps | DPI | Purpose |
|------|-------------|-------|-------|-----|---------|
| 1 | Small | 251 | 125 | 350 | Quick demonstration |
| 2 | Medium | 501 | 250 | 400 | Standard analysis |
| 3 | Large | 1001 | 500 | 500 | High-detail study |
| 4 | Extra Large | 2001 | 1000 | 600 | Publication quality |

All cases maintain $t < w/2$ to ensure complete pyramidal patterns without boundary interactions.

## Configuration

Example configuration file:
```text
grid_width = 501           # Number of cells
time_steps = 250           # Evolution steps (< width/2 for full pyramid)
initial_condition = single # Single center cell (standard)
center_position = 250      # Auto-calculated if not specified
plot_dpi = 400            # Output image resolution
save_netcdf = true        # Save NetCDF file
save_plot = true          # Save PNG plot
colormap = binary         # Color scheme
```

## Output Files

For each simulation, the following files are generated:

**NetCDF** (`.nc`):
- `grid(time, x)`: Complete evolution history
- `entropy(time)`: Shannon entropy $H(t)$
- `complexity(time)`: Normalized transition density

**CSV** (`.csv`):
- `{scenario}_entropy.csv`: Time series of entropy values
- `{scenario}_complexity.csv`: Time series of complexity values
- `{scenario}_composite.csv`: Combined entropy and complexity

**PNG** (`.png`):
- Spatio-temporal visualization of evolution

## Metrics

**Shannon Entropy**: 
$$H(t) = -p_1 \log_2 p_1 - p_0 \log_2 p_0$$
where $p_1 = N_1/N$ is the fraction of alive cells.

**Local Complexity**: 
$$C(t) = \frac{1}{N} \sum_{i=1}^{N} |s_i^t - s_{i+1}^t|$$
measuring spatial transition density.

## Parallel Processing

Utilizes all available CPU cores by default. Override with:

```bash
batara-guru case3 --cores 8
```

Or programmatically:
```python
solver = Rule30Solver(width=1001, steps=500, n_cores=8)
```

## Citation

If this tool is useful for your research or teaching, please cite:

```bibtex
@software{batara_guru_2025,
  author = {Herho, Sandy H. S. and Napitupulu, Gandhi},
  title = {\texttt{batara-guru}: Python-based Rule 30 cellular automaton analyzer},
  year = {2025},
  version = {0.0.1},
  url = {https://github.com/yourusername/batara-guru},
  license = {MIT}
}
```

## Authors

- Sandy H. S. Herho (sandy.herho@email.ucr.edu)
- Gandhi Napitupulu

## License

MIT License - See [LICENSE](LICENSE) for details.

## Acknowledgments

This is an educational implementation inspired by Wolfram's pioneering work on cellular automata. For comprehensive cellular automata research, see [Wolfram's *A New Kind of Science*](https://www.wolframscience.com/).
