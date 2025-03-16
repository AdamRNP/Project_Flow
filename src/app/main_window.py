# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 15:11:13 2025
@author: adamp
"""

import os
import sys
import subprocess
import glob
import tempfile
import webbrowser
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QDockWidget, QAction, QDialog,
                           QToolBar, QStatusBar, QFileDialog, QMessageBox,
                           QTreeView, QTextEdit, QVBoxLayout, QWidget, QHBoxLayout,  QGroupBox, QDialogButtonBox,
                           QSplitter, QMenu, QListWidget, QLabel, QComboBox, QPushButton, QTextEdit)
from PyQt5.QtCore import Qt, QSettings, QSize, QDir, QProcess
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem, QFont, QColor

# Import modules
from core.project import ProjectManager
from core.plugin import PluginManager
from ui.welcome import WelcomeWidget
from modules.mesh import MeshWidget
from modules.physics.physics_widget import PhysicsWidget

# Import placeholders for future modules
# These will be implemented in separate files
class GeometryWidget(QWidget):
    """Placeholder for geometry editor widget."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Geometry Import and Editing Interface"))
        
        # Add geometry import options
        import_label = QLabel("Import Geometry:")
        layout.addWidget(import_label)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["STL", "OBJ", "STEP", "IGES", "Parasolid"])
        layout.addWidget(self.format_combo)
        
        # Placeholder for 3D view
        view_label = QLabel("3D View will be displayed here")
        view_label.setStyleSheet("background-color: #f0f0f0; min-height: 300px;")
        layout.addWidget(view_label)
        
        # Operation buttons will be added here
        
class BoundaryWidget(QWidget):
    """Placeholder for boundary conditions configuration widget."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Boundary Conditions Configuration"))
        
        # Add boundary list
        self.boundary_list = QListWidget()
        self.boundary_list.addItems(["inlet", "outlet", "walls", "atmosphere"])
        layout.addWidget(self.boundary_list)
        
        # Placeholder for boundary settings
        settings_label = QLabel("Boundary settings will appear here when a boundary is selected")
        settings_label.setStyleSheet("background-color: #f0f0f0; min-height: 200px;")
        layout.addWidget(settings_label)

class SimulationWidget(QWidget):
    """Placeholder for simulation control widget."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Simulation Control"))
        
        # Add solver selection
        solver_label = QLabel("Solver:")
        layout.addWidget(solver_label)
        
        self.solver_combo = QComboBox()
        self.solver_combo.addItems(["simpleFoam", "pimpleFoam", "interFoam", "buoyantSimpleFoam"])
        layout.addWidget(self.solver_combo)
        
        # Add time control settings
        time_label = QLabel("Time Controls:")
        layout.addWidget(time_label)
        
        # Run controls will be added here
        
class PostProcessWidget(QWidget):
    """Placeholder for post-processing widget."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Post-Processing and Visualization"))
        
        # Add visualization options
        viz_label = QLabel("Visualization Options:")
        layout.addWidget(viz_label)
        
        # Placeholder for visualization window
        view_label = QLabel("Visualization will be displayed here")
        view_label.setStyleSheet("background-color: #f0f0f0; min-height: 300px;")
        layout.addWidget(view_label)

class ConsoleWidget(QTextEdit):
    """Console widget to display OpenFOAM command outputs."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("background-color: #202020; color: #f0f0f0; font-family: 'Courier New';")
        self.append("OpenFOAM Console Ready")
        
    def log(self, message):
        """Add a message to the console log."""
        self.append(message)

class ProjectExplorer(QTreeView):
    """Project explorer widget to navigate project files and components."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Project Files"])
        self.setModel(self.model)
        
        # Default project structure
        self.root = self.model.invisibleRootItem()
        
        # Add project structure
        self.create_default_structure()
        
        # Expand all items by default
        self.expandAll()
        
    def create_default_structure(self):
        """Create default project structure in the tree view."""
        # Main folders
        self.geometry_item = QStandardItem(QIcon("resources/icons/geometry.png"), "Geometry")
        self.mesh_item = QStandardItem(QIcon("resources/icons/mesh.png"), "Mesh")
        self.physics_item = QStandardItem(QIcon("resources/icons/physics.png"), "Physics")
        self.boundary_item = QStandardItem(QIcon("resources/icons/boundary.png"), "Boundary Conditions")
        self.simulation_item = QStandardItem(QIcon("resources/icons/simulation.png"), "Simulation")
        self.results_item = QStandardItem(QIcon("resources/icons/results.png"), "Results")
        
        # Add to root
        self.root.appendRow(self.geometry_item)
        self.root.appendRow(self.mesh_item)
        self.root.appendRow(self.physics_item)
        self.root.appendRow(self.boundary_item)
        self.root.appendRow(self.simulation_item)
        self.root.appendRow(self.results_item)
        
    def update_project_structure(self, project_path):
        """Update project structure based on loaded project."""
        # Update tree with actual project files (to be implemented)
        pass

class PropertyPanel(QWidget):
    """Property panel to display and edit properties of selected items."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Properties"))
        
        self.property_list = QListWidget()
        layout.addWidget(self.property_list)
        
        # Add placeholder properties
        self.property_list.addItems([
            "Name: Untitled",
            "Type: Project",
            "Created: Sun Mar 16 2025",
            "Modified: Sun Mar 16 2025"
        ])
        
