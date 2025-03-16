# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 18:36:16 2025

@author: adamp
"""

"""
Main application window for Project_Flow.
"""
import os
from typing import Optional

from PyQt5.QtWidgets import (
    QMainWindow, QAction, QFileDialog, QMessageBox, 
    QDockWidget, QTreeView, QTabWidget, QToolBar, QStatusBar
)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon

from src.ui.central_widget import CentralWidget
from src.ui.case_explorer import CaseExplorerWidget
from src.ui.project_manager import ProjectManager
from src.utils.config import Config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MainWindow(QMainWindow):
    """Main application window class."""
    
    def __init__(self, config: Config, settings: QSettings) -> None:
        """Initialize the main window.
        
        Args:
            config: Application configuration
            settings: Qt settings object
        """
        super().__init__()
        self.config = config
        self.settings = settings
        self.project_manager = ProjectManager(self.config)
        
        self._init_ui()
        self._load_settings()
        
        logger.info("Main window initialized")
    
    def _init_ui(self) -> None:
        """Initialize the user interface."""
        # Set window properties
        self.setWindowTitle("Project_Flow")
        self.setMinimumSize(800, 600)
        
        # Central widget
        self.central_widget = CentralWidget(self)
        self.setCentralWidget(self.central_widget)
        
        # Create menus
        self._create_menus()
        
        # Create toolbars
        self._create_toolbars()
        
        # Create status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Create dock widgets
        self._create_dock_widgets()
    
    def _create_menus(self) -> None:
        """Create application menus."""
        # File menu
        self.file_menu = self.menuBar().addMenu("&File")
        
        self.new_project_action = QAction("&New Project", self)
        self.new_project_action.setStatusTip("Create a new project")
        self.new_project_action.triggered.connect(self._on_new_project)
        self.file_menu.addAction(self.new_project_action)
        
        self.open_project_action = QAction("&Open Project", self)
        self.open_project_action.setStatusTip("Open an existing project")
        self.open_project_action.triggered.connect(self._on_open_project)
        self.file_menu.addAction(self.open_project_action)
        
        self.save_project_action = QAction("&Save Project", self)
        self.save_project_action.setStatusTip("Save the current project")
        self.save_project_action.triggered.connect(self._on_save_project)
        self.file_menu.addAction(self.save_project_action)
        
        self.file_menu.addSeparator()
        
        self.exit_action = QAction("E&xit", self)
        self.exit_action.setStatusTip("Exit the application")
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)
        
        # Edit menu
        self.edit_menu = self.menuBar().addMenu("&Edit")
        
        self.preferences_action = QAction("&Preferences", self)
        self.preferences_action.setStatusTip("Edit application preferences")
        self.preferences_action.triggered.connect(self._on_preferences)
        self.edit_menu.addAction(self.preferences_action)
        
        # View menu
        self.view_menu = self.menuBar().addMenu("&View")
        
        # Simulation menu
        self.simulation_menu = self.menuBar().addMenu("&Simulation")
        
        self.run_action = QAction("&Run", self)
        self.run_action.setStatusTip("Run the current simulation")
        self.run_action.triggered.connect(self._on_run_simulation)
        self.simulation_menu.addAction(self.run_action)
        
        self.stop_action = QAction("&Stop", self)
        self.stop_action.setStatusTip("Stop the current simulation")
        self.stop_action.triggered.connect(self._on_stop_simulation)
        self.simulation_menu.addAction(self.stop_action)
        
        # Help menu
        self.help_menu = self.menuBar().addMenu("&Help")
        
        self.about_action = QAction("&About", self)
        self.about_action.setStatusTip("Show the application's About box")
        self.about_action.triggered.connect(self._on_about)
        self.help_menu.addAction(self.about_action)
    
    def _create_toolbars(self) -> None:
        """Create application toolbars."""
        # Main toolbar
        self.main_toolbar = QToolBar("Main Toolbar")
        self.addToolBar(Qt.TopToolBarArea, self.main_toolbar)
        
        self.main_toolbar.addAction(self.new_project_action)
        self.main_toolbar.addAction(self.open_project_action)
        self.main_toolbar.addAction(self.save_project_action)
        
        self.main_toolbar.addSeparator()
        
        self.main_toolbar.addAction(self.run_action)
        self.main_toolbar.addAction(self.stop_action)
    
    def _create_dock_widgets(self) -> None:
        """Create application dock widgets."""
        # Case explorer dock
        self.case_explorer_dock = QDockWidget("Case Explorer", self)
        self.case_explorer_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.case_explorer = CaseExplorerWidget(self)
        self.case_explorer_dock.setWidget(self.case_explorer)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.case_explorer_dock)
        
        # Add to View menu
        self.view_menu.addAction(self.case_explorer_dock.toggleViewAction())
    
    def _load_settings(self) -> None:
        """Load application settings."""
        # Restore window geometry
        geometry = self.settings.value("mainwindow/geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        # Restore window state
        state = self.settings.value("mainwindow/state")
        if state:
            self.restoreState(state)
    
    def _save_settings(self) -> None:
        """Save application settings."""
        # Save window geometry and state
        self.settings.setValue("mainwindow/geometry", self.saveGeometry())
        self.settings.setValue("mainwindow/state", self.saveState())
    
    def closeEvent(self, event) -> None:
        """Handle window close event.
        
        Args:
            event: Close event
        """
        # Save settings
        self._save_settings()
        
        # Check for unsaved changes
        if self.project_manager.has_unsaved_changes():
            reply = QMessageBox.question(
                self, 
                "Unsaved Changes",
                "There are unsaved changes. Do you want to save before exiting?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                self._on_save_project()
                event.accept()
            elif reply == QMessageBox.Cancel:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()
    
    def _on_new_project(self) -> None:
        """Handle new project action."""
        # Check for unsaved changes
        if self.project_manager.has_unsaved_changes():
            reply = QMessageBox.question(
                self, 
                "Unsaved Changes",
                "There are unsaved changes. Do you want to save before creating a new project?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                self._on_save_project()
            elif reply == QMessageBox.Cancel:
                return
        
        # Create new project
        self.project_manager.new_project()
        self.central_widget.update_for_project()
        self.case_explorer.update_for_project()
        self.status_bar.showMessage("New project created")
    
    def _on_open_project(self) -> None:
        """Handle open project action."""
        # Check for unsaved changes
        if self.project_manager.has_unsaved_changes():
            reply = QMessageBox.question(
                self, 
                "Unsaved Changes",
                "There are unsaved changes. Do you want to save before opening a new project?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                self._on_save_project()
            elif reply == QMessageBox.Cancel:
                return
        
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            "",
            "Project_Flow Project Files (*.pflow);;All Files (*)"
        )
        
        if file_path:
            try:
                self.project_manager.open_project(file_path)
                self.central_widget.update_for_project()
                self.case_explorer.update_for_project()
                self.status_bar.showMessage(f"Project opened: {file_path}")
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error Opening Project",
                    f"An error occurred while opening the project:\n{e}"
                )
    
    def _on_save_project(self) -> None:
        """Handle save project action."""
        if self.project_manager.project_file_path:
            try:
                self.project_manager.save_project()
                self.status_bar.showMessage(f"Project saved: {self.project_manager.project_file_path}")
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error Saving Project",
                    f"An error occurred while saving the project:\n{e}"
                )
        else:
            self._on_save_project_as()
    
    def _on_save_project_as(self) -> None:
        """Handle save project as action."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project As",
            "",
            "Project_Flow Project Files (*.pflow);;All Files (*)"
        )
        
        if file_path:
            if not file_path.endswith(".pflow"):
                file_path += ".pflow"
            
            try:
                self.project_manager.save_project(file_path)
                self.status_bar.showMessage(f"Project saved: {file_path}")
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error Saving Project",
                    f"An error occurred while saving the project:\n{e}"
                )
    
    def _on_preferences(self) -> None:
        """Handle preferences action."""
        # Open preferences dialog
        # In a real implementation, this would show a preferences dialog
        self.status_bar.showMessage("Preferences dialog not implemented yet")
    
    def _on_run_simulation(self) -> None:
        """Handle run simulation action."""
        # Run simulation
        # In a real implementation, this would start the simulation
        self.status_bar.showMessage("Running simulation...")
    
    def _on_stop_simulation(self) -> None:
        """Handle stop simulation action."""
        # Stop simulation
        # In a real implementation, this would stop the simulation
        self.status_bar.showMessage("Simulation stopped")
    
    def _on_about(self) -> None:
        """Handle about action."""
        QMessageBox.about(
            self,
            "About Project_Flow",
            "Project_Flow - OpenFOAM GUI\n\n"
            "Version: 0.1.0\n\n"
            "A graphical user interface for OpenFOAM CFD simulations."
        )
