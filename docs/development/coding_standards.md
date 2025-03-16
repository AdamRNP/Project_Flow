# Coding Standards for Project_Flow

This document outlines the coding standards and best practices for the Project_Flow codebase. Following these standards ensures code quality, maintainability, and consistency across the project.

## Python Style Guidelines

### Code Formatting

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use [Black](https://github.com/psf/black) for code formatting with default settings

### Imports

- Organize imports in the following order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application/library specific imports
- Use absolute imports rather than relative imports when possible
- Import specific functions/classes rather than entire modules when appropriate

Example:
```python
# Standard library
import os
import sys
from typing import Dict, List, Optional

# Third-party libraries
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow

# Local modules
from models.simulation import SimulationModel
from views.main_window import MainWindow