class MainWindow(QMainWindow):
    """Main application window providing the core UI framework for OpenFOAM GUI."""
    
    def __init__(self):
        super().__init__()
        
        # Application settings
        self.settings = QSettings("OpenFOAM-GUI", "CFDInterface")
        self.current_project_path = None
        
        # Set window properties
        self.setWindowTitle("OpenFOAM CFD Interface")
        self.setWindowIcon(QIcon("resources/icons/app_icon.png"))
        self.resize(1280, 800)
        
        # Initialize core managers
        self.init_managers()
        
        # Set up UI components
        self.setup_menus()
        self.setup_toolbars()
        self.setup_central_widget()
        self.setup_dock_widgets()
        self.setup_status_bar()
        
        # Restore previous session state if available
        self.restore_window_state()
        
    def init_managers(self):
        """Initialize core application managers."""
        # Project manager handles saving/loading project files
        self.project_manager = ProjectManager()
        
        # Plugin manager handles discovery and loading of plugins
        self.plugin_manager = PluginManager(self)
        
        # Load available plugins
        plugin_count = self.plugin_manager.discover_plugins()
        print(f"Discovered {plugin_count} plugins")
        
    def setup_menus(self):
        """Set up application menu structure."""
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        
        new_action = QAction(QIcon("resources/icons/new.png"), "&New Project", self)
        new_action.setShortcut("Ctrl+N")
        new_action.setStatusTip("Create a new project")
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction(QIcon("resources/icons/open.png"), "&Open Project", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open an existing project")
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        save_action = QAction(QIcon("resources/icons/save.png"), "&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip("Save the current project")
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save &As...", self)
        save_as_action.setStatusTip("Save the project to a new location")
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("&Export OpenFOAM Case", self)
        export_action.setStatusTip("Export project as OpenFOAM case structure")
        export_action.triggered.connect(self.export_openfoam_case)
        file_menu.addAction(export_action)
        
        import_action = QAction("&Import OpenFOAM Case", self)
        import_action.setStatusTip("Import existing OpenFOAM case")
        import_action.triggered.connect(self.import_openfoam_case)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Setup menu
        setup_menu = self.menuBar().addMenu("&Setup")
        
        geometry_action = QAction("&Geometry", self)
        geometry_action.setStatusTip("Create or import geometry")
        geometry_action.triggered.connect(self.open_geometry)
        setup_menu.addAction(geometry_action)
        
        mesh_action = QAction("&Mesh", self)
        mesh_action.setStatusTip("Generate or import mesh")
        mesh_action.triggered.connect(self.open_mesh)
        setup_menu.addAction(mesh_action)
        
        physics_action = QAction("&Physics Models", self)
        physics_action.setStatusTip("Configure physics models")
        physics_action.triggered.connect(self.open_physics)
        setup_menu.addAction(physics_action)
        
        boundary_action = QAction("&Boundary Conditions", self)
        boundary_action.setStatusTip("Set boundary conditions")
        boundary_action.triggered.connect(self.open_boundary)
        setup_menu.addAction(boundary_action)
        
        # Simulation menu
        sim_menu = self.menuBar().addMenu("&Simulation")
        
        run_action = QAction(QIcon("resources/icons/run.png"), "&Run", self)
        run_action.setStatusTip("Run simulation")
        run_action.triggered.connect(self.run_simulation)
        sim_menu.addAction(run_action)
        
        monitor_action = QAction("&Monitor", self)
        monitor_action.setStatusTip("Monitor simulation progress")
        monitor_action.triggered.connect(self.monitor_simulation)
        sim_menu.addAction(monitor_action)
        
        # Results menu
        results_menu = self.menuBar().addMenu("&Results")
        
        post_action = QAction("&Post-processing", self)
        post_action.setStatusTip("Analyze simulation results")
        post_action.triggered.connect(self.open_postprocessing)
        results_menu.addAction(post_action)
        
        paraview_action = QAction("Open in &ParaView", self)
        paraview_action.setStatusTip("Open results in ParaView")
        paraview_action.triggered.connect(self.open_paraview)
        results_menu.addAction(paraview_action)
        
        # Tools menu
        tools_menu = self.menuBar().addMenu("&Tools")
        
        of_terminal_action = QAction("OpenFOAM &Terminal", self)
        of_terminal_action.setStatusTip("Open OpenFOAM terminal")
        of_terminal_action.triggered.connect(self.open_of_terminal)
        tools_menu.addAction(of_terminal_action)
        
        of_utilities_menu = tools_menu.addMenu("OpenFOAM &Utilities")
        
        checkMesh_action = QAction("&checkMesh", self)
        checkMesh_action.triggered.connect(lambda: self.run_of_utility("checkMesh"))
        of_utilities_menu.addAction(checkMesh_action)
        
        foamToVTK_action = QAction("&foamToVTK", self)
        foamToVTK_action.triggered.connect(lambda: self.run_of_utility("foamToVTK"))
        of_utilities_menu.addAction(foamToVTK_action)
        
        # Help menu
        help_menu = self.menuBar().addMenu("&Help")
        
        docs_action = QAction("OpenFOAM &Documentation", self)
        docs_action.triggered.connect(self.show_openfoam_docs)
        help_menu.addAction(docs_action)
        
        tutorials_action = QAction("&Tutorials", self)
        tutorials_action.triggered.connect(self.show_tutorials)
        help_menu.addAction(tutorials_action)
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_toolbars(self):
        """Create application toolbars."""
        # Main toolbar
        main_toolbar = QToolBar("Main")
        main_toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(main_toolbar)
        
        main_toolbar.addAction(QIcon("resources/icons/new.png"), "New Project", self.new_project)
        main_toolbar.addAction(QIcon("resources/icons/open.png"), "Open Project", self.open_project)
        main_toolbar.addAction(QIcon("resources/icons/save.png"), "Save Project", self.save_project)
        
        main_toolbar.addSeparator()
        
        # Add workflow buttons
        main_toolbar.addAction(QIcon("resources/icons/geometry.png"), "Geometry", self.open_geometry)
        main_toolbar.addAction(QIcon("resources/icons/mesh.png"), "Mesh", self.open_mesh)
        main_toolbar.addAction(QIcon("resources/icons/physics.png"), "Physics", self.open_physics)
        main_toolbar.addAction(QIcon("resources/icons/boundary.png"), "Boundary", self.open_boundary)
        
        main_toolbar.addSeparator()
        
        main_toolbar.addAction(QIcon("resources/icons/run.png"), "Run Simulation", self.run_simulation)
        main_toolbar.addAction(QIcon("resources/icons/results.png"), "Post-processing", self.open_postprocessing)
        
        # Allow toolbar to be customizable
        main_toolbar.setMovable(True)
        
    def setup_central_widget(self):
        """Set up the central widget with tab support."""
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tab_widget)
        
        # Add console widget at the bottom
        self.console = ConsoleWidget()
        
        # Create a splitter to separate main area and console
        self.main_splitter = QSplitter(Qt.Vertical)
        self.main_splitter.addWidget(self.tab_widget)
        self.main_splitter.addWidget(self.console)
        self.main_splitter.setStretchFactor(0, 4)  # Make the tab widget area larger
        self.main_splitter.setStretchFactor(1, 1)  # Make the console smaller
        
        self.setCentralWidget(self.main_splitter)
        
        # Add initial welcome tab
        welcome_widget = WelcomeWidget(self)
        self.tab_widget.addTab(welcome_widget, "Welcome")
        
        # Add existing modules
        self.physics_widget = PhysicsWidget()
        self.tab_widget.addTab(self.physics_widget, "Physics")
    
    def setup_dock_widgets(self):
        """Create dock widgets for different panels."""
        # Project explorer dock
        self.project_dock = QDockWidget("Project Explorer", self)
        self.project_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.project_explorer = ProjectExplorer(self)
        self.project_dock.setWidget(self.project_explorer)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.project_dock)
        
        # Properties dock
        self.properties_dock = QDockWidget("Properties", self)
        self.properties_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.property_panel = PropertyPanel(self)
        self.properties_dock.setWidget(self.property_panel)
        self.addDockWidget(Qt.RightDockWidgetArea, self.properties_dock)
        
    def setup_status_bar(self):
        """Set up the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def restore_window_state(self):
        """Restore window geometry and state from previous session."""
        if self.settings.contains("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))
        
        if self.settings.contains("windowState"):
            self.restoreState(self.settings.value("windowState"))
    
    def closeEvent(self, event):
        """Handle application close event."""
        # Save window state
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        
        # Check for unsaved changes
        if self.project_manager.has_unsaved_changes():
            reply = QMessageBox.question(
                self, 
                "Unsaved Changes",
                "The current project has unsaved changes. Do you want to save?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                saved = self.save_project()
                if not saved:
                    event.ignore()
                    return
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return
        
        event.accept()
    
    # Action handlers
    def new_project(self):
        """Create a new project."""
        if self.project_manager.has_unsaved_changes():
            reply = QMessageBox.question(
                self, 
                "Unsaved Changes",
                "The current project has unsaved changes. Do you want to save?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                saved = self.save_project()
                if not saved:
                    return
            elif reply == QMessageBox.Cancel:
                return
        
        # Create new project
        self.project_manager.create_new_project()
        self.current_project_path = None
        self.setWindowTitle("OpenFOAM CFD Interface - New Project")
        self.status_bar.showMessage("New project created")
        
        # Reset UI for new project
        self.console.log("New project created")
        
        # Clear existing tabs except Welcome
        for i in range(self.tab_widget.count() - 1, -1, -1):
            if self.tab_widget.tabText(i) != "Welcome":
                self.tab_widget.removeTab(i)
        
        # Reset project explorer
        self.project_explorer.create_default_structure()
    
    def open_project(self):
        """Open an existing project."""
        if self.project_manager.has_unsaved_changes():
            reply = QMessageBox.question(
                self, 
                "Unsaved Changes",
                "The current project has unsaved changes. Do you want to save?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                saved = self.save_project()
                if not saved:
                    return
            elif reply == QMessageBox.Cancel:
                return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            "",
            "OpenFOAM GUI Projects (*.ofp);;All Files (*)"
        )
        
        if file_path:
            try:
                self.project_manager.load_project(file_path)
                self.current_project_path = file_path
                
                project_name = os.path.basename(file_path)
                self.setWindowTitle(f"OpenFOAM CFD Interface - {project_name}")
                self.status_bar.showMessage(f"Project loaded: {project_name}")
                
                # Update UI with loaded project
                self.console.log(f"Project loaded from {file_path}")
                
                # Update project explorer
                self.project_explorer.update_project_structure(file_path)
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error Opening Project",
                    f"Could not open project file: {str(e)}"
                )
    
    def save_project(self):
        """Save the current project."""
        if not self.current_project_path:
            return self.save_project_as()
        
        try:
            self.project_manager.save_project(self.current_project_path)
            self.status_bar.showMessage(f"Project saved to {self.current_project_path}")
            self.console.log(f"Project saved to {self.current_project_path}")
            return True
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Saving Project",
                f"Could not save project: {str(e)}"
            )
            return False
    
    def save_project_as(self):
        """Save the project to a new location."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project As",
            "",
            "OpenFOAM GUI Projects (*.ofp);;All Files (*)"
        )
        
        if file_path:
            if not file_path.endswith('.ofp'):
                file_path += '.ofp'
                
            try:
                self.project_manager.save_project(file_path)
                self.current_project_path = file_path
                
                project_name = os.path.basename(file_path)
                self.setWindowTitle(f"OpenFOAM CFD Interface - {project_name}")
                self.status_bar.showMessage(f"Project saved as: {project_name}")
                self.console.log(f"Project saved as {file_path}")
                return True
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error Saving Project",
                    f"Could not save project: {str(e)}"
                )
        
        return False
    
    def close_tab(self, index):
        """Close a tab in the central widget."""
        # TODO: Check for unsaved changes in the tab
        self.tab_widget.removeTab(index)
    
    # New methods for export/import
    def export_openfoam_case(self):
        """Export current project as OpenFOAM case structure."""
        if not self.current_project_path:
            QMessageBox.warning(
                self,
                "No Project",
                "Please save the project before exporting as OpenFOAM case."
            )
            return
            
        export_dir = QFileDialog.getExistingDirectory(
            self,
            "Select Export Directory",
            ""
        )
        
        if export_dir:
            try:
                # Placeholder for actual export logic
                # TODO: Implement export to OpenFOAM case structure
                self.status_bar.showMessage(f"Project exported to OpenFOAM case: {export_dir}")
                self.console.log(f"Project exported to OpenFOAM case: {export_dir}")
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error Exporting Project",
                    f"Could not export project: {str(e)}"
                )
    
    def import_openfoam_case(self):
        """Import existing OpenFOAM case as a project."""
        case_dir = QFileDialog.getExistingDirectory(
            self,
            "Select OpenFOAM Case Directory",
            ""
        )
        
        if case_dir:
            try:
                # Placeholder for actual import logic
                # TODO: Implement import from OpenFOAM case structure
                self.status_bar.showMessage(f"OpenFOAM case imported: {case_dir}")
                self.console.log(f"OpenFOAM case imported: {case_dir}")
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error Importing Case",
                    f"Could not import OpenFOAM case: {str(e)}"
                )
    
    # Module opening methods
    def open_geometry(self):
        """Open geometry editor tab."""
        # First check if tab already exists
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "Geometry":
                self.tab_widget.setCurrentIndex(i)
                return
                
        # Create new geometry tab
        geometry_widget = GeometryWidget(self)
        self.tab_widget.addTab(geometry_widget, "Geometry")
        self.tab_widget.setCurrentWidget(geometry_widget)
        self.status_bar.showMessage("Geometry editor opened")
        self.console.log("Geometry editor opened")
        
    def open_mesh(self):
        """Open mesh generator tab."""
        # First check if tab already exists
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "Mesh":
                self.tab_widget.setCurrentIndex(i)
                return
                
        # Create new mesh tab
        mesh_widget = MeshWidget()
        self.tab_widget.addTab(mesh_widget, "Mesh")
        self.tab_widget.setCurrentWidget(mesh_widget)
        self.status_bar.showMessage("Mesh generator opened")
        self.console.log("Mesh generator opened")
        
    def open_physics(self):
        """Open physics model editor tab."""
        # First check if tab already exists
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "Physics":
                self.tab_widget.setCurrentIndex(i)
                return
                
        # Create new physics tab if not already created
        if hasattr(self, 'physics_widget'):
            self.tab_widget.addTab(self.physics_widget, "Physics")
            self.tab_widget.setCurrentWidget(self.physics_widget)
        else:
            self.physics_widget = PhysicsWidget()
            self.tab_widget.addTab(self.physics_widget, "Physics")
            self.tab_widget.setCurrentWidget(self.physics_widget)
            
        self.status_bar.showMessage("Physics model editor opened")
        self.console.log("Physics model editor opened")
        
    def open_boundary(self):
        """Open boundary condition editor tab."""
        # First check if tab already exists
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "Boundary Conditions":
                self.tab_widget.setCurrentIndex(i)
                return
                
        # Create new boundary tab
        boundary_widget = BoundaryWidget(self)
        self.tab_widget.addTab(boundary_widget, "Boundary Conditions")
        self.tab_widget.setCurrentWidget(boundary_widget)
        self.status_bar.showMessage("Boundary condition editor opened")
        self.console.log("Boundary condition editor opened")
    
    def open_simulation(self):
        """Open simulation control tab."""
        # First check if tab already exists
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "Simulation":
                self.tab_widget.setCurrentIndex(i)
                return
                
        # Create new simulation tab
        simulation_widget = SimulationWidget(self)
        self.tab_widget.addTab(simulation_widget, "Simulation")
        self.tab_widget.setCurrentWidget(simulation_widget)
        self.status_bar.showMessage("Simulation control opened")
        self.console.log("Simulation control opened")
    
    def open_postprocess(self):
        """Open post-processing and visualization tab."""
        # First check if tab already exists
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "Post-Processing":
                self.tab_widget.setCurrentIndex(i)
                return
                
        # Create new post-processing tab
        postprocess_widget = PostProcessWidget(self)
        self.tab_widget.addTab(postprocess_widget, "Post-Processing")
        self.tab_widget.setCurrentWidget(postprocess_widget)
        self.status_bar.showMessage("Post-processing opened")
        self.console.log("Post-processing opened")
    
    def run_simulation(self):
        """Run the current OpenFOAM simulation."""
        if not hasattr(self, 'project_manager') or not self.project_manager.current_path:
            QMessageBox.warning(
                self,
                "No Project",
                "Please save the project before running the simulation."
            )
            return
            
        # Check if case is exported
        case_dir = os.path.join(self.project_manager.current_path, "openfoam_case")
        if not os.path.exists(case_dir):
            reply = QMessageBox.question(
                self, 
                "Export Required",
                "The case needs to be exported to OpenFOAM format before running. Export now?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                self.export_openfoam_case()  # Export first
            else:
                return
        
        # Create simulation runner
        if not hasattr(self, 'simulation_process'):
            self.simulation_process = QProcess()
            self.simulation_process.readyReadStandardOutput.connect(self.process_output)
            self.simulation_process.readyReadStandardError.connect(self.process_error)
            self.simulation_process.finished.connect(self.simulation_finished)
        
        # Get the solver name from simulation settings
        # This is a placeholder, in a real implementation you would get this from the UI
        solver = "simpleFoam"  # Default solver
        
        # Start the simulation
        try:
            self.console.log(f"Starting simulation with {solver}...")
            self.status_bar.showMessage(f"Running {solver}...")
            
            # Change to case directory and run solver
            self.simulation_process.setWorkingDirectory(case_dir)
            self.simulation_process.start(solver, ["-case", "."])
            
            # Show simulation monitoring if not already visible
            self.open_simulation()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Simulation Error",
                f"Error starting simulation: {str(e)}"
            )
    
    def process_output(self):
        """Process standard output from simulation process."""
        if hasattr(self, 'simulation_process'):
            data = self.simulation_process.readAllStandardOutput().data().decode('utf-8')
            self.console.log(data.strip())
    
    def process_error(self):
        """Process standard error from simulation process."""
        if hasattr(self, 'simulation_process'):
            data = self.simulation_process.readAllStandardError().data().decode('utf-8')
            self.console.log_error(data.strip())
    
    def simulation_finished(self, exit_code, exit_status):
        """Handle simulation completion."""
        if exit_code == 0:
            self.status_bar.showMessage("Simulation completed successfully")
            self.console.log("Simulation completed successfully")
            
            # Automatically open post-processing
            reply = QMessageBox.question(
                self, 
                "Simulation Complete",
                "Simulation completed successfully. Open post-processing view?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                self.open_postprocess()
        else:
            self.status_bar.showMessage("Simulation failed")
            self.console.log_error(f"Simulation failed with exit code {exit_code}")
    
    def cancel_simulation(self):
        """Cancel the running simulation."""
        if hasattr(self, 'simulation_process') and self.simulation_process.state() != QProcess.NotRunning:
            reply = QMessageBox.question(
                self, 
                "Cancel Simulation",
                "Are you sure you want to cancel the running simulation?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.simulation_process.kill()
                self.status_bar.showMessage("Simulation cancelled")
                self.console.log("Simulation cancelled by user")
        else:
            self.status_bar.showMessage("No simulation running")
    
    def closeEvent(self, event):
        """Handle application close event."""
        if hasattr(self, 'project_manager') and self.project_manager.is_modified:
            reply = QMessageBox.question(
                self, 
                "Save Project",
                "The project has unsaved changes. Save before closing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            
            if reply == QMessageBox.Save:
                if self.save_project():
                    event.accept()
                else:
                    event.ignore()
            elif reply == QMessageBox.Cancel:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()
            
    def monitor_simulation(self):
        """Monitor the progress of a running OpenFOAM simulation.
        This method is triggered from the Simulation menu's Monitor action."""
        # Check if simulation is running
        if not hasattr(self, 'simulation_process') or self.simulation_process is None:
            QMessageBox.information(
                self,
                "Monitor Simulation",
                "No simulation is currently running."
            )
            self.status_bar.showMessage("No simulation running to monitor")
            return
            
        # If simulation is running, show the monitoring interface
        try:
            # Create monitoring tab if not exists
            if not hasattr(self, 'monitoring_widget'):
                self.monitoring_widget = QWidget()
                monitoring_layout = QVBoxLayout(self.monitoring_widget)
                
                # Add output display
                self.simulation_output = QTextEdit()
                self.simulation_output.setReadOnly(True)
                font = QFont("Courier New", 10)
                self.simulation_output.setFont(font)
                monitoring_layout.addWidget(QLabel("Simulation Output:"))
                monitoring_layout.addWidget(self.simulation_output)
                
                # Add progress information
                info_layout = QHBoxLayout()
                info_layout.addWidget(QLabel("Status:"))
                self.simulation_status = QLabel("Running")
                info_layout.addWidget(self.simulation_status)
                info_layout.addStretch()
                monitoring_layout.addLayout(info_layout)
                
                # Add control buttons
                button_layout = QHBoxLayout()
                stop_button = QPushButton("Stop Simulation")
                stop_button.clicked.connect(self.stop_simulation)
                button_layout.addWidget(stop_button)
                button_layout.addStretch()
                monitoring_layout.addLayout(button_layout)
                
                # Add to tabs
                index = self.tab_widget.addTab(self.monitoring_widget, "Simulation Monitor")
                self.tab_widget.setCurrentIndex(index)
            else:
                # Just switch to monitoring tab if it exists
                for i in range(self.tab_widget.count()):
                    if self.tab_widget.widget(i) is self.monitoring_widget:
                        self.tab_widget.setCurrentIndex(i)
                        break
            
            # Make sure process output connections are established
            if hasattr(self, 'simulation_process'):
                self.simulation_process.readyReadStandardOutput.connect(self.process_output)
                self.simulation_process.readyReadStandardError.connect(self.process_error)
            
            self.status_bar.showMessage("Monitoring simulation")
            self.console.log("Monitoring simulation")
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Monitor Error",
                f"Error setting up simulation monitoring: {str(e)}"
            )
    
    def process_output(self):
        """Process standard output from simulation process."""
        if hasattr(self, 'simulation_process') and hasattr(self, 'simulation_output'):
            data = self.simulation_process.readAllStandardOutput().data().decode('utf-8')
            self.console.log(data.strip())
            self.simulation_output.append(data.strip())
    
    def process_error(self):
        """Process standard error from simulation process."""
        if hasattr(self, 'simulation_process') and hasattr(self, 'simulation_output'):
            data = self.simulation_process.readAllStandardError().data().decode('utf-8')
            self.console.log_error(data.strip())
            self.simulation_output.append(f"<span style='color:red'>{data.strip()}</span>")
            self.simulation_output.setTextColor(QColor("red"))
            self.simulation_output.append(data.strip())
            self.simulation_output.setTextColor(QColor("black"))
    
    def open_postprocessing(self):
        """
        Open the postprocessing interface for visualizing and analyzing simulation results.
        """
        # Check if there are results to postprocess
        case_dir = self.get_current_case_directory()
        if not case_dir or not os.path.exists(case_dir):
            QMessageBox.warning(
                self,
                "No Case Available",
                "Please open or create a simulation case first."
            )
            self.status_bar.showMessage("No simulation case available for postprocessing")
            return
            
        # Check if simulation has results
        results_dir = os.path.join(case_dir, "postProcessing")
        if not os.path.exists(results_dir):
            QMessageBox.warning(
                self,
                "No Results Available",
                "No postprocessing results found. Run a simulation first or check the case directory."
            )
            self.status_bar.showMessage("No results found for postprocessing")
            return
        
        try:
            # Create a new tab for postprocessing if it doesn't exist
            if not hasattr(self, 'postprocessing_widget'):
                from PyQt5.QtWidgets import QSplitter, QTreeView, QTabWidget
                
                self.postprocessing_widget = QWidget()
                main_layout = QVBoxLayout(self.postprocessing_widget)
                
                # Create splitter for tree view and visualization area
                splitter = QSplitter()
                
                # Results tree view - left side
                self.results_tree = QTreeView()
                self.results_tree.setHeaderHidden(True)
                # Set up model for the tree view - simplified here
                # self.setup_results_tree_model()
                
                # Visualization area - right side
                self.visualization_tabs = QTabWidget()
                tab1 = QWidget()  # Placeholder for actual visualization
                self.visualization_tabs.addTab(tab1, "Visualize")
                
                splitter.addWidget(self.results_tree)
                splitter.addWidget(self.visualization_tabs)
                splitter.setSizes([200, 800])  # Default split sizes
                
                main_layout.addWidget(splitter)
                
                # Control buttons
                button_layout = QHBoxLayout()
                refresh_button = QPushButton("Refresh Results")
                export_button = QPushButton("Export Data")
                button_layout.addWidget(refresh_button)
                button_layout.addWidget(export_button)
                button_layout.addStretch()
                main_layout.addLayout(button_layout)
                
                # Add tab and switch to it
                index = self.tab_widget.addTab(self.postprocessing_widget, "Postprocessing")
                self.tab_widget.setCurrentIndex(index)
                
                # Connect signals
                refresh_button.clicked.connect(self.refresh_postprocessing)
                export_button.clicked.connect(self.export_postprocessing_data)
                
                # Load initial data
                self.load_postprocessing_data(results_dir)
            else:
                # Just switch to postprocessing tab if it exists
                for i in range(self.tab_widget.count()):
                    if self.tab_widget.widget(i) is self.postprocessing_widget:
                        self.tab_widget.setCurrentIndex(i)
                        break
            
            self.status_bar.showMessage("Postprocessing module opened")
            self.console.log("Opened postprocessing interface")
        
        except Exception as e:
            QMessageBox.critical(
                self,
                "Postprocessing Error",
                f"Error opening postprocessing: {str(e)}"
            )
            self.console.log_error(f"Failed to open postprocessing: {str(e)}")

    def get_current_case_directory(self):
        """Get the currently active OpenFOAM case directory."""
        # This is a placeholder - implement based on your app's structure
        if hasattr(self, 'current_case_dir') and self.current_case_dir:
            return self.current_case_dir
        return None

    def refresh_postprocessing(self):
        """Refresh the postprocessing data from the case directory."""
        case_dir = self.get_current_case_directory()
        if case_dir:
            results_dir = os.path.join(case_dir, "postProcessing")
            if os.path.exists(results_dir):
                self.load_postprocessing_data(results_dir)
                self.status_bar.showMessage("Postprocessing data refreshed")
            else:
                self.status_bar.showMessage("No postprocessing data found")
    
    def load_postprocessing_data(self, results_dir):
        """Load postprocessing data from the specified directory."""
        # Placeholder for actual data loading logic
        # This would typically involve reading OpenFOAM result files
        self.console.log(f"Loading postprocessing data from {results_dir}")
        # Implementation should populate the results tree and prepare data for visualization
    
    def export_postprocessing_data(self):
        """Export the current postprocessing data to a file."""
        # Placeholder for export functionality
        self.console.log("Exporting postprocessing data")
        # Implementation should provide file dialog and export options
    
    def open_paraview(self):
        """
        Open the current case in ParaView for visualization.
        This method launches ParaView with the current OpenFOAM case.
        """
        case_dir = self.get_current_case_directory()
        if not case_dir or not os.path.exists(case_dir):
            QMessageBox.warning(
                self,
                "No Case Available",
                "Please open or create a simulation case first."
            )
            self.status_bar.showMessage("No simulation case available for visualization")
            return
        
        # Check if there's anything to visualize
        if not any(os.path.exists(os.path.join(case_dir, d)) for d in 
                  ["postProcessing", "VTK", "0", "0.org", "1", "2", "3"]):
            reply = QMessageBox.question(
                self,
                "No Results Found",
                "No simulation results were found. Would you like to open ParaView anyway?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        try:
            # First, check if ParaView is in the system path
            paraview_cmd = "paraview"
            
            # On Windows, you might need to look in specific locations
            if sys.platform == "win32":
                # Try common installation paths
                potential_paths = [
                    os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "ParaView", "bin", "paraview.exe"),
                    os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "ParaView", "bin", "paraview.exe"),
                    # Add any other common ParaView installation locations for Windows
                ]
                
                for path in potential_paths:
                    if os.path.exists(path):
                        paraview_cmd = path
                        break
            
            # Check for OpenFOAM-specific paraview command
            # (e.g., paraFoam which is ParaView configured for OpenFOAM)
            parafoam_cmd = None
            for cmd in ["paraFoam", "paraview", "paraview5", "paraview4"]:
                try:
                    subprocess.run([cmd, "--version"], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE, 
                                   check=False)
                    parafoam_cmd = cmd
                    break
                except FileNotFoundError:
                    continue
            
            # Determine which command to use and arguments
            env = os.environ.copy()
            cmd_to_run = None
            args = []
            
            if parafoam_cmd == "paraFoam":
                # paraFoam is the OpenFOAM-specific ParaView launcher
                cmd_to_run = parafoam_cmd
                args = ["-case", case_dir]
            elif parafoam_cmd:
                # Regular ParaView but available in PATH
                cmd_to_run = parafoam_cmd
                
                # Check for OpenFOAM .foam file or create one
                foam_file = os.path.join(case_dir, f"{os.path.basename(case_dir)}.foam")
                if not os.path.exists(foam_file):
                    # Create a dummy .foam file for ParaView
                    with open(foam_file, 'w') as f:
                        f.write("# ParaView case file")
                
                args = [foam_file]
            elif os.path.exists(paraview_cmd):
                # Found ParaView executable but not in PATH
                cmd_to_run = paraview_cmd
                
                # Create .foam file as above
                foam_file = os.path.join(case_dir, f"{os.path.basename(case_dir)}.foam")
                if not os.path.exists(foam_file):
                    with open(foam_file, 'w') as f:
                        f.write("# ParaView case file")
                
                args = [foam_file]
            else:
                raise FileNotFoundError("ParaView executable not found. Please install ParaView or add it to your PATH.")
            
            # Launch ParaView
            self.console.log(f"Launching ParaView with command: {cmd_to_run} {' '.join(args)}")
            
            # Use QProcess for better integration with Qt
            self.paraview_process = QProcess()
            self.paraview_process.setWorkingDirectory(case_dir)
            
            # Set environment variables if needed
            self.paraview_process.setEnvironment([f"{key}={value}" for key, value in env.items()])
            
            # Start the process
            self.paraview_process.start(cmd_to_run, args)
            
            # Check if process started successfully
            if not self.paraview_process.waitForStarted(3000):  # Wait up to 3 seconds
                raise RuntimeError(f"Failed to start ParaView: {self.paraview_process.errorString()}")
            
            self.status_bar.showMessage("ParaView launched successfully")
        
        except FileNotFoundError as e:
            QMessageBox.critical(
                self,
                "ParaView Not Found",
                f"Could not find ParaView. Please make sure ParaView is installed and in your PATH.\n\nError: {str(e)}"
            )
            self.console.log_error(f"ParaView not found: {str(e)}")
        
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Launching ParaView",
                f"Failed to launch ParaView: {str(e)}"
            )
            self.console.log_error(f"Failed to launch ParaView: {str(e)}")
                
    
    def open_of_terminal(self):
        """
        Open a terminal with OpenFOAM environment activated.
        This provides access to all OpenFOAM commands in a shell.
        """
        try:
            # Get current case directory, if available
            case_dir = None
            if hasattr(self, 'project_manager') and hasattr(self.project_manager, 'current_case_dir'):
                case_dir = self.project_manager.current_case_dir
            
            # Determine operating system and appropriate terminal command
            terminal_cmd = None
            shell_args = []
            env = os.environ.copy()
            
            # Add OpenFOAM environment setup
            openfoam_bashrc = None
            
            # Linux systems
            if sys.platform.startswith('linux'):
                # Common terminal emulators
                for term in ["gnome-terminal", "xterm", "konsole", "terminator"]:
                    try:
                        subprocess.run(["which", term], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                        terminal_cmd = term
                        break
                    except FileNotFoundError:
                        continue
                        
                if terminal_cmd is None:
                    raise FileNotFoundError("Could not find a suitable terminal emulator")
                
                # Look for OpenFOAM environment setup files
                for path in ["/opt/openfoam*", "/usr/lib/openfoam*", "$HOME/OpenFOAM/OpenFOAM-*"]:
                    possible_paths = glob.glob(os.path.expandvars(path))
                    for p in possible_paths:
                        if os.path.exists(os.path.join(p, "etc", "bashrc")):
                            openfoam_bashrc = os.path.join(p, "etc", "bashrc")
                            break
                    if openfoam_bashrc:
                        break
                        
                # Configure terminal command based on the terminal type
                if terminal_cmd == "gnome-terminal":
                    shell_args = ["--", "bash", "-c"]
                elif terminal_cmd in ["xterm", "konsole", "terminator"]:
                    shell_args = ["-e", "bash", "-c"]
                    
            # macOS
            elif sys.platform == "darwin":
                terminal_cmd = "open"
                shell_args = ["-a", "Terminal"]
                
                # Look for OpenFOAM environment (often installed via brew)
                for path in ["/opt/openfoam*", "/usr/local/opt/openfoam*", "$HOME/OpenFOAM/OpenFOAM-*"]:
                    possible_paths = glob.glob(os.path.expandvars(path))
                    for p in possible_paths:
                        if os.path.exists(os.path.join(p, "etc", "bashrc")):
                            openfoam_bashrc = os.path.join(p, "etc", "bashrc")
                            break
                    if openfoam_bashrc:
                        break
                        
            # Windows
            elif sys.platform == "win32":
                # On Windows, OpenFOAM is typically installed via WSL or MinGW/MSYS2
                # First, try WSL
                try:
                    subprocess.run(["wsl", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                    terminal_cmd = "wsl"
                    # No additional shell args needed for basic WSL
                except FileNotFoundError:
                    # Try CMD if WSL not available
                    terminal_cmd = "cmd.exe"
                    shell_args = ["/k"]
                
                # For WSL, we don't need to set openfoam_bashrc, as it would be inside WSL
                if terminal_cmd != "wsl":
                    # For native Windows, look for environment setup (unlikely but possible)
                    for path in ["C:\\Program Files\\OpenFOAM*", "C:\\OpenFOAM*"]:
                        possible_paths = glob.glob(path)
                        for p in possible_paths:
                            setup_file = os.path.join(p, "etc", "bashrc")
                            if os.path.exists(setup_file):
                                openfoam_bashrc = setup_file
                                break
                        if openfoam_bashrc:
                            break
                
            if terminal_cmd is None:
                raise RuntimeError("Could not determine appropriate terminal command for your system")
            
            # Prepare the command to execute in the terminal
            commands = []
            
            # Change to case directory if provided
            if case_dir and os.path.exists(case_dir):
                if sys.platform == "win32" and terminal_cmd == "wsl":
                    # For WSL, convert Windows path to WSL path
                    wsl_path = subprocess.check_output(
                        ["wsl", "wslpath", "-a", case_dir],
                        universal_newlines=True
                    ).strip()
                    commands.append(f"cd {wsl_path}")
                else:
                    commands.append(f"cd {case_dir}")
            
            # Source OpenFOAM environment if found
            if openfoam_bashrc:
                commands.append(f"source {openfoam_bashrc}")
                commands.append("echo 'OpenFOAM environment loaded.'")
            else:
                # If no OpenFOAM setup file found, try to use aliases if they exist
                commands.append("which openfoam &>/dev/null && openfoam 2>/dev/null || echo 'OpenFOAM environment not found. Please source it manually.'")
                
            # Create command string
            command_str = "; ".join(commands)
            
            # For interactive shells, add final bash to keep terminal open
            if not sys.platform == "darwin":  # macOS Terminal handles this automatically
                command_str += "; exec bash"
            
            if sys.platform == "win32" and terminal_cmd == "wsl":
                # Special handling for WSL
                subprocess.Popen([terminal_cmd, "--", "bash", "-c", command_str])
            elif sys.platform == "darwin":
                # Special handling for macOS
                if command_str:
                    # Create a temporary script to run in Terminal
                    temp_script = tempfile.NamedTemporaryFile(delete=False, suffix='.command')
                    temp_script.write(f"#!/bin/bash\n{command_str}\n".encode('utf-8'))
                    temp_script.close()
                    os.chmod(temp_script.name, 0o755)  # Make executable
                    
                    # Open the script with Terminal
                    subprocess.Popen([terminal_cmd, temp_script.name])
                else:
                    # Just open Terminal
                    subprocess.Popen(shell_args)
            else:
                # Linux and Windows CMD
                full_command = shell_args + [command_str] if command_str else shell_args
                subprocess.Popen([terminal_cmd] + full_command)
                
            self.status_bar.showMessage("OpenFOAM terminal launched")
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Terminal Launch Error",
                f"Could not open OpenFOAM terminal: {str(e)}"
            )
            if hasattr(self, 'console') and hasattr(self.console, 'log_error'):
                self.console.log_error(f"Failed to open OpenFOAM terminal: {str(e)}")

    def show_openfoam_docs(self):
        """
        Open the OpenFOAM documentation in the default web browser.
        Shows either online documentation or local docs if available.
        """
        try:
            # URLs for online documentation
            online_doc_urls = {
                "OpenFOAM Foundation": "https://openfoam.org/documentation/",
                "OpenFOAM ESI": "https://www.openfoam.com/documentation/",
                "OpenFOAM Wiki": "https://openfoamwiki.net/index.php/Main_Page"
            }
            
            # Check for local documentation
            local_doc_paths = []
            
            # Look in common installation locations for OpenFOAM documentation
            if sys.platform.startswith('linux') or sys.platform == "darwin":
                # Common Linux/macOS installation paths
                for path in ["/opt/openfoam*", "/usr/lib/openfoam*", "/usr/local/openfoam*", 
                            "$HOME/OpenFOAM/OpenFOAM-*"]:
                    possible_paths = glob.glob(os.path.expandvars(path))
                    for p in possible_paths:
                        doc_path = os.path.join(p, "doc", "Guides")
                        if os.path.exists(doc_path):
                            local_doc_paths.append(doc_path)
                        
                        # Check for user guide PDF
                        user_guide = os.path.join(p, "doc", "UserGuide.pdf")
                        if os.path.exists(user_guide):
                            local_doc_paths.append(user_guide)
            
            elif sys.platform == "win32":
                # Windows installations (could be in Program Files or WSL)
                for path in ["C:\\Program Files\\OpenFOAM*", 
                             os.path.expandvars("%USERPROFILE%\\AppData\\Local\\OpenFOAM*")]:
                    possible_paths = glob.glob(path)
                    for p in possible_paths:
                        doc_path = os.path.join(p, "doc")
                        if os.path.exists(doc_path):
                            local_doc_paths.append(doc_path)
            
            # Create a dialog for the user to choose documentation
            dialog = QDialog(self)
            dialog.setWindowTitle("OpenFOAM Documentation")
            dialog.setMinimumWidth(400)
            layout = QVBoxLayout(dialog)
            
            info_label = QLabel("Select OpenFOAM documentation to view:")
            layout.addWidget(info_label)
            
            # Add options for local documentation
            if local_doc_paths:
                local_group = QGroupBox("Local Documentation")
                local_layout = QVBoxLayout()
                
                for path in local_doc_paths:
                    button = QPushButton(os.path.basename(path))
                    button.clicked.connect(lambda checked, p=path: self.open_local_doc(p))
                    local_layout.addWidget(button)
                    
                local_group.setLayout(local_layout)
                layout.addWidget(local_group)
            
            # Add options for online documentation
            online_group = QGroupBox("Online Documentation")
            online_layout = QVBoxLayout()
            
            for name, url in online_doc_urls.items():
                button = QPushButton(name)
                button.clicked.connect(lambda checked, u=url: self.open_url(u))
                online_layout.addWidget(button)
                
            online_group.setLayout(online_layout)
            layout.addWidget(online_group)
            
            # Add close button
            button_box = QDialogButtonBox(QDialogButtonBox.Close)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)
            
            dialog.setLayout(layout)
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Documentation Error",
                f"Could not open OpenFOAM documentation: {str(e)}"
            )
            if hasattr(self, 'console') and hasattr(self.console, 'log_error'):
                self.console.log_error(f"Failed to open documentation: {str(e)}")
        
    def open_local_doc(self, path):
        """Open local documentation file or directory."""
        try:
            if os.path.isdir(path):
                # Open directory in file explorer
                if sys.platform == "win32":
                    os.startfile(path)
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", path])
                else:
                    subprocess.Popen(["xdg-open", path])
            else:
                # Open file with default application
                if sys.platform == "win32":
                    os.startfile(path)
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", path])
                else:
                    subprocess.Popen(["xdg-open", path])
                    
            self.status_bar.showMessage(f"Opened documentation: {path}")
            
        except Exception as e:
            QMessageBox.warning(
                self,
                "Open Error",
                f"Could not open {path}: {str(e)}"
            )
    
    def open_url(self, url):
        """Open URL in the default web browser."""
        try:
            webbrowser.open(url)
            self.status_bar.showMessage(f"Opened documentation: {url}")
        except Exception as e:
            QMessageBox.warning(
                self,
                "Browser Error",
                f"Could not open browser to {url}: {str(e)}"
            )
            
    def show_tutorials(self):
        """
        Display OpenFOAM tutorials in a categorized browser window.
        Allows users to explore and load example cases for learning purposes.
        """
        try:
            # Import required modules if not at the top of the file
            from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                                        QTreeWidget, QTreeWidgetItem, QSplitter,
                                        QPushButton, QTextEdit, QFileDialog,
                                        QLabel, QDialogButtonBox)
            import os
            import glob
            import subprocess
            
            # Create tutorial browser dialog
            dialog = QDialog(self)
            dialog.setWindowTitle("OpenFOAM Tutorials")
            dialog.resize(900, 600)
            
            # Main layout
            layout = QVBoxLayout(dialog)
            
            # Create splitter for tutorial tree and description panel
            splitter = QSplitter(dialog)
            
            # Create tree widget for tutorials
            tutorial_tree = QTreeWidget()
            tutorial_tree.setHeaderLabels(["Tutorial Cases"])
            tutorial_tree.setMinimumWidth(300)
            
            # Create description panel
            description_panel = QWidget()
            desc_layout = QVBoxLayout(description_panel)
            
            # Add title and description fields
            title_label = QLabel("<b>Select a tutorial</b>")
            desc_layout.addWidget(title_label)
            
            description = QTextEdit()
            description.setReadOnly(True)
            desc_layout.addWidget(description)
            
            # Add buttons for actions
            button_layout = QHBoxLayout()
            
            open_button = QPushButton("Open Tutorial")
            open_button.setEnabled(False)
            open_button.clicked.connect(lambda: self.open_tutorial(
                tutorial_tree.currentItem().data(0, Qt.UserRole)))
            
            copy_button = QPushButton("Copy to Project")
            copy_button.setEnabled(False)
            copy_button.clicked.connect(lambda: self.copy_tutorial_to_project(
                tutorial_tree.currentItem().data(0, Qt.UserRole)))
            
            docs_button = QPushButton("View Documentation")
            docs_button.setEnabled(False)
            
            button_layout.addWidget(open_button)
            button_layout.addWidget(copy_button)
            button_layout.addWidget(docs_button)
            desc_layout.addLayout(button_layout)
            
            # Add components to splitter
            splitter.addWidget(tutorial_tree)
            splitter.addWidget(description_panel)
            splitter.setSizes([300, 600])
            
            # Add splitter to main layout
            layout.addWidget(splitter)
            
            # Add close button
            button_box = QDialogButtonBox(QDialogButtonBox.Close)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)
            
            # Tutorial data structure
            tutorial_categories = {
                "Basic": {
                    "description": "Fundamental cases demonstrating basic OpenFOAM usage",
                    "cases": []
                },
                "Incompressible Flow": {
                    "description": "Cases for incompressible fluid flow simulations",
                    "cases": []
                },
                "Compressible Flow": {
                    "description": "Cases for compressible fluid flow simulations",
                    "cases": []
                },
                "Heat Transfer": {
                    "description": "Cases demonstrating heat transfer and thermal analysis",
                    "cases": []
                },
                "Multiphase Flow": {
                    "description": "Cases for multiphase and interface tracking simulations",
                    "cases": []
                },
                "Turbulence": {
                    "description": "Cases demonstrating various turbulence models",
                    "cases": []
                },
                "Other": {
                    "description": "Additional tutorial cases",
                    "cases": []
                }
            }
            
            # Populate tutorial categories from the filesystem
            tutorial_paths = []
            
            # Look for OpenFOAM tutorial directories in standard locations
            of_paths = self.find_openfoam_paths()
            
            for of_path in of_paths:
                tutorial_dir = os.path.join(of_path, "tutorials")
                if os.path.exists(tutorial_dir):
                    tutorial_paths.append(tutorial_dir)
            
            # Process tutorial directories and categorize them
            for tutorial_dir in tutorial_paths:
                self.process_tutorial_directory(tutorial_dir, tutorial_categories)
            
            # Populate tree widget with tutorial categories
            for category, data in tutorial_categories.items():
                if data["cases"]:  # Only add categories that have cases
                    category_item = QTreeWidgetItem([category])
                    tutorial_tree.addTopLevelItem(category_item)
                    
                    for case in data["cases"]:
                        case_item = QTreeWidgetItem([os.path.basename(case["path"])])
                        case_item.setData(0, Qt.UserRole, case)
                        category_item.addChild(case_item)
                    
                    category_item.setExpanded(True)
            
            # Connect signals
            def on_tutorial_selected(item, column):
                # Enable/disable buttons based on selection
                is_case = item.parent() is not None
                open_button.setEnabled(is_case)
                copy_button.setEnabled(is_case)
                docs_button.setEnabled(is_case)
                
                if is_case:
                    case_data = item.data(0, Qt.UserRole)
                    title_label.setText(f"<b>{item.text(0)}</b>")
                    
                    # Load and display description
                    desc_text = self.get_tutorial_description(case_data["path"])
                    description.setHtml(desc_text)
                else:
                    # Show category description
                    title_label.setText(f"<b>{item.text(0)}</b>")
                    category_desc = tutorial_categories.get(item.text(0), {}).get("description", "")
                    description.setHtml(f"<p>{category_desc}</p>")
                    description.append(f"<p>Number of cases: {item.childCount()}</p>")
            
            tutorial_tree.itemClicked.connect(on_tutorial_selected)
            
            # Show dialog
            dialog.exec_()
        
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Tutorial Browser Error",
                f"Could not open tutorial browser: {str(e)}"
            )
            if hasattr(self, 'console') and hasattr(self.console, 'log_error'):
                self.console.log_error(f"Failed to open tutorial browser: {str(e)}")
    
    def find_openfoam_paths(self):
        """Find OpenFOAM installation directories."""
        of_paths = []
        
        if sys.platform.startswith('linux') or sys.platform == "darwin":
            # Common Linux/macOS installation paths
            for path in ["/opt/openfoam*", "/usr/lib/openfoam*", "/usr/local/openfoam*", 
                        "$HOME/OpenFOAM/OpenFOAM-*"]:
                of_paths.extend(glob.glob(os.path.expandvars(path)))
        
        elif sys.platform == "win32":
            # Windows installations
            for path in ["C:\\Program Files\\OpenFOAM*", 
                         os.path.expandvars("%USERPROFILE%\\AppData\\Local\\OpenFOAM*")]:
                of_paths.extend(glob.glob(path))
        
        return of_paths
    
    def process_tutorial_directory(self, tutorial_dir, categories):
        """Process tutorial directory and categorize tutorials."""
        # Map directory names to categories
        dir_to_category = {
            "basic": "Basic",
            "incompressible": "Incompressible Flow",
            "compressible": "Compressible Flow",
            "heatTransfer": "Heat Transfer",
            "multiphase": "Multiphase Flow",
            "combustion": "Multiphase Flow",  # Often involves multiphase
            "DNS": "Turbulence",
            "DNSCWE": "Turbulence",
            "LES": "Turbulence",
            "electromagnetics": "Other",
            "finiteArea": "Other",
            "lagrangian": "Other",
            "mesh": "Basic",
            "multiphysics": "Other",
            "stressAnalysis": "Other",
            "verificationAndValidation": "Other"
        }
        
        # Walk through tutorial directories
        for root, dirs, files in os.walk(tutorial_dir):
            # Check if this is a case directory (contains system/controlDict)
            if os.path.exists(os.path.join(root, "system", "controlDict")):
                # Determine category
                relative_path = os.path.relpath(root, tutorial_dir)
                parts = relative_path.split(os.path.sep)
                
                category = "Other"
                for part in parts:
                    if part in dir_to_category:
                        category = dir_to_category[part]
                        break
                
                # Add to appropriate category
                case_info = {
                    "path": root,
                    "name": os.path.basename(root),
                    "category": category
                }
                
                categories[category]["cases"].append(case_info)
    
    def get_tutorial_description(self, case_path):
        """Generate HTML description for a tutorial case."""
        html = "<div style='font-family: Arial; font-size: 10pt;'>"
        
        # Add case path
        html += f"<p><b>Path:</b> {case_path}</p>"
        
        # Check for README file
        readme_path = os.path.join(case_path, "README")
        if os.path.exists(readme_path):
            try:
                with open(readme_path, 'r') as f:
                    readme_content = f.read()
                html += "<p><b>README:</b></p>"
                html += f"<pre>{readme_content}</pre>"
            except:
                html += "<p>README file exists but could not be read.</p>"
        
        # Check for controlDict to get solver info
        control_dict_path = os.path.join(case_path, "system", "controlDict")
        if os.path.exists(control_dict_path):
            try:
                application = None
                start_time = None
                end_time = None
                
                with open(control_dict_path, 'r') as f:
                    for line in f:
                        if "application" in line and ";" in line:
                            application = line.split()[1].rstrip(";")
                        if "startTime" in line and ";" in line:
                            start_time = line.split()[1].rstrip(";")
                        if "endTime" in line and ";" in line:
                            end_time = line.split()[1].rstrip(";")
                
                html += "<p><b>Simulation Details:</b></p>"
                html += "<ul>"
                if application:
                    html += f"<li>Solver: {application}</li>"
                if start_time:
                    html += f"<li>Start Time: {start_time}</li>"
                if end_time:
                    html += f"<li>End Time: {end_time}</li>"
                html += "</ul>"
            except:
                html += "<p>Error reading controlDict file.</p>"
        
        # List key directories
        html += "<p><b>Case Structure:</b></p><ul>"
        for dir_name in ["0", "0.orig", "constant", "system"]:
            dir_path = os.path.join(case_path, dir_name)
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                html += f"<li>{dir_name}/</li>"
        html += "</ul>"
        
        html += "</div>"
        return html
    
    def open_tutorial(self, case_data):
        """Open a tutorial case in the file manager."""
        path = case_data["path"]
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
                
            self.status_bar.showMessage(f"Opened tutorial: {path}")
        except Exception as e:
            QMessageBox.warning(
                self,
                "Open Error",
                f"Could not open tutorial at {path}: {str(e)}"
            )
    
    def copy_tutorial_to_project(self, case_data):
        """Copy a tutorial case to the current project directory."""
        source_path = case_data["path"]
        
        # Ask for destination directory
        dest_dir = QFileDialog.getExistingDirectory(
            self, 
            "Select Destination Directory",
            os.path.expanduser("~")
        )
        
        if not dest_dir:
            return
        
        try:
            # Create destination case directory
            case_name = os.path.basename(source_path)
            target_path = os.path.join(dest_dir, case_name)
            
            # Check if directory already exists
            if os.path.exists(target_path):
                confirm = QMessageBox.question(
                    self,
                    "Directory Exists",
                    f"The directory {target_path} already exists. Overwrite?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if confirm == QMessageBox.No:
                    return
            
            # Copy files using system commands for better handling of special files
            if sys.platform == "win32":
                subprocess.run(["xcopy", source_path, target_path, "/E", "/I", "/Y"], 
                             shell=True, check=True)
            else:
                subprocess.run(["cp", "-r", source_path, target_path], check=True)
            
            self.status_bar.showMessage(f"Tutorial copied to: {target_path}")
            
            # Offer to open the copied tutorial
            confirm = QMessageBox.question(
                self,
                "Open Tutorial",
                f"Tutorial copied successfully. Would you like to open it now?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if confirm == QMessageBox.Yes:
                # Logic to open the tutorial in the application
                # This would depend on your application's project loading mechanism
                if hasattr(self, 'load_project'):
                    self.load_project(target_path)
                else:
                    # Just open the directory
                    self.open_tutorial({"path": target_path})
                    
        except Exception as e:
            QMessageBox.critical(
                self,
                "Copy Error",
                f"Failed to copy tutorial: {str(e)}"
            )

    def show_about(self):
        """
        Display information about the OpenFOAM GUI application.
        Shows version information, credits, and licensing details.
        """
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
        from PyQt5.QtGui import QPixmap, QFont
        from PyQt5.QtCore import Qt
        
        # Create about dialog
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About OpenFOAM CFD Interface")
        about_dialog.setFixedSize(550, 400)
        
        # Dialog layout
        layout = QVBoxLayout(about_dialog)
        layout.setSpacing(10)
        
        # Application name with larger font
        app_name = QLabel("OpenFOAM CFD Interface")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        app_name.setFont(font)
        app_name.setAlignment(Qt.AlignCenter)
        layout.addWidget(app_name)
        
        # Version information
        version_label = QLabel("Version 1.0.0")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        # Try to add OpenFOAM logo if available
        try:
            # Attempt to find an OpenFOAM logo in standard locations
            logo_paths = [
                os.path.join(os.path.dirname(__file__), "resources/openfoam_logo.png"),
                "/usr/share/OpenFOAM/images/openfoam_logo.png",
                os.path.expanduser("~/.OpenFOAM/images/openfoam_logo.png")
            ]
            
            logo_path = None
            for path in logo_paths:
                if os.path.exists(path):
                    logo_path = path
                    break
            
            if logo_path:
                logo_label = QLabel()
                pixmap = QPixmap(logo_path)
                scaled_pixmap = pixmap.scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(scaled_pixmap)
                logo_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(logo_label)
        except Exception:
            # If logo can't be loaded, just skip it
            pass
        
        # Description
        description = QLabel(
            "<p>A graphical user interface for setting up, running, and analyzing "
            "Computational Fluid Dynamics (CFD) simulations with OpenFOAM.</p>"
            "<p>This application provides an integrated environment for the complete "
            "CFD workflow, from mesh generation to post-processing.</p>"
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)
        
        # OpenFOAM information
        openfoam_info = QLabel(
            "<p><b>OpenFOAM</b> (Open Field Operation And Manipulation) is a free, "
            "open source CFD software package developed by OpenCFD Ltd and distributed "
            "by the OpenFOAM Foundation.</p>"
            "<p>Visit <a href='https://www.openfoam.com'>www.openfoam.com</a> for more information.</p>"
        )
        openfoam_info.setWordWrap(True)
        openfoam_info.setTextFormat(Qt.RichText)
        openfoam_info.setOpenExternalLinks(True)
        layout.addWidget(openfoam_info)
        
        # Copyright
        copyright_label = QLabel(
            "© 2023-2025 OpenFOAM GUI Contributors\n"
            "OpenFOAM and OpenCFD are registered trademarks of OpenCFD Ltd."
        )
        copyright_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(copyright_label)
        
        # License information
        license_label = QLabel(
            "<p>This program is free software: you can redistribute it and/or modify "
            "it under the terms of the GNU General Public License as published by "
            "the Free Software Foundation, either version 3 of the License, or "
            "(at your option) any later version.</p>"
        )
        license_label.setWordWrap(True)
        license_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(license_label)
        
        # Add close button
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.rejected.connect(about_dialog.reject)
        layout.addWidget(button_box)
        
        # Show the dialog
        about_dialog.exec_()



class ConsoleOutput(QTextEdit):
    """Console widget for displaying output messages."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setStyleSheet(
            "background-color: #f0f0f0; font-family: Consolas, Monaco, monospace; font-size: 10pt;"
        )
    
    def log(self, message):
        """Log a normal message to the console."""
        if not message:
            return
            
        self.append(f"[INFO] {message}")
        # Ensure the latest message is visible
        cursor = self.textCursor()
        cursor.movePosition(cursor.End)
        self.setTextCursor(cursor)
    
    def log_error(self, message):
        """Log an error message to the console."""
        if not message:
            return
            
        self.append(f'<span style="color:red">[ERROR] {message}</span>')
        # Ensure the latest message is visible
        cursor = self.textCursor()
        cursor.movePosition(cursor.End)
        self.setTextCursor(cursor)
    
    def log_warning(self, message):
        """Log a warning message to the console."""
        if not message:
            return
            
        self.append(f'<span style="color:orange">[WARNING] {message}</span>')
        # Ensure the latest message is visible
        cursor = self.textCursor()
        cursor.movePosition(cursor.End)
        self.setTextCursor(cursor)
    
    def clear_console(self):
        """Clear the console output."""
        self.clear()
        

def main():
    """Application entry point."""
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    app.setApplicationName("OpenFOAM GUI")
    app.setOrganizationName("CFD Tools")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

