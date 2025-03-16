# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 15:14:52 2025

@author: adamp
"""
# src/modules/physics/physics_widget.py
from PyQt5.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QComboBox, QGroupBox, QPushButton, 
                            QFormLayout, QSpinBox, QDoubleSpinBox, QCheckBox)
from PyQt5.QtCore import pyqtSignal, Qt

class PhysicsWidget(QWidget):
    """Main widget for setting up physics for CFD simulation."""
    
    physics_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the physics configuration UI."""
        main_layout = QVBoxLayout(self)
        
        # Create tabs for different physics configuration sections
        self.tabs = QTabWidget()
        
        # General flow type configuration
        self.general_tab = QWidget()
        self.setup_general_tab()
        self.tabs.addTab(self.general_tab, "General")
        
        # Models tab - turbulence, energy, etc.
        self.models_tab = QWidget()
        self.setup_models_tab()
        self.tabs.addTab(self.models_tab, "Models")
        
        # Materials tab
        self.materials_tab = QWidget()
        self.setup_materials_tab()
        self.tabs.addTab(self.materials_tab, "Materials")
        
        # Boundary conditions tab
        self.bc_tab = QWidget()
        self.setup_bc_tab()
        self.tabs.addTab(self.bc_tab, "Boundary Conditions")
        
        # Solver settings tab
        self.solver_tab = QWidget()
        self.setup_solver_tab()
        self.tabs.addTab(self.solver_tab, "Solver Settings")
        
        main_layout.addWidget(self.tabs)
        
        # Add apply/reset buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)
        button_layout.addWidget(self.apply_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_settings)
        button_layout.addWidget(self.reset_button)
        
        main_layout.addLayout(button_layout)
        
    def setup_general_tab(self):
        """Setup the general flow configuration tab."""
        layout = QVBoxLayout(self.general_tab)
        
        # Flow type selection
        flow_group = QGroupBox("Flow Type")
        flow_layout = QFormLayout()
        
        self.flow_type = QComboBox()
        self.flow_type.addItems(["Incompressible", "Compressible", "Multiphase"])
        flow_layout.addRow("Flow Type:", self.flow_type)
        
        self.time_model = QComboBox()
        self.time_model.addItems(["Steady", "Transient"])
        flow_layout.addRow("Time Model:", self.time_model)
        
        flow_group.setLayout(flow_layout)
        layout.addWidget(flow_group)
        
        # Reference values
        ref_group = QGroupBox("Reference Values")
        ref_layout = QFormLayout()
        
        self.ref_pressure = QDoubleSpinBox()
        self.ref_pressure.setRange(0, 1000000)
        self.ref_pressure.setValue(101325)
        self.ref_pressure.setSuffix(" Pa")
        ref_layout.addRow("Reference Pressure:", self.ref_pressure)
        
        self.ref_temperature = QDoubleSpinBox()
        self.ref_temperature.setRange(0, 5000)
        self.ref_temperature.setValue(300)
        self.ref_temperature.setSuffix(" K")
        ref_layout.addRow("Reference Temperature:", self.ref_temperature)
        
        self.gravity = QCheckBox("Enable Gravity")
        ref_layout.addRow(self.gravity)
        
        ref_group.setLayout(ref_layout)
        layout.addWidget(ref_group)
        
        # Operating conditions
        op_group = QGroupBox("Operating Conditions")
        op_layout = QFormLayout()
        
        self.op_pressure = QDoubleSpinBox()
        self.op_pressure.setRange(0, 1000000)
        self.op_pressure.setValue(101325)
        self.op_pressure.setSuffix(" Pa")
        op_layout.addRow("Operating Pressure:", self.op_pressure)
        
        op_group.setLayout(op_layout)
        layout.addWidget(op_group)
        
        layout.addStretch(1)
        
    def setup_models_tab(self):
        """Setup the physical models tab."""
        layout = QVBoxLayout(self.models_tab)
        
        # Turbulence Model
        turb_group = QGroupBox("Turbulence Model")
        turb_layout = QFormLayout()
        
        self.turbulence_enabled = QCheckBox("Enable Turbulence")
        self.turbulence_enabled.setChecked(True)
        turb_layout.addRow(self.turbulence_enabled)
        
        self.turbulence_model = QComboBox()
        self.turbulence_model.addItems(["k-epsilon", "k-omega SST", "Spalart-Allmaras", "Reynolds Stress"])
        turb_layout.addRow("Model:", self.turbulence_model)
        
        self.wall_treatment = QComboBox()
        self.wall_treatment.addItems(["Standard Wall Functions", "Enhanced Wall Treatment"])
        turb_layout.addRow("Wall Treatment:", self.wall_treatment)
        
        turb_group.setLayout(turb_layout)
        layout.addWidget(turb_group)
        
        # Energy Equation
        energy_group = QGroupBox("Energy Equation")
        energy_layout = QFormLayout()
        
        self.energy_enabled = QCheckBox("Enable Energy Equation")
        energy_layout.addRow(self.energy_enabled)
        
        energy_group.setLayout(energy_layout)
        layout.addWidget(energy_group)
        
        layout.addStretch(1)
        
    def setup_materials_tab(self):
        """Setup the materials tab."""
        layout = QVBoxLayout(self.materials_tab)
        
        # Add some basic controls for material properties
        materials_group = QGroupBox("Fluid Materials")
        materials_layout = QFormLayout()
        
        self.fluid_material = QComboBox()
        self.fluid_material.addItems(["Air", "Water", "Custom"])
        materials_layout.addRow("Material:", self.fluid_material)
        
        # Properties
        self.density = QDoubleSpinBox()
        self.density.setRange(0.1, 10000)
        self.density.setValue(1.225)
        self.density.setSuffix(" kg/m³")
        materials_layout.addRow("Density:", self.density)
        
        self.viscosity = QDoubleSpinBox()
        self.viscosity.setRange(1e-6, 1000)
        self.viscosity.setValue(1.7894e-5)
        self.viscosity.setSuffix(" kg/m·s")
        self.viscosity.setDecimals(6)
        materials_layout.addRow("Viscosity:", self.viscosity)
        
        materials_group.setLayout(materials_layout)
        layout.addWidget(materials_group)
        
        layout.addStretch(1)
        
    def setup_bc_tab(self):
        """Setup the boundary conditions tab."""
        layout = QVBoxLayout(self.bc_tab)
        
        # This would typically be populated with the boundaries from the mesh
        # For now, just add a placeholder
        bc_group = QGroupBox("Boundary Conditions")
        bc_layout = QVBoxLayout()
        
        bc_label = QLabel("Boundary conditions will be loaded after mesh import.")
        bc_layout.addWidget(bc_label)
        
        bc_group.setLayout(bc_layout)
        layout.addWidget(bc_group)
        
        layout.addStretch(1)
        
    def setup_solver_tab(self):
        """Setup the solver settings tab."""
        layout = QVBoxLayout(self.solver_tab)
        
        # Solver settings
        solver_group = QGroupBox("Solver Settings")
        solver_layout = QFormLayout()
        
        self.solver_type = QComboBox()
        self.solver_type.addItems(["SIMPLE", "PISO", "PIMPLE"])
        solver_layout.addRow("Algorithm:", self.solver_type)
        
        self.max_iterations = QSpinBox()
        self.max_iterations.setRange(1, 10000)
        self.max_iterations.setValue(1000)
        solver_layout.addRow("Max Iterations:", self.max_iterations)
        
        self.convergence_criteria = QDoubleSpinBox()
        self.convergence_criteria.setRange(1e-12, 1)
        self.convergence_criteria.setValue(1e-4)
        self.convergence_criteria.setDecimals(10)
        solver_layout.addRow("Convergence Criteria:", self.convergence_criteria)
        
        solver_group.setLayout(solver_layout)
        layout.addWidget(solver_group)
        
        # Discretization schemes
        scheme_group = QGroupBox("Discretization Schemes")
        scheme_layout = QFormLayout()
        
        self.gradient_scheme = QComboBox()
        self.gradient_scheme.addItems(["Gauss Linear", "Least Squares", "Gauss Node"])
        scheme_layout.addRow("Gradient:", self.gradient_scheme)
        
        self.divergence_scheme = QComboBox()
        self.divergence_scheme.addItems(["upwind", "linearUpwind", "QUICK", "TVD", "MUSCL"])
        scheme_layout.addRow("Divergence:", self.divergence_scheme)
        
        scheme_group.setLayout(scheme_layout)
        layout.addWidget(scheme_group)
        
        layout.addStretch(1)
        
    def apply_settings(self):
        """Apply the physics settings to the simulation."""
        # This would normally gather all settings and update the simulation
        self.physics_changed.emit()
        
    def reset_settings(self):
        """Reset all physics settings to defaults."""
        # Reset all widgets to default values
        self.flow_type.setCurrentIndex(0)
        self.time_model.setCurrentIndex(0)
        self.ref_pressure.setValue(101325)
        self.ref_temperature.setValue(300)
        self.gravity.setChecked(False)
        self.op_pressure.setValue(101325)
        self.turbulence_enabled.setChecked(True)
        self.turbulence_model.setCurrentIndex(0)
        self.wall_treatment.setCurrentIndex(0)
        self.energy_enabled.setChecked(False)
        self.fluid_material.setCurrentIndex(0)
        self.density.setValue(1.225)
        self.viscosity.setValue(1.7894e-5)
        self.solver_type.setCurrentIndex(0)
        self.max_iterations.setValue(1000)
        self.convergence_criteria.setValue(1e-4)
        self.gradient_scheme.setCurrentIndex(0)
        self.divergence_scheme.setCurrentIndex(0)
        
        self.physics_changed.emit()
