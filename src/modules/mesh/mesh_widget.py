# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 15:34:31 2025

@author: adamp
"""

## src/modules/mesh/mesh_widget.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                            QLabel, QPushButton, QComboBox, QSpinBox, 
                            QDoubleSpinBox, QGroupBox, QFormLayout, QFileDialog,
                            QCheckBox, QTableWidget, QTableWidgetItem, QMessageBox)
from PyQt5.QtCore import pyqtSignal, Qt
import os

class MeshWidget(QWidget):
    """Main widget for mesh generation and manipulation."""
    
    mesh_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.mesh_file = None
        self.mesh_type = None
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the mesh configuration UI."""
        main_layout = QVBoxLayout(self)
        
        # Create tabs for different mesh operations
        self.tabs = QTabWidget()
        
        # Import tab
        self.import_tab = QWidget()
        self.setup_import_tab()
        self.tabs.addTab(self.import_tab, "Import Mesh")
        
        # Generate tab
        self.generate_tab = QWidget()
        self.setup_generate_tab()
        self.tabs.addTab(self.generate_tab, "Generate Mesh")
        
        # SnappyHexMesh tab (OpenFOAM-specific mesh generator)
        self.snappy_tab = QWidget()
        self.setup_snappy_tab()
        self.tabs.addTab(self.snappy_tab, "SnappyHexMesh")
        
        # Quality check tab
        self.quality_tab = QWidget()
        self.setup_quality_tab()
        self.tabs.addTab(self.quality_tab, "Quality Check")
        
        main_layout.addWidget(self.tabs)
        
        # Mesh information section
        info_group = QGroupBox("Mesh Information")
        info_layout = QFormLayout()
        
        self.mesh_status = QLabel("No mesh loaded")
        info_layout.addRow("Status:", self.mesh_status)
        
        self.cell_count = QLabel("0")
        info_layout.addRow("Cell Count:", self.cell_count)
        
        self.face_count = QLabel("0")
        info_layout.addRow("Face Count:", self.face_count)
        
        self.boundary_count = QLabel("0")
        info_layout.addRow("Boundary Count:", self.boundary_count)
        
        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.view_mesh_btn = QPushButton("View Mesh")
        self.view_mesh_btn.clicked.connect(self.view_mesh)
        self.view_mesh_btn.setEnabled(False)
        button_layout.addWidget(self.view_mesh_btn)
        
        button_layout.addStretch(1)
        
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_mesh)
        button_layout.addWidget(self.apply_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_mesh)
        button_layout.addWidget(self.reset_button)
        
        main_layout.addLayout(button_layout)
        
    def setup_import_tab(self):
        """Setup the mesh import tab."""
        layout = QVBoxLayout(self.import_tab)
        
        # Mesh format selection
        format_group = QGroupBox("Mesh Format")
        format_layout = QFormLayout()
        
        self.mesh_format = QComboBox()
        self.mesh_format.addItems(["OpenFOAM", "STL", "Fluent (.msh)", "CGNS", "Other"])
        format_layout.addRow("Format:", self.mesh_format)
        
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)
        
        # File selection
        file_group = QGroupBox("Mesh File")
        file_layout = QHBoxLayout()
        
        self.file_path = QLabel("No file selected")
        file_layout.addWidget(self.file_path, 1)
        
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_mesh_file)
        file_layout.addWidget(self.browse_btn)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Import options
        options_group = QGroupBox("Import Options")
        options_layout = QFormLayout()
        
        self.scale_factor = QDoubleSpinBox()
        self.scale_factor.setRange(0.001, 1000)
        self.scale_factor.setValue(1.0)
        options_layout.addRow("Scale Factor:", self.scale_factor)
        
        self.convert_to_meters = QCheckBox("Convert to meters")
        self.convert_to_meters.setChecked(True)
        options_layout.addRow("", self.convert_to_meters)
        
        self.clean_topology = QCheckBox("Clean topology")
        self.clean_topology.setChecked(True)
        options_layout.addRow("", self.clean_topology)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Import button
        self.import_btn = QPushButton("Import")
        self.import_btn.clicked.connect(self.import_mesh)
        layout.addWidget(self.import_btn)
        
        layout.addStretch(1)
        
    def setup_generate_tab(self):
        """Setup the mesh generation tab."""
        layout = QVBoxLayout(self.generate_tab)
        
        # Base mesh type selection
        mesh_type_group = QGroupBox("Mesh Type")
        mesh_type_layout = QFormLayout()
        
        self.base_mesh_type = QComboBox()
        self.base_mesh_type.addItems(["Block Mesh", "Hex Mesh", "Tetrahedral Mesh", "Polyhedral Mesh"])
        self.base_mesh_type.currentIndexChanged.connect(self.update_mesh_options)
        mesh_type_layout.addRow("Type:", self.base_mesh_type)
        
        mesh_type_group.setLayout(mesh_type_layout)
        layout.addWidget(mesh_type_group)
        
        # Mesh generation parameters
        self.mesh_params_group = QGroupBox("Mesh Parameters")
        self.mesh_params_layout = QFormLayout()
        
        self.cell_count_x = QSpinBox()
        self.cell_count_x.setRange(1, 1000)
        self.cell_count_x.setValue(20)
        self.mesh_params_layout.addRow("Cells X:", self.cell_count_x)
        
        self.cell_count_y = QSpinBox()
        self.cell_count_y.setRange(1, 1000)
        self.cell_count_y.setValue(20)
        self.mesh_params_layout.addRow("Cells Y:", self.cell_count_y)
        
        self.cell_count_z = QSpinBox()
        self.cell_count_z.setRange(1, 1000)
        self.cell_count_z.setValue(20)
        self.mesh_params_layout.addRow("Cells Z:", self.cell_count_z)
        
        self.mesh_grading = QDoubleSpinBox()
        self.mesh_grading.setRange(0.1, 10)
        self.mesh_grading.setValue(1.0)
        self.mesh_params_layout.addRow("Grading:", self.mesh_grading)
        
        self.mesh_params_group.setLayout(self.mesh_params_layout)
        layout.addWidget(self.mesh_params_group)
        
        # Generate button
        self.generate_btn = QPushButton("Generate Mesh")
        self.generate_btn.clicked.connect(self.generate_mesh)
        layout.addWidget(self.generate_btn)
        
        layout.addStretch(1)
        
    def setup_snappy_tab(self):
        """Setup the SnappyHexMesh specific tab."""
        layout = QVBoxLayout(self.snappy_tab)
        
        # Base mesh selection
        base_mesh_group = QGroupBox("Base Mesh")
        base_mesh_layout = QFormLayout()
        
        self.use_current_mesh = QCheckBox("Use current mesh as base")
        self.use_current_mesh.setChecked(False)
        base_mesh_layout.addRow("", self.use_current_mesh)
        
        base_mesh_group.setLayout(base_mesh_layout)
        layout.addWidget(base_mesh_group)
        
        # STL geometry
        stl_group = QGroupBox("STL Geometry")
        stl_layout = QHBoxLayout()
        
        self.stl_path = QLabel("No STL file selected")
        stl_layout.addWidget(self.stl_path, 1)
        
        self.browse_stl_btn = QPushButton("Browse...")
        self.browse_stl_btn.clicked.connect(self.browse_stl_file)
        stl_layout.addWidget(self.browse_stl_btn)
        
        stl_group.setLayout(stl_layout)
        layout.addWidget(stl_group)
        
        # Snappy parameters
        snappy_group = QGroupBox("SnappyHexMesh Parameters")
        snappy_layout = QFormLayout()
        
        self.castellated_mesh = QCheckBox("Castellated Mesh")
        self.castellated_mesh.setChecked(True)
        snappy_layout.addRow("", self.castellated_mesh)
        
        self.snap = QCheckBox("Snap")
        self.snap.setChecked(True)
        snappy_layout.addRow("", self.snap)
        
        self.add_layers = QCheckBox("Add Layers")
        self.add_layers.setChecked(True)
        snappy_layout.addRow("", self.add_layers)
        
        self.refinement_level = QSpinBox()
        self.refinement_level.setRange(0, 10)
        self.refinement_level.setValue(2)
        snappy_layout.addRow("Refinement Level:", self.refinement_level)
        
        self.num_layers = QSpinBox()
        self.num_layers.setRange(0, 20)
        self.num_layers.setValue(3)
        snappy_layout.addRow("Number of Layers:", self.num_layers)
        
        snappy_group.setLayout(snappy_layout)
        layout.addWidget(snappy_group)
        
        # Run snappyHexMesh button
        self.run_snappy_btn = QPushButton("Run SnappyHexMesh")
        self.run_snappy_btn.clicked.connect(self.run_snappy_hex_mesh)
        layout.addWidget(self.run_snappy_btn)
        
        layout.addStretch(1)
        
    def setup_quality_tab(self):
        """Setup the mesh quality check tab."""
        layout = QVBoxLayout(self.quality_tab)
        
        # Quality metrics selection
        metrics_group = QGroupBox("Quality Metrics")
        metrics_layout = QVBoxLayout()
        
        self.check_non_orthogonality = QCheckBox("Non-orthogonality")
        self.check_non_orthogonality.setChecked(True)
        metrics_layout.addWidget(self.check_non_orthogonality)
        
        self.check_skewness = QCheckBox("Skewness")
        self.check_skewness.setChecked(True)
        metrics_layout.addWidget(self.check_skewness)
        
        self.check_aspect_ratio = QCheckBox("Aspect Ratio")
        self.check_aspect_ratio.setChecked(True)
        metrics_layout.addWidget(self.check_aspect_ratio)
        
        self.check_volume_ratio = QCheckBox("Volume Ratio")
        self.check_volume_ratio.setChecked(True)
        metrics_layout.addWidget(self.check_volume_ratio)
        
        metrics_group.setLayout(metrics_layout)
        layout.addWidget(metrics_group)
        
        # Thresholds
        threshold_group = QGroupBox("Quality Thresholds")
        threshold_layout = QFormLayout()
        
        self.max_non_ortho = QDoubleSpinBox()
        self.max_non_ortho.setRange(0, 180)
        self.max_non_ortho.setValue(70)
        threshold_layout.addRow("Max Non-orthogonality:", self.max_non_ortho)
        
        self.max_skewness = QDoubleSpinBox()
        self.max_skewness.setRange(0, 10)
        self.max_skewness.setValue(4)
        threshold_layout.addRow("Max Skewness:", self.max_skewness)
        
        threshold_group.setLayout(threshold_layout)
        layout.addWidget(threshold_group)
        
        # Results table
        self.quality_results = QTableWidget(0, 3)
        self.quality_results.setHorizontalHeaderLabels(["Metric", "Max Value", "Status"])
        layout.addWidget(self.quality_results)
        
        # Check quality button
        self.check_quality_btn = QPushButton("Check Mesh Quality")
        self.check_quality_btn.clicked.connect(self.check_mesh_quality)
        layout.addWidget(self.check_quality_btn)
        
    def browse_mesh_file(self):
        """Open file dialog to browse for mesh files."""
        file_filter = "All Files (*);;OpenFOAM (*constant/polyMesh*);;STL Files (*.stl);;Fluent Mesh (*.msh);;CGNS Files (*.cgns)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Mesh File", "", file_filter)
        if file_path:
            self.file_path.setText(file_path)
            # Guess format based on extension
            if "polyMesh" in file_path:
                self.mesh_format.setCurrentText("OpenFOAM")
            elif file_path.lower().endswith(".stl"):
                self.mesh_format.setCurrentText("STL")
            elif file_path.lower().endswith(".msh"):
                self.mesh_format.setCurrentText("Fluent (.msh)")
            elif file_path.lower().endswith(".cgns"):
                self.mesh_format.setCurrentText("CGNS")
    
    def browse_stl_file(self):
        """Open file dialog to browse for STL files."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select STL File", "", "STL Files (*.stl)")
        if file_path:
            self.stl_path.setText(file_path)
    
    def update_mesh_options(self):
        """Update mesh parameters based on selected mesh type."""
        mesh_type = self.base_mesh_type.currentText()
        
        # Clear existing layout
        while self.mesh_params_layout.rowCount() > 0:
            self.mesh_params_layout.removeRow(0)
        
        # Add common parameters
        self.cell_count_x = QSpinBox()
        self.cell_count_x.setRange(1, 1000)
        self.cell_count_x.setValue(20)
        self.mesh_params_layout.addRow("Cells X:", self.cell_count_x)
        
        self.cell_count_y = QSpinBox()
        self.cell_count_y.setRange(1, 1000)
        self.cell_count_y.setValue(20)
        self.mesh_params_layout.addRow("Cells Y:", self.cell_count_y)
        
        self.cell_count_z = QSpinBox()
        self.cell_count_z.setRange(1, 1000)
        self.cell_count_z.setValue(20)
        self.mesh_params_layout.addRow("Cells Z:", self.cell_count_z)
        
        # Add type-specific parameters
        if mesh_type == "Block Mesh":
            self.mesh_grading = QDoubleSpinBox()
            self.mesh_grading.setRange(0.1, 10)
            self.mesh_grading.setValue(1.0)
            self.mesh_params_layout.addRow("Grading:", self.mesh_grading)
            
        elif mesh_type == "Tetrahedral Mesh":
            self.max_cell_size = QDoubleSpinBox()
            self.max_cell_size.setRange(0.001, 1000)
            self.max_cell_size.setValue(0.1)
            self.mesh_params_layout.addRow("Max Cell Size:", self.max_cell_size)
            
            self.min_quality = QDoubleSpinBox()
            self.min_quality.setRange(0, 1)
            self.min_quality.setValue(0.3)
            self.min_quality.setSingleStep(0.05)
            self.mesh_params_layout.addRow("Min Quality:", self.min_quality)
            
        elif mesh_type == "Polyhedral Mesh":
            self.base_cell_size = QDoubleSpinBox()
            self.base_cell_size.setRange(0.001, 1000)
            self.base_cell_size.setValue(0.1)
            self.mesh_params_layout.addRow("Base Cell Size:", self.base_cell_size)
    
    def import_mesh(self):
        """Import mesh from file."""
        file_path = self.file_path.text()
        if file_path == "No file selected":
            QMessageBox.warning(self, "Warning", "Please select a mesh file first.")
            return
            
        # This would normally call OpenFOAM tools to import the mesh
        # For now, we'll just update the UI to simulate success
        self.mesh_file = file_path
        self.mesh_type = self.mesh_format.currentText()
        
        # Update mesh information
        self.mesh_status.setText("Mesh loaded from file")
        self.cell_count.setText("125000")  # Simulated values
        self.face_count.setText("375000")
        self.boundary_count.setText("6")
        
        self.view_mesh_btn.setEnabled(True)
        
        QMessageBox.information(self, "Success", "Mesh imported successfully!")
        
    def generate_mesh(self):
        """Generate mesh based on parameters."""
        mesh_type = self.base_mesh_type.currentText()
        
        # This would normally call OpenFOAM tools to generate the mesh
        # For now, we'll just update the UI to simulate success
        
        # Calculate simulated cell count
        cell_count = self.cell_count_x.value() * self.cell_count_y.value() * self.cell_count_z.value()
        
        # Update mesh information
        self.mesh_file = f"Generated {mesh_type}"
        self.mesh_type = mesh_type
        self.mesh_status.setText(f"Generated {mesh_type}")
        self.cell_count.setText(str(cell_count))
        self.face_count.setText(str(cell_count * 3))  # Approximate
        self.boundary_count.setText("6")  # For box domains
        
        self.view_mesh_btn.setEnabled(True)
        
        QMessageBox.information(self, "Success", "Mesh generated successfully!")
        
    def run_snappy_hex_mesh(self):
        """Run snappyHexMesh on the base mesh."""
        if not self.use_current_mesh.isChecked() and (self.mesh_file is None):
            QMessageBox.warning(self, "Warning", "Please generate or import a base mesh first.")
            return
            
        stl_path = self.stl_path.text()
        if stl_path == "No STL file selected":
            QMessageBox.warning(self, "Warning", "Please select an STL file first.")
            return
            
        # This would normally call OpenFOAM's snappyHexMesh
        # For now, we'll just update the UI to simulate success
        
        # Update mesh information
        self.mesh_file = "SnappyHexMesh result"
        self.mesh_type = "SnappyHexMesh"
        self.mesh_status.setText("SnappyHexMesh completed")
        
        # Simulated values - would normally come from actual mesh
        if self.use_current_mesh.isChecked():
            current_cells = int(self.cell_count.text())
            new_cells = current_cells * (2 ** self.refinement_level.value()) // 2
        else:
            new_cells = 125000 * (2 ** self.refinement_level.value()) // 2
            
        self.cell_count.setText(str(new_cells))
        self.face_count.setText(str(new_cells * 4))  # Approximate for snappy
        self.boundary_count.setText("12")  # Typical for snappy with one STL
        
        self.view_mesh_btn.setEnabled(True)
        
        QMessageBox.information(self, "Success", "SnappyHexMesh completed successfully!")
        
    def check_mesh_quality(self):
        """Check the quality of the current mesh."""
        if self.mesh_file is None:
            QMessageBox.warning(self, "Warning", "Please generate or import a mesh first.")
            return
            
        # This would normally call OpenFOAM's checkMesh
        # For now, we'll simulate quality metrics
        
        # Clear previous results
        self.quality_results.setRowCount(0)
        
        # Add quality metrics (simulated values)
        metrics = []
        
        if self.check_non_orthogonality.isChecked():
            max_value = 48.2
            status = "OK" if max_value < self.max_non_ortho.value() else "Warning"
            metrics.append(["Non-orthogonality", f"{max_value:.1f}", status])
            
        if self.check_skewness.isChecked():
            max_value = 2.1
            status = "OK" if max_value < self.max_skewness.value() else "Warning"
            metrics.append(["Skewness", f"{max_value:.2f}", status])
            
        if self.check_aspect_ratio.isChecked():
            max_value = 6.4
            status = "OK" if max_value < 10 else "Warning"
            metrics.append(["Aspect Ratio", f"{max_value:.1f}", status])
            
        if self.check_volume_ratio.isChecked():
            max_value = 3.2
            status = "OK" if max_value < 8 else "Warning"
            metrics.append(["Volume Ratio", f"{max_value:.1f}", status])
            
        # Add rows to table
        self.quality_results.setRowCount(len(metrics))
        for i, (metric, value, status) in enumerate(metrics):
            self.quality_results.setItem(i, 0, QTableWidgetItem(metric))
            self.quality_results.setItem(i, 1, QTableWidgetItem(value))
            status_item = QTableWidgetItem(status)
            if status == "Warning":
                status_item.setBackground(Qt.yellow)
            elif status == "Error":
                status_item.setBackground(Qt.red)
            else:
                status_item.setBackground(Qt.green)
            self.quality_results.setItem(i, 2, status_item)
        
        self.quality_results.resizeColumnsToContents()
        
    def view_mesh(self):
        """View the current mesh in a 3D viewer."""
        if self.mesh_file is None:
            return
            
        # This would normally open ParaView or other viewer
        # For now, just show a message
        QMessageBox.information(self, "View Mesh", 
                               f"Opening mesh viewer for {self.mesh_file}.\n"
                               "This would normally launch ParaView or integrated viewer.")
        
    def apply_mesh(self):
        """Apply the current mesh to the simulation."""
        if self.mesh_file is None:
            QMessageBox.warning(self, "Warning", "Please generate or import a mesh first.")
            return
            
        # This would normally copy/link the mesh to the OpenFOAM case directory
        self.mesh_changed.emit()
        
        QMessageBox.information(self, "Success", "Mesh applied to simulation case.")
        
    def reset_mesh(self):
        """Reset the mesh settings."""
        self.mesh_file = None
        self.mesh_type = None
        
        # Reset UI elements
        self.mesh_status.setText("No mesh loaded")
        self.cell_count.setText("0")
        self.face_count.setText("0")
        self.boundary_count.setText("0")
        
        self.file_path.setText("No file selected")
        self.stl_path.setText("No STL file selected")
        
        self.view_mesh_btn.setEnabled(False)
        
        # Reset other parameters to defaults
        self.scale_factor.setValue(1.0)
        self.convert_to_meters.setChecked(True)
        self.clean_topology.setChecked(True)
        
        self.base_mesh_type.setCurrentIndex(0)
        self.update_mesh_options()
        
        self.use_current_mesh.setChecked(False)
        self.castellated_mesh.setChecked(True)
        self.snap.setChecked(True)
        self.add_layers.setChecked(True)
        self.refinement_level.setValue(2)
        self.num_layers.setValue(3)
        
        # Clear quality results
        self.quality_results.setRowCount(0)
