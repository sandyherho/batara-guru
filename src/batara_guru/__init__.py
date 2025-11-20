"""Batara Guru - Rule 30 Cellular Automaton Analyzer"""

__version__ = "0.0.1"
__author__ = "Sandy H. S. Herho, Gandhi Napitupulu"

from .core.solver import Rule30Solver
from .io.config_manager import ConfigManager
from .io.data_handler import DataHandler

__all__ = ["Rule30Solver", "ConfigManager", "DataHandler"]
