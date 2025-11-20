#!/usr/bin/env python
"""Command Line Interface for batara-guru."""

import argparse
import sys
from pathlib import Path

from .core.solver import Rule30Solver
from .io.config_manager import ConfigManager
from .io.data_handler import DataHandler
from .visualization.plotter import Plotter
from .utils.logger import SimulationLogger
from .utils.timer import Timer


def print_header():
    """Print ASCII art header."""
    print("\n" + "=" * 70)
    print(" " * 15 + "batara-guru - RULE 30 ANALYZER")
    print(" " * 20 + "Parallel Numba Processing")
    print(" " * 25 + "Version 0.0.1")
    print("=" * 70)
    print("\n  Authors: Sandy H. S. Herho and Gandhi Napitupulu")
    print("\n  License: MIT License")
    print("=" * 70 + "\n")


def normalize_scenario_name(scenario_name: str) -> str:
    """Convert scenario name to clean filename format."""
    clean = scenario_name.lower()
    clean = clean.replace(' - ', '_')
    clean = clean.replace('-', '_')
    clean = clean.replace(' ', '_')
    
    while '__' in clean:
        clean = clean.replace('__', '_')
    
    clean = clean.rstrip('_')
    return clean


def run_scenario(config: dict, output_dir: str = "outputs",
                verbose: bool = True, n_cores: int = None):
    """Run complete Rule 30 simulation scenario."""
    scenario_name = config.get('scenario_name', 'simulation')
    clean_name = normalize_scenario_name(scenario_name)
    
    if verbose:
        print(f"\n{'=' * 60}")
        print(f"SCENARIO: {scenario_name}")
        print(f"{'=' * 60}")
    
    logger = SimulationLogger(clean_name, "logs", verbose)
    timer = Timer()
    timer.start("total")
    
    try:
        logger.log_parameters(config)
        
        # Initialize solver
        with timer.time_section("solver_init"):
            if verbose:
                print("\n[1/5] Initializing Rule 30 solver...")
            
            solver = Rule30Solver(
                width=config.get('grid_width', 501),
                steps=config.get('time_steps', 250),
                verbose=verbose,
                logger=logger,
                n_cores=n_cores
            )
        
        # Run simulation
        with timer.time_section("simulation"):
            if verbose:
                print("\n[2/5] Running Rule 30 evolution...")
            
            result = solver.evolve(
                initial_condition=config.get('initial_condition', 'single'),
                center_position=config.get('center_position', None),
                show_progress=verbose
            )
            
            logger.log_results(result)
        
        # Save NetCDF
        if config.get('save_netcdf', True):
            with timer.time_section("save_netcdf"):
                if verbose:
                    print("\n[3/5] Saving NetCDF file...")
                
                filename = f"{clean_name}.nc"
                DataHandler.save_netcdf(filename, result, config, output_dir)
                
                if verbose:
                    print(f"       ✓ Saved: {output_dir}/{filename}")
        
        # Save CSV files
        with timer.time_section("save_csv"):
            if verbose:
                print("\n[4/5] Saving CSV files...")
            
            entropy_file, complexity_file, composite_file = DataHandler.save_csv(
                clean_name, result, config, output_dir
            )
            
            if verbose:
                print(f"       ✓ Saved: {entropy_file.name}")
                print(f"       ✓ Saved: {complexity_file.name}")
                print(f"       ✓ Saved: {composite_file.name}")
        
        # Create plot
        if config.get('save_plot', True):
            with timer.time_section("plot"):
                if verbose:
                    print("\n[5/5] Creating spatio-temporal plot...")
                
                filename = f"{clean_name}.png"
                dpi = config.get('plot_dpi', 350)
                colormap = config.get('colormap', 'binary')
                
                Plotter.create_plot(
                    result,
                    filename,
                    output_dir,
                    dpi,
                    colormap
                )
        
        timer.stop("total")
        logger.log_timing(timer.get_times())
        
        # Print timing summary
        if verbose:
            times = timer.get_times()
            print(f"\n{'=' * 60}")
            print("TIMING SUMMARY")
            print('=' * 60)
            for key, value in sorted(times.items()):
                display_name = key.replace('_', ' ').title()
                print(f"  {display_name:.<45} {value:>8.2f} s")
            print('=' * 60)
        
        if verbose:
            print(f"\n{'=' * 60}")
            print("✓ SIMULATION COMPLETED SUCCESSFULLY")
            print(f"{'=' * 60}\n")
    
    except Exception as e:
        logger.error(f"Simulation failed: {str(e)}")
        if verbose:
            print(f"\n{'=' * 60}")
            print(f"✗ SIMULATION FAILED: {str(e)}")
            print(f"{'=' * 60}\n")
        raise
    
    finally:
        logger.finalize()


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='Batara Guru - Rule 30 Cellular Automaton Analyzer',
        epilog='Example: batara-guru case1 --cores 8 --dpi 600'
    )
    
    parser.add_argument(
        'case',
        nargs='?',
        choices=['case1', 'case2', 'case3', 'case4'],
        help='Test case to run'
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Path to custom configuration file'
    )
    
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Run all test cases sequentially'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default='outputs',
        help='Output directory (default: outputs)'
    )
    
    parser.add_argument(
        '--cores',
        type=int,
        default=None,
        help='Number of CPU cores (default: all available)'
    )
    
    parser.add_argument(
        '--dpi',
        type=int,
        default=None,
        help='Plot DPI (overrides config)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Quiet mode'
    )
    
    args = parser.parse_args()
    verbose = not args.quiet
    
    if verbose:
        print_header()
    
    if args.config:
        config = ConfigManager.load(args.config)
        if args.dpi:
            config['plot_dpi'] = args.dpi
        run_scenario(config, args.output_dir, verbose, args.cores)
    
    elif args.all:
        configs_dir = Path(__file__).parent.parent.parent / 'configs'
        config_files = sorted(configs_dir.glob('case*.txt'))
        
        if not config_files:
            print("ERROR: No configuration files found in configs/")
            sys.exit(1)
        
        for i, cfg_file in enumerate(config_files, 1):
            if verbose:
                print(f"\n{'#' * 70}")
                print(f"# RUNNING CASE {i}/{len(config_files)}: {cfg_file.stem}")
                print(f"{'#' * 70}")
            
            config = ConfigManager.load(str(cfg_file))
            if args.dpi:
                config['plot_dpi'] = args.dpi
            run_scenario(config, args.output_dir, verbose, args.cores)
    
    elif args.case:
        cfg_name = args.case
        configs_dir = Path(__file__).parent.parent.parent / 'configs'
        cfg_file = configs_dir / f'{cfg_name}.txt'
        
        if cfg_file.exists():
            config = ConfigManager.load(str(cfg_file))
            if args.dpi:
                config['plot_dpi'] = args.dpi
            run_scenario(config, args.output_dir, verbose, args.cores)
        else:
            print(f"ERROR: Configuration file not found: {cfg_file}")
            sys.exit(1)
    
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == '__main__':
    main()
