# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 18:18:50 2025

@author: adamp
"""

"""
Global pytest configuration and fixtures for Project_Flow tests.
"""
import os
import sys
import pytest
from PyQt5.QtWidgets import QApplication

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Create QApplication instance for UI tests
@pytest.fixture(scope="session")
def qapp():
    """Create a QApplication instance for UI tests."""
    app = QApplication([])
    yield app
    app.quit()

# Mock OpenFOAM environment
@pytest.fixture
def mock_openfoam_env(monkeypatch):
    """Create a mock OpenFOAM environment for testing."""
    monkeypatch.setenv("WM_PROJECT_DIR", "/mock/path/to/openfoam")
    monkeypatch.setenv("FOAM_RUN", "/mock/path/to/run")
    monkeypatch.setenv("FOAM_USER_APPBIN", "/mock/path/to/bin")
    return {
        "WM_PROJECT_DIR": "/mock/path/to/openfoam",
        "FOAM_RUN": "/mock/path/to/run",
        "FOAM_USER_APPBIN": "/mock/path/to/bin"
    }

# Temporary directory for simulation tests
@pytest.fixture
def temp_simulation_dir(tmp_path):
    """Create a temporary directory with OpenFOAM case structure."""
    case_dir = tmp_path / "testCase"
    case_dir.mkdir()
    
    # Create standard OpenFOAM directories
    (case_dir / "0").mkdir()
    (case_dir / "constant").mkdir()
    (case_dir / "system").mkdir()
    
    # Create minimal required files
    (case_dir / "system" / "controlDict").write_text("// Mock controlDict")
    (case_dir / "system" / "fvSchemes").write_text("// Mock fvSchemes")
    (case_dir / "system" / "fvSolution").write_text("// Mock fvSolution")
    
    return case_dir
