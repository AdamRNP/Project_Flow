# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 15:09:00 2025

@author: adamp
"""

"""
Main entry point for the Project_Flow application.
"""
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings

from src.ui.main_window import MainWindow
from src.utils.config import Config
from src.utils.logger import setup_logger

def main():
    """Main application entry point."""
    # Set up logging
    setup_logger()
    
    # Load configuration
    config = Config()
    config.load()
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Project_Flow")
    app.setOrganizationName("Project_Flow")
    app.setOrganizationDomain("projectflow.org")
    
    # Set up QSettings
    settings = QSettings()
    
    # Create and show main window
    main_window = MainWindow(config, settings)
    main_window.show()
    
    # Run application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

