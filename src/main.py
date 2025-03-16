# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 13:00:15 2025

@author: adamp
"""

"""
OpenFOAM Studio - Advanced CFD Simulation Interface
"""
import sys
from PyQt5.QtWidgets import QApplication

from core.application import OpenFOAMStudio

def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    app.setApplicationName("OpenFOAM Studio")
    
    # Create main window
    window = OpenFOAMStudio()
    window.show()
    
    # Start the application
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())