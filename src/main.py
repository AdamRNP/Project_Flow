# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 15:09:00 2025

@author: adamp
"""

import sys
from PyQt5.QtWidgets import QApplication
from app.main_window import MainWindow

def main():
    """Application entry point."""
    # Create the application
    app = QApplication(sys.argv)
    app.setApplicationName("OpenFOAM CFD Interface")
    app.setOrganizationName("OpenFOAM-GUI")
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
