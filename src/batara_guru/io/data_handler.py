"""NetCDF Data Handler for Rule 30 Results."""

import numpy as np
from netCDF4 import Dataset
from pathlib import Path
from datetime import datetime


class DataHandler:
    """NetCDF output handler for Rule 30 simulations."""
    
    @staticmethod
    def save_netcdf(filename: str, result: dict, metadata: dict,
                   output_dir: str = "outputs"):
        """Save Rule 30 simulation results to NetCDF file."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        filepath = output_path / filename
        
        with Dataset(filepath, 'w', format='NETCDF4') as nc:
            
            # Dimensions
            width = result['params']['width']
            steps = result['params']['steps']
            
            nc.createDimension('x', width)
            nc.createDimension('time', steps + 1)
            
            # Coordinates
            nc_x = nc.createVariable('x', 'i4', ('x',), zlib=True, complevel=4)
            nc_x[:] = np.arange(width)
            nc_x.units = "cell_index"
            nc_x.long_name = "spatial_coordinate"
            
            nc_t = nc.createVariable('time', 'i4', ('time',), zlib=True, complevel=4)
            nc_t[:] = np.arange(steps + 1)
            nc_t.units = "time_step"
            nc_t.long_name = "temporal_coordinate"
            
            # Grid evolution
            nc_grid = nc.createVariable('grid', 'i1', ('time', 'x'),
                                       zlib=True, complevel=6)
            nc_grid[:] = result['grid']
            nc_grid.units = "state"
            nc_grid.long_name = "cellular_automaton_state"
            nc_grid.description = "0=dead, 1=alive"
            
            # Entropy
            nc_entropy = nc.createVariable('entropy', 'f4', ('time',),
                                          zlib=True, complevel=4)
            nc_entropy[:] = result['entropy']
            nc_entropy.units = "bits"
            nc_entropy.long_name = "shannon_entropy"
            
            # Complexity
            nc_complexity = nc.createVariable('complexity', 'f4', ('time',),
                                             zlib=True, complevel=4)
            nc_complexity[:] = result['complexity']
            nc_complexity.units = "normalized"
            nc_complexity.long_name = "local_complexity"
            
            # Global attributes - Results
            nc.mean_entropy = float(result['mean_entropy'])
            nc.std_entropy = float(result['std_entropy'])
            nc.mean_complexity = float(result['mean_complexity'])
            nc.std_complexity = float(result['std_complexity'])
            nc.final_density = float(result['final_density'])
            
            # Global attributes - Parameters
            params = result['params']
            nc.grid_width = int(params['width'])
            nc.time_steps = int(params['steps'])
            nc.initial_condition = str(params['initial_condition'])
            nc.center_position = int(params['center_position'])
            
            # Metadata
            nc.scenario = metadata.get('scenario_name', 'unknown')
            nc.created = datetime.now().isoformat()
            nc.software = "batara-guru"
            nc.version = "0.0.1"
            nc.rule = "rule_30"
            nc.Conventions = "CF-1.8"
            nc.title = f"Rule 30 Simulation: {metadata.get('scenario_name', 'unknown')}"
            nc.institution = "Independent Research"
