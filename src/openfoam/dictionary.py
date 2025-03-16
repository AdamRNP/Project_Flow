# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 18:31:18 2025

@author: adamp
"""

"""
Parser and writer for OpenFOAM dictionary files.
"""
import re
import os
from typing import Dict, List, Union, Optional, Any, TextIO

from src.utils.logger import get_logger

logger = get_logger(__name__)

class DictParseError(Exception):
    """Exception raised for errors during dictionary parsing."""
    pass

class OpenFOAMDict:
    """Class for handling OpenFOAM dictionary files.
    
    This class provides functionality to read, write, and manipulate OpenFOAM
    dictionary files, which are used extensively in OpenFOAM for configuration.
    """
    
    def __init__(self) -> None:
        """Initialize an empty OpenFOAM dictionary."""
        self._data: Dict[str, Any] = {}
        self._header: str = self._get_default_header()
    
    def __getitem__(self, key: str) -> Any:
        """Get a value from the dictionary.
        
        Args:
            key: Dictionary key
            
        Returns:
            The value associated with the key
            
        Raises:
            KeyError: If the key doesn't exist
        """
        return self._data[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Set a value in the dictionary.
        
        Args:
            key: Dictionary key
            value: Value to set
        """
        self._data[key] = value
    
    def __len__(self) -> int:
        """Return the number of entries in the dictionary."""
        return len(self._data)
    
    def __contains__(self, key: str) -> bool:
        """Check if key exists in the dictionary."""
        return key in self._data
    
    def _get_default_header(self) -> str:
        """Return the default header for OpenFOAM dictionary files."""
        return """/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  v2106                                 |
|   \\\\  /    A nd           | Website:  www.openfoam.com                      |
|    \\\\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      %s;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
"""
    
    def set_header_object(self, object_name: str) -> None:
        """Set the object name in the header.
        
        Args:
            object_name: Name to use in the header
        """
        self._header = self._get_default_header() % object_name
    
    def read(self, file_path: str) -> None:
        """Read a dictionary from a file.
        
        Args:
            file_path: Path to the OpenFOAM dictionary file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            DictParseError: If parsing fails
        """
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Skip FoamFile header
            match = re.search(r'// \* \* \* \* \* \* \* \* \* \* \* \* \* \* \* \* \* \* \* \* \* \*', content)
            if match:
                content = content[match.end():]
            
            self._parse_dict(content)
        except FileNotFoundError:
            logger.error(f"Dictionary file not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error parsing dictionary file {file_path}: {e}")
            raise DictParseError(f"Error parsing dictionary: {e}")
    
    def _parse_dict(self, content: str) -> None:
        """Parse dictionary content.
        
        Args:
            content: String content of the dictionary
            
        Raises:
            DictParseError: If parsing fails
        """
        # Simplified parsing logic - in practice, this would be more robust
        # Remove comments and empty lines
        lines = []
        for line in content.split('\n'):
            line = re.sub(r'//.*$', '', line).strip()
            if line:
                lines.append(line)
        
        # Parse entries
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Handle simple key-value pairs
            if ';' in line:
                key_val = line.split(';')[0].strip()
                try:
                    key, val = re.split(r'\s+', key_val, 1)
                    self._data[key] = val.strip()
                except ValueError:
                    pass  # Skip invalid lines
            
            # Handle dictionary entries
            elif '{' in line:
                key = line.split('{')[0].strip()
                # Find matching closing brace
                brace_count = 1
                j = i + 1
                sub_dict_lines = []
                
                while j < len(lines) and brace_count > 0:
                    if '{' in lines[j]:
                        brace_count += 1
                    if '}' in lines[j]:
                        brace_count -= 1
                    
                    if brace_count > 0:
                        sub_dict_lines.append(lines[j])
                    j += 1
                
                # Create sub-dictionary
                sub_dict = OpenFOAMDict()
                sub_dict._parse_dict('\n'.join(sub_dict_lines))
                self._data[key] = sub_dict
                
                i = j - 1  # Move to line after closing brace
            
            i += 1
    
    def write(self, file_path: str, object_name: Optional[str] = None) -> None:
        """Write the dictionary to a file.
        
        Args:
            file_path: Path where to write the file
            object_name: Optional name to use in the header
        """
        if object_name:
            self.set_header_object(object_name)
        else:
            # Try to deduce object name from file path
            try:
                object_name = os.path.basename(file_path)
                self.set_header_object(object_name)
            except:
                self.set_header_object("dictionary")
        
        with open(file_path, 'w') as f:
            f.write(self._header)
            f.write(self._to_foam_string())
            f.write("\n// ************************************************************************* //")
    
    def _to_foam_string(self, indent: int = 0) -> str:
        """Convert the dictionary to an OpenFOAM format string.
        
        Args:
            indent: Indentation level
            
        Returns:
            String representation in OpenFOAM format
        """
        result = []
        indent_str = "    " * indent
        
        for key, value in self._data.items():
            if isinstance(value, OpenFOAMDict):
                result.append(f"{indent_str}{key}\n{indent_str}{{")
                result.append(value._to_foam_string(indent + 1))
                result.append(f"{indent_str}}}")
            else:
                result.append(f"{indent_str}{key}    {value};")
        
        return "\n".join(result)

