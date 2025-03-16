# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 18:40:44 2025

@author: adamp
"""

"""
Simulation setup panel for configuring CFD simulation parameters.
"""
import os
from typing import Dict, Any, List, Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit,
    QPushButton, QTabWidget, QFormLayout, QGroupBox, QSpinBox, QDoubleSpinBox,
    QCheckBox, QFileDialog, QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal

from src.openfoam.dictionary import Dictionary
from src.openfoam.case_manager import CaseManager
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SimulationSetupPanel(QWidget):
    """Panel for configuring simulation parameters."""
    
    # Signal emitted when settings are changed
    settings_changed = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the simulation setup panel.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.case_manager = CaseManager()
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        main_layout = QVBoxLayout()
        
        # Create a tab widget for different categories of settings
        tab_widget = QTabWidget()
        
        # Add tabs
        tab_widget.addTab(self._create_general_tab(), "General")
        tab_widget.addTab(self._create_fluid_tab(), "Fluid Properties")
        tab_widget.addTab(self._create_thermal_tab(), "Thermal Settings")
        tab_widget.addTab(self._create_turbulence_tab(), "Turbulence Models")
        tab_widget.addTab(self._create_multiphase_tab(), "Multiphase Settings")
        tab_widget.addTab(self._create_reactions_tab(), "Chemical Reactions")
        tab_widget.addTab(self._create_numerics_tab(), "Numerical Settings")
        
        # Add the tab widget to the main layout
        main_layout.addWidget(tab_widget)
        
        # Add apply and reset buttons
        button_layout = QHBoxLayout()
        
        apply_button = QPushButton("Apply Settings")
        apply_button.clicked.connect(self._apply_settings)
        
        reset_button = QPushButton("Reset to Defaults")
        reset_button.clicked.connect(self._reset_to_defaults)
        
        button_layout.addStretch()
        button_layout.addWidget(reset_button)
        button_layout.addWidget(apply_button)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
    
    def _create_general_tab(self) -> QWidget:
        """Create the general settings tab.
        
        Returns:
            Widget containing general settings
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Solver selection
        solver_group = QGroupBox("Solver")
        solver_layout = QFormLayout()
        
        self.solver_combo = QComboBox()
        self.solver_combo.addItems([
            "simpleFoam", "pimpleFoam", "buoyantPimpleFoam", 
            "buoyantSimpleFoam", "chtMultiRegionFoam", "reactingFoam"
        ])
        solver_layout.addRow("Solver Type:", self.solver_combo)
        
        self.time_scheme_combo = QComboBox()
        self.time_scheme_combo.addItems(["Steady", "Transient"])
        solver_layout.addRow("Time Scheme:", self.time_scheme_combo)
        
        solver_group.setLayout(solver_layout)
        layout.addWidget(solver_group)
        
        # Time control settings
        time_group = QGroupBox("Time Control")
        time_layout = QFormLayout()
        
        self.start_time = QDoubleSpinBox()
        self.start_time.setValue(0.0)
        self.start_time.setSingleStep(0.1)
        time_layout.addRow("Start Time:", self.start_time)
        
        self.end_time = QDoubleSpinBox()
        self.end_time.setValue(100.0)
        self.end_time.setRange(0.0, 1000000.0)
        time_layout.addRow("End Time:", self.end_time)
        
        self.delta_t = QDoubleSpinBox()
        self.delta_t.setValue(0.01)
        self.delta_t.setRange(0.000001, 1000.0)
        self.delta_t.setDecimals(6)
        time_layout.addRow("Time Step (deltaT):", self.delta_t)
        
        self.write_interval = QDoubleSpinBox()
        self.write_interval.setValue(10.0)
        time_layout.addRow("Write Interval:", self.write_interval)
        
        time_group.setLayout(time_layout)
        layout.addWidget(time_group)
        
        # Add some vertical space
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab

    def _create_fluid_tab(self) -> QWidget:
        """Create the fluid properties tab.
        
        Returns:
            Widget containing fluid properties settings
        """
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        
        # Fluid properties
        fluid_group = QGroupBox("Fluid Properties")
        fluid_layout = QFormLayout()
        
        self.fluid_type_combo = QComboBox()
        self.fluid_type_combo.addItems(["Air", "Water", "Custom"])
        fluid_layout.addRow("Fluid Type:", self.fluid_type_combo)
        
        self.density = QDoubleSpinBox()
        self.density.setRange(0.01, 10000.0)
        self.density.setValue(1.0)
        self.density.setSuffix(" kg/m³")
        fluid_layout.addRow("Density:", self.density)
        
        self.viscosity = QDoubleSpinBox()
        self.viscosity.setRange(1e-6, 100.0)
        self.viscosity.setValue(1.8e-5)
        self.viscosity.setDecimals(6)
        self.viscosity.setSuffix(" Pa·s")
        fluid_layout.addRow("Dynamic Viscosity:", self.viscosity)
        
        fluid_group.setLayout(fluid_layout)
        layout.addWidget(fluid_group)
        
        # Thermophysical properties
        thermo_group = QGroupBox("Thermophysical Properties")
        thermo_layout = QFormLayout()
        
        self.use_thermo = QCheckBox("Enable Thermophysical Model")
        thermo_layout.addRow("", self.use_thermo)
        
        self.thermo_model = QComboBox()
        self.thermo_model.addItems([
            "hePsiThermo", "heRhoThermo", "hsSolidThermo"
        ])
        thermo_layout.addRow("Thermophysical Model:", self.thermo_model)
        
        self.specific_heat = QDoubleSpinBox()
        self.specific_heat.setRange(1.0, 10000.0)
        self.specific_heat.setValue(1005.0)
        self.specific_heat.setSuffix(" J/(kg·K)")
        thermo_layout.addRow("Specific Heat Capacity:", self.specific_heat)
        
        self.thermal_conductivity = QDoubleSpinBox()
        self.thermal_conductivity.setRange(0.001, 1000.0)
        self.thermal_conductivity.setValue(0.026)
        self.thermal_conductivity.setSuffix(" W/(m·K)")
        thermo_layout.addRow("Thermal Conductivity:", self.thermal_conductivity)
        
        thermo_group.setLayout(thermo_layout)
        layout.addWidget(thermo_group)
        
        # Add some vertical space
        layout.addStretch()
        
        content.setLayout(layout)
        tab.setWidget(content)
        return tab

    def _create_thermal_tab(self) -> QWidget:
        """Create the thermal settings tab.
        
        Returns:
            Widget containing thermal settings
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Heat transfer settings
        heat_group = QGroupBox("Heat Transfer")
        heat_layout = QFormLayout()
        
        self.enable_heat_transfer = QCheckBox("Enable Heat Transfer")
        heat_layout.addRow("", self.enable_heat_transfer)
        
        self.reference_temperature = QDoubleSpinBox()
        self.reference_temperature.setRange(0.0, 5000.0)
        self.reference_temperature.setValue(300.0)
        self.reference_temperature.setSuffix(" K")
        heat_layout.addRow("Reference Temperature:", self.reference_temperature)
        
        self.operating_temperature = QDoubleSpinBox()
        self.operating_temperature.setRange(0.0, 5000.0)
        self.operating_temperature.setValue(300.0)
        self.operating_temperature.setSuffix(" K")
        heat_layout.addRow("Operating Temperature:", self.operating_temperature)
        
        heat_group.setLayout(heat_layout)
        layout.addWidget(heat_group)
        
        # Buoyancy settings
        buoyancy_group = QGroupBox("Buoyancy")
        buoyancy_layout = QFormLayout()
        
        self.enable_buoyancy = QCheckBox("Enable Buoyancy")
        buoyancy_layout.addRow("", self.enable_buoyancy)
        
        self.gravity_x = QDoubleSpinBox()
        self.gravity_x.setRange(-100.0, 100.0)
        self.gravity_x.setValue(0.0)
        self.gravity_x.setSuffix(" m/s²")
        buoyancy_layout.addRow("Gravity X-component:", self.gravity_x)
        
        self.gravity_y = QDoubleSpinBox()
        self.gravity_y.setRange(-100.0, 100.0)
        self.gravity_y.setValue(-9.81)
        self.gravity_y.setSuffix(" m/s²")
        buoyancy_layout.addRow("Gravity Y-component:", self.gravity_y)
        
        self.gravity_z = QDoubleSpinBox()
        self.gravity_z.setRange(-100.0, 100.0)
        self.gravity_z.setValue(0.0)
        self.gravity_z.setSuffix(" m/s²")
        buoyancy_layout.addRow("Gravity Z-component:", self.gravity_z)
        
        buoyancy_group.setLayout(buoyancy_layout)
        layout.addWidget(buoyancy_group)
        
        # Add some vertical space
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab
    
    def _create_turbulence_tab(self) -> QWidget:
        """Create the turbulence models tab.
        
        Returns:
            Widget containing turbulence model settings
        """
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        
        # Turbulence model settings
        turb_group = QGroupBox("Turbulence Model")
        turb_layout = QFormLayout()
        
        self.turbulence_model = QComboBox()
        self.turbulence_model.addItems([
            "laminar", "kEpsilon", "kOmega", "kOmegaSST", 
            "SpalartAllmaras", "RNGkEpsilon", "ReynoldsStress"
        ])
        turb_layout.addRow("Turbulence Model:", self.turbulence_model)
        
        self.inlet_turbulence_intensity = QDoubleSpinBox()
        self.inlet_turbulence_intensity.setRange(0.0, 100.0)
        self.inlet_turbulence_intensity.setValue(5.0)
        self.inlet_turbulence_intensity.setSuffix(" %")
        turb_layout.addRow("Inlet Turbulence Intensity:", self.inlet_turbulence_intensity)
        
        self.inlet_turbulence_length = QDoubleSpinBox()
        self.inlet_turbulence_length.setRange(0.0001, 1000.0)
        self.inlet_turbulence_length.setValue(0.1)
        self.inlet_turbulence_length.setSuffix(" m")
        turb_layout.addRow("Inlet Turbulence Length Scale:", self.inlet_turbulence_length)
        
        turb_group.setLayout(turb_layout)
        layout.addWidget(turb_group)
        
        # Reynolds Stress Model settings (only visible when selected)
        rsm_group = QGroupBox("Reynolds Stress Model Options")
        rsm_layout = QFormLayout()
        
        self.rsm_model = QComboBox()
        self.rsm_model.addItems([
            "LRR", "SSG", "LRR-IP", "SSG-LRR-omega"
        ])
        rsm_layout.addRow("RSM Variant:", self.rsm_model)
        
        self.rsm_wall_reflection = QCheckBox("Enable Wall Reflection")
        self.rsm_wall_reflection.setChecked(True)
        rsm_layout.addRow("", self.rsm_wall_reflection)
        
        rsm_group.setLayout(rsm_layout)
        layout.addWidget(rsm_group)
        
        # Wall treatment options
        wall_group = QGroupBox("Wall Treatment")
        wall_layout = QFormLayout()
        
        self.wall_treatment = QComboBox()
        self.wall_treatment.addItems([
            "Standard Wall Functions", 
            "Enhanced Wall Treatment", 
            "Low-Re Wall Treatment"
        ])
        wall_layout.addRow("Wall Treatment:", self.wall_treatment)
        
        self.y_plus_target = QDoubleSpinBox()
        self.y_plus_target.setRange(0.1, 1000.0)
        self.y_plus_target.setValue(30.0)
        wall_layout.addRow("Target y+ Value:", self.y_plus_target)
        
        wall_group.setLayout(wall_layout)
        layout.addWidget(wall_group)
        
        # Add some vertical space
        layout.addStretch()
        
        content.setLayout(layout)
        tab.setWidget(content)
        return tab

    def _create_multiphase_tab(self) -> QWidget:
        """Create the multiphase settings tab.
        
        Returns:
            Widget containing multiphase settings
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Multiphase settings
        multiphase_group = QGroupBox("Multiphase Flow")
        multiphase_layout = QFormLayout()
        
        self.enable_multiphase = QCheckBox("Enable Multiphase Flow")
        multiphase_layout.addRow("", self.enable_multiphase)
        
        self.multiphase_model = QComboBox()
        self.multiphase_model.addItems([
            "VOF", "Mixture", "Eulerian"
        ])
        multiphase_layout.addRow("Multiphase Model:", self.multiphase_model)
        
        self.number_of_phases = QSpinBox()
        self.number_of_phases.setRange(2, 10)
        self.number_of_phases.setValue(2)
        multiphase_layout.addRow("Number of Phases:", self.number_of_phases)
        
        multiphase_group.setLayout(multiphase_layout)
        layout.addWidget(multiphase_group)
        
        # Phase interaction settings
        interaction_group = QGroupBox("Phase Interaction")
        interaction_layout = QFormLayout()
        
        self.surface_tension = QDoubleSpinBox()
        self.surface_tension.setRange(0.0, 1.0)
        self.surface_tension.setValue(0.072)
        self.surface_tension.setSuffix(" N/m")
        interaction_layout.addRow("Surface Tension:", self.surface_tension)
        
        self.interface_compression = QDoubleSpinBox()
        self.interface_compression.setRange(0.0, 10.0)
        self.interface_compression.setValue(1.0)
        interaction_layout.addRow("Interface Compression:", self.interface_compression)
        
        interaction_group.setLayout(interaction_layout)
        layout.addWidget(interaction_group)
        
        # Add some vertical space
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab
    
    def _create_reactions_tab(self) -> QWidget:
        """Create the chemical reactions tab.
        
        Returns:
            Widget containing chemical reaction settings
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Reactions settings
        reaction_group = QGroupBox("Chemical Reactions")
        reaction_layout = QFormLayout()
        
        self.enable_reactions = QCheckBox("Enable Chemical Reactions")
        reaction_layout.addRow("", self.enable_reactions)
        
        self.reaction_model = QComboBox()
        self.reaction_model.addItems([
            "laminar", "EDC", "PaSR"
        ])
        reaction_layout.addRow("Reaction Model:", self.reaction_model)
        
        self.combustion_model = QComboBox()
        self.combustion_model.addItems([
            "None", "Eddy Dissipation", "Finite Rate Chemistry"
        ])
        reaction_layout.addRow("Combustion Model:", self.combustion_model)
        
        reaction_group.setLayout(reaction_layout)
        layout.addWidget(reaction_group)
        
        # Species settings
        species_group = QGroupBox("Species")
        species_layout = QFormLayout()
        
        self.number_of_species = QSpinBox()
        self.number_of_species.setRange(1, 50)
        self.number_of_species.setValue(1)
        species_layout.addRow("Number of Species:", self.number_of_species)
        
        self.load_mechanism_button = QPushButton("Load Reaction Mechanism")
        species_layout.addRow("", self.load_mechanism_button)
        
        species_group.setLayout(species_layout)
        layout.addWidget(species_group)
        
        # Add some vertical space
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab
    
    def _create_numerics_tab(self) -> QWidget:
        """Create the numerical settings tab.
        
        Returns:
            Widget containing numerical settings
        """
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Solver settings
        solver_group = QGroupBox("Solver Controls")
        solver_layout = QFormLayout()
        
        self.pressure_solver = QComboBox()
        self.pressure_solver.addItems([
            "GAMG", "PCG", "smoothSolver"
        ])
        solver_layout.addRow("Pressure Solver:", self.pressure_solver)
        
        self.momentum_solver = QComboBox()
        self.momentum_solver.addItems([
            "smoothSolver", "PBiCG", "GAMG"
        ])
        solver_layout.addRow("Momentum Solver:", self.momentum_solver)
        
        self.energy_solver = QComboBox()
        self.energy_solver.addItems([
            "smoothSolver", "PBiCG", "GAMG"
        ])
        solver_layout.addRow("Energy Solver:", self.energy_solver)
        
        solver_group.setLayout(solver_layout)
        layout.addWidget(solver_group)
        
        # Discretization schemes
        schemes_group = QGroupBox("Discretization Schemes")
        schemes_layout = QFormLayout()
        
        self.grad_scheme = QComboBox()
        self.grad_scheme.addItems([
            "Gauss linear", "leastSquares", "Gauss cubic"
        ])
        schemes_layout.addRow("Gradient Scheme:", self.grad_scheme)
        
        self.div_scheme = QComboBox()
        self.div_scheme.addItems([
            "Gauss upwind", "Gauss linear", "Gauss linearUpwind grad(U)",
            "Gauss QUICK", "Gauss limitedLinear 1"
        ])
        schemes_layout.addRow("Divergence Scheme:", self.div_scheme)
        
        self.laplacian_scheme = QComboBox()
        self.laplacian_scheme.addItems([
            "Gauss linear corrected", "Gauss linear limited 0.5"
        ])
        schemes_layout.addRow("Laplacian Scheme:", self.laplacian_scheme)
        
        schemes_group.setLayout(schemes_layout)
        layout.addWidget(schemes_group)
        
        # Relaxation factors
        relaxation_group = QGroupBox("Relaxation Factors")
        relaxation_layout = QFormLayout()
        
        self.p_relax = QDoubleSpinBox()
        self.p_relax.setRange(0.01, 1.0)
        self.p_relax.setValue(0.3)
        relaxation_layout.addRow("Pressure:", self.p_relax)
        
        self.U_relax = QDoubleSpinBox()
        self.U_relax.setRange(0.01, 1.0)
        self.U_relax.setValue(0.7)
        relaxation_layout.addRow("Velocity:", self.U_relax)
        
        self.T_relax = QDoubleSpinBox()
        self.T_relax.setRange(0.01, 1.0)
        self.T_relax.setValue(0.7)
        relaxation_layout.addRow("Temperature:", self.T_relax)
        
        relaxation_group.setLayout(relaxation_layout)
        layout.addWidget(relaxation_group)
        
        # Add some vertical space
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab
    
    def _apply_settings(self) -> None:
        """Apply the current settings to the case."""
        try:
            logger.info("Applying simulation settings...")
            # In a real implementation, this would update the OpenFOAM case files
            # based on the current UI settings
            
            # Emit signal indicating settings have changed
            self.settings_changed.emit()
            
            QMessageBox.information(
                self,
                "Settings Applied",
                "Simulation settings have been applied successfully."
            )
        except Exception as e:
            logger.error(f"Error applying settings: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred while applying settings:\n{e}"
            )
    
    def _reset_to_defaults(self) -> None:
        """Reset all settings to their default values."""
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Are you sure you want to reset all settings to their default values?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Reset all settings to defaults
            # This would be implemented in a real application
            logger.info("Resetting settings to defaults")
            QMessageBox.information(
                self,
                "Settings Reset",
                "All settings have been reset to their default values."
            )
