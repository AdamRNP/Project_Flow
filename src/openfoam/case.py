# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 18:33:38 2025

@author: adamp
"""

"""
OpenFOAM case directory manipulation.
"""
import os
import shutil
from typing import Dict, List, Optional, Any
from pathlib import Path

from src.openfoam.dictionary import OpenFOAMDict
from src.utils.logger import get_logger

logger = get_logger(__name__)

class OpenFOAMCase:
    """Class for handling OpenFOAM case directories.
    
    This class provides functionality to create, modify, and run OpenFOAM cases.
    """
    
    def __init__(self, case_dir: str) -> None:
        """Initialize with the case directory.
        
        Args:
            case_dir: Path to the OpenFOAM case directory
        """
        self.case_dir = os.path.abspath(case_dir)
        self.system_dir = os.path.join(self.case_dir, "system")
        self.constant_dir = os.path.join(self.case_dir, "constant")
        self.time_dirs: List[str] = []
        
        # Cache for loaded dictionaries
        self._dict_cache: Dict[str, OpenFOAMDict] = {}
    
    def create(self) -> None:
        """Create a new OpenFOAM case directory structure."""
        logger.info(f"Creating new OpenFOAM case: {self.case_dir}")
        
        # Create directory structure
        os.makedirs(self.case_dir, exist_ok=True)
        os.makedirs(self.system_dir, exist_ok=True)
        os.makedirs(self.constant_dir, exist_ok=True)
        os.makedirs(os.path.join(self.case_dir, "0"), exist_ok=True)
        
        # Create minimal required files
        self._create_minimal_files()
    
    def _create_minimal_files(self) -> None:
        """Create minimal required files for a valid OpenFOAM case."""
        # controlDict
        control_dict = OpenFOAMDict()
        control_dict["application"] = "simpleFoam"
        control_dict["startFrom"] = "startTime"
        control_dict["startTime"] = "0"
        control_dict["stopAt"] = "endTime"
        control_dict["endTime"] = "1000"
        control_dict["deltaT"] = "1"
        control_dict["writeControl"] = "timeStep"
        control_dict["writeInterval"] = "100"
        control_dict["purgeWrite"] = "0"
        control_dict["writeFormat"] = "ascii"
        control_dict["writePrecision"] = "6"
        control_dict["writeCompression"] = "off"
        control_dict["timeFormat"] = "general"
        control_dict["timePrecision"] = "6"
        control_dict["runTimeModifiable"] = "true"
        control_dict.write(os.path.join(self.system_dir, "controlDict"), "controlDict")
        
        # fvSchemes
        fv_schemes = OpenFOAMDict()
        fv_schemes["ddtSchemes"] = OpenFOAMDict()
        fv_schemes["ddtSchemes"]["default"] = "steadyState"
        
        fv_schemes["gradSchemes"] = OpenFOAMDict()
        fv_schemes["gradSchemes"]["default"] = "Gauss linear"
        
        fv_schemes["divSchemes"] = OpenFOAMDict()
        fv_schemes["divSchemes"]["default"] = "none"
        fv_schemes["divSchemes"]["div(phi,U)"] = "bounded Gauss upwind"
        fv_schemes["divSchemes"]["div(phi,k)"] = "bounded Gauss upwind"
        fv_schemes["divSchemes"]["div(phi,epsilon)"] = "bounded Gauss upwind"
        fv_schemes["divSchemes"]["div(phi,omega)"] = "bounded Gauss upwind"
        fv_schemes["divSchemes"]["div((nuEff*dev2(T(grad(U)))))"] = "Gauss linear"
        
        fv_schemes["laplacianSchemes"] = OpenFOAMDict()
        fv_schemes["laplacianSchemes"]["default"] = "Gauss linear corrected"
        
        fv_schemes["interpolationSchemes"] = OpenFOAMDict()
        fv_schemes["interpolationSchemes"]["default"] = "linear"
        
        fv_schemes["snGradSchemes"] = OpenFOAMDict()
        fv_schemes["snGradSchemes"]["default"] = "corrected"
        
        fv_schemes.write(os.path.join(self.system_dir, "fvSchemes"), "fvSchemes")
        
        # fvSolution
        fv_solution = OpenFOAMDict()
        fv_solution["solvers"] = OpenFOAMDict()
        
        fv_solution["solvers"]["p"] = OpenFOAMDict()
        fv_solution["solvers"]["p"]["solver"] = "GAMG"
        fv_solution["solvers"]["p"]["tolerance"] = "1e-6"
        fv_solution["solvers"]["p"]["relTol"] = "0.1"
        fv_solution["solvers"]["p"]["smoother"] = "GaussSeidel"
        
        fv_solution["solvers"]["U"] = OpenFOAMDict()
        fv_solution["solvers"]["U"]["solver"] = "smoothSolver"
        fv_solution["solvers"]["U"]["smoother"] = "GaussSeidel"
        fv_solution["solvers"]["U"]["tolerance"] = "1e-6"
        fv_solution["solvers"]["U"]["relTol"] = "0.1"
        
        fv_solution["SIMPLE"] = OpenFOAMDict()
        fv_solution["SIMPLE"]["nNonOrthogonalCorrectors"] = "0"
        fv_solution["SIMPLE"]["consistent"] = "true"
        fv_solution["SIMPLE"]["residualControl"] = OpenFOAMDict()
        fv_solution["SIMPLE"]["residualControl"]["p"] = "1e-4"
        fv_solution["SIMPLE"]["residualControl"]["U"] = "1e-4"
        
        fv_solution.write(os.path.join(self.system_dir, "fvSolution"), "fvSolution")
    
    def get_dictionary(self, path: str) -> OpenFOAMDict:
        """Get a dictionary from the case.
        
        Args:
            path: Relative path to the dictionary from case directory
            
        Returns:
            The loaded dictionary
        """
        abs_path = os.path.join(self.case_dir, path)
        
        if abs_path in self._dict_cache:
            return self._dict_cache[abs_path]
        
        dict_obj = OpenFOAMDict()
        dict_obj.read(abs_path)
        self._dict_cache[abs_path] = dict_obj
        return dict_obj
    
    def write_dictionary(self, dict_obj: OpenFOAMDict, path: str) -> None:
        """Write a dictionary to the case.
        
        Args:
            dict_obj: Dictionary to write
            path: Relative path from case directory
        """
        abs_path = os.path.join(self.case_dir, path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        dict_obj.write(abs_path)
        self._dict_cache[abs_path] = dict_obj
    
    def run_solver(self, solver_name: Optional[str] = None) -> None:
        """Run the OpenFOAM solver for this case.
        
        Args:
            solver_name: Name of the solver to run. If None, read from controlDict.
        """
        # In a real implementation, this would actually run the solver
        # For now, we just simulate it
        logger.info(f"Running solver for case: {self.case_dir}")
        
        if not solver_name:
            control_dict = self.get_dictionary("system/controlDict")
            solver_name = control_dict["application"]
        
        logger.info(f"Using solver: {solver_name}")
        # Here we would actually launch the solver process
