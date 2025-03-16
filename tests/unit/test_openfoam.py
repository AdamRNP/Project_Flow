# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 18:19:55 2025

@author: adamp
"""

"""
Unit tests for OpenFOAM dictionary handling functionality.
"""
import os
import pytest
from src.openfoam.dictionary import OpenFOAMDict, DictParseError
from src.openfoam.case import OpenFOAMCase

class TestOpenFOAMDict:
    """Test the OpenFOAMDict class functionality."""
    
    def test_create_empty_dict(self):
        """Test creating an empty OpenFOAM dictionary."""
        foam_dict = OpenFOAMDict()
        assert len(foam_dict) == 0
    
    def test_add_simple_entry(self):
        """Test adding a simple key-value entry."""
        foam_dict = OpenFOAMDict()
        foam_dict["application"] = "simpleFoam"
        foam_dict["startFrom"] = "latestTime"
        
        assert foam_dict["application"] == "simpleFoam"
        assert foam_dict["startFrom"] == "latestTime"
    
    def test_add_nested_dict(self):
        """Test adding a nested dictionary."""
        foam_dict = OpenFOAMDict()
        foam_dict["solvers"] = OpenFOAMDict()
        foam_dict["solvers"]["p"] = OpenFOAMDict()
        foam_dict["solvers"]["p"]["solver"] = "GAMG"
        foam_dict["solvers"]["p"]["tolerance"] = "1e-6"
        
        assert foam_dict["solvers"]["p"]["solver"] == "GAMG"
        assert foam_dict["solvers"]["p"]["tolerance"] == "1e-6"
    
    def test_write_to_string(self):
        """Test conversion of dictionary to OpenFOAM format string."""
        foam_dict = OpenFOAMDict()
        foam_dict["application"] = "simpleFoam"
        foam_dict["startTime"] = 0
        foam_dict["endTime"] = 1000
        
        dict_str = str(foam_dict)
        assert "application simpleFoam;" in dict_str
        assert "startTime 0;" in dict_str
        assert "endTime 1000;" in dict_str
    
    def test_parse_from_string(self):
        """Test parsing a dictionary from an OpenFOAM format string."""
        dict_str = """
        /*--------------------------------*- C++ -*----------------------------------*\\
        | =========                 |                                                 |
        | \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
        |  \\\\    /   O peration     | Version:  v2012                                 |
        |   \\\\  /    A nd           | Website:  www.openfoam.com                      |
        |    \\\\/     M anipulation  |                                                 |
        \\*---------------------------------------------------------------------------*/
        FoamFile
        {
            version     2.0;
            format      ascii;
            class       dictionary;
            location    "system";
            object      controlDict;
        }
        // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

        application     simpleFoam;
        startFrom       startTime;
        startTime       0;
        stopAt          endTime;
        endTime         1000;
        deltaT          1;
        writeControl    timeStep;
        writeInterval   100;
        purgeWrite      0;
        writeFormat     ascii;
        writePrecision  6;
        writeCompression off;
        timeFormat      general;
        timePrecision   6;
        runTimeModifiable true;
        """
        
        foam_dict = OpenFOAMDict.parse_string(dict_str)
        assert foam_dict["application"] == "simpleFoam"
        assert foam_dict["startFrom"] == "startTime"
        assert foam_dict["endTime"] == "1000"
        assert foam_dict["runTimeModifiable"] == "true"
    
    def test_invalid_syntax(self):
        """Test handling of invalid OpenFOAM dictionary syntax."""
        dict_str = """
        application     simpleFoam
        // Missing semicolon above
        startFrom       startTime;
        """
        
        with pytest.raises(DictParseError):
            OpenFOAMDict.parse_string(dict_str)


class TestOpenFOAMCase:
    """Test the OpenFOAMCase class functionality."""
    
    def test_create_case(self, temp_simulation_dir):
        """Test creating a case object with an existing directory."""
        case = OpenFOAMCase(str(temp_simulation_dir))
        assert case.case_dir == str(temp_simulation_dir)
        assert os.path.exists(case.case_dir)
    
    def test_read_control_dict(self, temp_simulation_dir):
        """Test reading the controlDict file."""
        control_dict_path = temp_simulation_dir / "system" / "controlDict"
        control_dict_path.write_text("""
        application     simpleFoam;
        startFrom       startTime;
        startTime       0;
        stopAt          endTime;
        endTime         1000;
        """)
        
        case = OpenFOAMCase(str(temp_simulation_dir))
        control_dict = case.read_control_dict()
        
        assert control_dict["application"] == "simpleFoam"
        assert control_dict["endTime"] == "1000"
    
    def test_write_control_dict(self, temp_simulation_dir):
        """Test writing to the controlDict file."""
        case = OpenFOAMCase(str(temp_simulation_dir))
        
        control_dict = OpenFOAMDict()
        control_dict["application"] = "pimpleFoam"
        control_dict["startFrom"] = "startTime"
        control_dict["startTime"] = 0
        control_dict["stopAt"] = "endTime"
        control_dict["endTime"] = 2000
        
        case.write_control_dict(control_dict)
        
        # Read back to verify
        written_dict = case.read_control_dict()
        assert written_dict["application"] == "pimpleFoam"
        assert written_dict["endTime"] == "2000"
