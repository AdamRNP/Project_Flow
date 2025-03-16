# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 18:41:13 2025

@author: adamp
"""

"""
Boundary conditions panel for configuring CFD simulation boundary conditions.
"""
from typing import Dict, List, Optional, Any

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QTabWidget, QLabel, QLineEdit, QComboBox,
    QDoubleSpinBox, QFormLayout, QGroupBox, QCheckBox, QMessageBox,
    QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal

from src.openfoam.dictionary import Dictionary
from src.utils.logger import get_logger

logger = get_logger(__name__)

class BoundaryConditionsPanel(QWidget):
    """Panel for configuring boundary conditions."""
    
    # Signal emitted when boundary conditions are changed
    conditions_changed = pyqtSignal()
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the boundary conditions panel.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Dictionary to store boundary conditions
        self.boundaries: Dict[str, Dict[str, Any]] = {}
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        main_layout = QHBoxLayout()
        
        # Create boundary list widget
        self.boundary_tree = QTreeWidget()
        self.boundary_tree.setHeaderLabels(["Boundary", "Type"])
        self.boundary_tree.setMinimumWidth(200)
        self.boundary_tree.currentItemChanged.connect(self._on_boundary_selected)
        
        # Create boundary editor
        self.editor_widget = QTabWidget()
        
        # Create buttons for boundary management
        button_layout = QVBoxLayout()
        
        add_button = QPushButton("Add")
        add_button.clicked.connect(self._on_add_boundary)
        
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self._on_delete_boundary)
        
        rename_button = QPushButton("Rename")
        rename_button.clicked.connect(self._on_rename_boundary)
        
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(rename_button)
        button_layout.addStretch()
        
        # Create an apply button
        apply_button = QPushButton("Apply Changes")
        apply_button.clicked.connect(self._on_apply_changes)
        button_layout.addWidget(apply_button)
        
        # Add widgets to main layout
        list_layout = QVBoxLayout()
        list_layout.addWidget(QLabel("Boundaries:"))
        list_layout.addWidget(self.boundary_tree)
        
        panel_layout = QVBoxLayout()
        panel_layout.addWidget(self.editor_widget)
        
        main_layout.addLayout(list_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(panel_layout, 1)
        
        self.setLayout(main_layout)
        
        # Create editor tabs
        self._create_editor_tabs()
    
    def _create_editor_tabs(self) -> None:
        """Create the tabs for the boundary condition editor."""
        # Velocity tab
        self.velocity_tab = QScrollArea()
        self.velocity_tab.setWidgetResizable(True)
        velocity_widget = QWidget()
        velocity_layout = QVBoxLayout()
        
        # Velocity settings
        velocity_group = QGroupBox("Velocity")
        v_layout = QFormLayout()
        
        self.velocity_type = QComboBox()
        self.velocity_type.addItems([
            "fixedValue", "zeroGradient", "noSlip", "slip", 
            "inletOutlet", "outletInlet", "pressureInletOutletVelocity"
        ])
        v_layout.addRow("Type:", self.velocity_type)
        
        self.velocity_x = QDoubleSpinBox()
        self.velocity_x.setRange(-1000, 1000)
        self.velocity_x.setValue(0)
        v_layout.addRow("X-component:", self.velocity_x)
        
        self.velocity_y = QDoubleSpinBox()
        self.velocity_y.setRange(-1000, 1000)
        self.velocity_y.setValue(0)
        v_layout.addRow("Y-component:", self.velocity_y)
        
        self.velocity_z = QDoubleSpinBox()
        self.velocity_z.setRange(-1000, 1000)
        self.velocity_z.setValue(0)
        v_layout.addRow("Z-component:", self.velocity_z)
        
        velocity_group.setLayout(v_layout)
        velocity_layout.addWidget(velocity_group)
        velocity_layout.addStretch()
        
        velocity_widget.setLayout(velocity_layout)
        self.velocity_tab.setWidget(velocity_widget)
        self.editor_widget.addTab(self.velocity_tab, "Velocity")
        
        # Pressure tab
        self.pressure_tab = QScrollArea()
        self.pressure_tab.setWidgetResizable(True)
        pressure_widget = QWidget()
        pressure_layout = QVBoxLayout()
        
        # Pressure settings
        pressure_group = QGroupBox("Pressure")
        p_layout = QFormLayout()
        
        self.pressure_type = QComboBox()
        self.pressure_type.addItems([
            "fixedValue", "zeroGradient", "totalPressure", 
            "prghPressure", "fixedFluxPressure"
        ])
        p_layout.addRow("Type:", self.pressure_type)
        
        self.pressure_value = QDoubleSpinBox()
        self.pressure_value.setRange(-100000, 1000000)
        self.pressure_value.setValue(0)
        self.pressure_value.setSuffix(" Pa")
        p_layout.addRow("Value:", self.pressure_value)
        
        pressure_group.setLayout(p_layout)
        pressure_layout.addWidget(pressure_group)
        pressure_layout.addStretch()
        
        pressure_widget.setLayout(pressure_layout)
        self.pressure_tab.setWidget(pressure_widget)
        self.editor_widget.addTab(self.pressure_tab, "Pressure")
        
        # Temperature tab
        self.temperature_tab = QScrollArea()
        self.temperature_tab.setWidgetResizable(True)
        temperature_widget = QWidget()
        temperature_layout = QVBoxLayout()
        
        # Temperature settings
        temperature_group = QGroupBox("Temperature")
        t_layout = QFormLayout()
        
        self.temperature_type = QComboBox()
        self.temperature_type.addItems([
            "fixedValue", "zeroGradient", "inletOutlet", 
            "outletInlet", "fixedGradient", "coupled"
        ])
        t_layout.addRow("Type:", self.temperature_type)
        
        self.temperature_value = QDoubleSpinBox()
        self.temperature_value.setRange(0, 5000)
        self.temperature_value.setValue(300)
        self.temperature_value.setSuffix(" K")
        t_layout.addRow("Value:", self.temperature_value)
        
        temperature_group.setLayout(t_layout)
        temperature_layout.addWidget(temperature_group)
        temperature_layout.addStretch()
        
        temperature_widget.setLayout(temperature_layout)
        self.temperature_tab.setWidget(temperature_widget)
        self.editor_widget.addTab(self.temperature_tab, "Temperature")
        
        # Turbulence tab
        self.turbulence_tab = QScrollArea()
        self.turbulence_tab.setWidgetResizable(True)
        turbulence_widget = QWidget()
        turbulence_layout = QVBoxLayout()
        
        # k settings
        k_group = QGroupBox("Turbulent Kinetic Energy (k)")
        k_layout = QFormLayout()
        
        self.k_type = QComboBox()
        self.k_type.addItems([
            "fixedValue", "zeroGradient", "inletOutlet", 
            "outletInlet", "calculated"
        ])
        k_layout.addRow("Type:", self.k_type)
        
        self.k_value = QDoubleSpinBox()
        self.k_value.setRange(0, 1000)
        self.k_value.setValue(0.1)
        self.k_value.setSingleStep(0.01)
        k_layout.addRow("Value:", self.k_value)
        
        k_group.setLayout(k_layout)
        turbulence_layout.addWidget(k_group)
        
        # epsilon/omega settings
        dissipation_group = QGroupBox("Turbulent Dissipation (ε/ω)")
        dissipation_layout = QFormLayout()
        
        self.dissipation_type = QComboBox()
        self.dissipation_type.addItems([
            "fixedValue", "zeroGradient", "inletOutlet", 
            "outletInlet", "calculated"
        ])
        dissipation_layout.addRow("Type:", self.dissipation_type)
        
        self.dissipation_value = QDoubleSpinBox()
        self.dissipation_value.setRange(0, 1000)
        self.dissipation_value.setValue(0.1)
        self.dissipation_value.setSingleStep(0.01)
        dissipation_layout.addRow("Value:", self.dissipation_value)
        
        dissipation_group.setLayout(dissipation_layout)
        turbulence_layout.addWidget(dissipation_group)
        
        # Turbulent viscosity
        nut_group = QGroupBox("Turbulent Viscosity (νt)")
        nut_layout = QFormLayout()
        
        self.nut_type = QComboBox()
        self.nut_type.addItems([
            "calculated", "fixedValue", "zeroGradient", 
            "kqRWallFunction", "nutkWallFunction"
        ])
        nut_layout.addRow("Type:", self.nut_type)
        
        self.nut_value = QDoubleSpinBox()
        self.nut_value.setRange(0, 1000)
        self.nut_value.setValue(0)
        nut_layout.addRow("Value:", self.nut_value)
        
        nut_group.setLayout(nut_layout)
        turbulence_layout.addWidget(nut_group)
        turbulence_layout.addStretch()
        
        turbulence_widget.setLayout(turbulence_layout)
        self.turbulence_tab.setWidget(turbulence_widget)
        self.editor_widget.addTab(self.turbulence_tab, "Turbulence")
        
        # Wall functions tab
        self.wall_tab = QScrollArea()
        self.wall_tab.setWidgetResizable(True)
        wall_widget = QWidget()
        wall_layout = QVBoxLayout()
        
        # Wall functions
        wall_group = QGroupBox("Wall Treatment")
        wall_form_layout = QFormLayout()
        
        self.wall_function_type = QComboBox()
        self.wall_function_type.addItems([
            "Standard Wall Functions", 
            "Enhanced Wall Treatment",
            "Low-Re Treatment"
        ])
        wall_form_layout.addRow("Wall Treatment:", self.wall_function_type)
        
        self.y_plus_target = QDoubleSpinBox()
        self.y_plus_target.setRange(0.1, 1000)
        self.y_plus_target.setValue(30)
        wall_form_layout.addRow("Target y+ value:", self.y_plus_target)
        
        self.wall_roughness = QCheckBox("Enable Surface Roughness")
        wall_form_layout.addRow(self.wall_roughness)
        
        self.roughness_height = QDoubleSpinBox()
        self.roughness_height.setRange(0, 1)
        self.roughness_height.setValue(0)
        self.roughness_height.setSingleStep(0.001)
        self.roughness_height.setSuffix(" m")
        wall_form_layout.addRow("Roughness Height:", self.roughness_height)
        
        self.roughness_constant = QDoubleSpinBox()
        self.roughness_constant.setRange(0, 10)
        self.roughness_constant.setValue(0.5)
        self.roughness_constant.setSingleStep(0.1)
        wall_form_layout.addRow("Roughness Constant:", self.roughness_constant)
        
        wall_group.setLayout(wall_form_layout)
        wall_layout.addWidget(wall_group)
        wall_layout.addStretch()
        
        wall_widget.setLayout(wall_layout)
        self.wall_tab.setWidget(wall_widget)
        self.editor_widget.addTab(self.wall_tab, "Wall Functions")
        
        # Species tab
        self.species_tab = QScrollArea()
        self.species_tab.setWidgetResizable(True)
        species_widget = QWidget()
        species_layout = QVBoxLayout()
        
        # Species settings
        species_group = QGroupBox("Species Settings")
        species_form_layout = QFormLayout()
        
        self.species_type = QComboBox()
        self.species_type.addItems([
            "fixedValue", "zeroGradient", "inletOutlet",
            "outletInlet", "calculated"
        ])
        species_form_layout.addRow("Type:", self.species_type)
        
        species_group.setLayout(species_form_layout)
        species_layout.addWidget(species_group)
        species_layout.addStretch()
        
        species_widget.setLayout(species_layout)
        self.species_tab.setWidget(species_widget)
        self.editor_widget.addTab(self.species_tab, "Species")
    
    def _on_boundary_selected(self) -> None:
        """Handle selection of a boundary in the tree view."""
        selected_items = self.boundary_tree.selectedItems()
        if not selected_items:
            self.editor_widget.setEnabled(False)
            return
        
        self.editor_widget.setEnabled(True)
        boundary_name = selected_items[0].text(0)
        
        # Load boundary condition data for the selected boundary
        self._load_boundary_data(boundary_name)
    
    def _load_boundary_data(self, boundary_name: str) -> None:
        """Load boundary condition data for the selected boundary.
        
        Args:
            boundary_name: Name of the selected boundary
        """
        # This method would load actual boundary condition data 
        # from OpenFOAM dictionaries
        logger.debug(f"Loading boundary data for: {boundary_name}")
        
        # Here we would parse OpenFOAM dictionary files to populate the UI
        # For now, just a placeholder
        pass
    
    def _on_apply_changes(self) -> None:
        """Apply changes to boundary conditions."""
        selected_items = self.boundary_tree.selectedItems()
        if not selected_items:
            return
        
        boundary_name = selected_items[0].text(0)
        
        # Collect data from UI and write to OpenFOAM dictionary files
        self._save_boundary_data(boundary_name)
        
        QMessageBox.information(
            self, 
            "Boundary Conditions", 
            f"Boundary conditions for '{boundary_name}' have been updated."
        )
    
    def _save_boundary_data(self, boundary_name: str) -> None:
        """Save boundary condition data.
        
        Args:
            boundary_name: Name of the boundary to save data for
        """
        # This method would save UI data to OpenFOAM dictionaries
        logger.debug(f"Saving boundary data for: {boundary_name}")
        
        # Here we would write to OpenFOAM dictionary files
        # For now, just a placeholder
        pass
    
    def _create_fluid_tab(self) -> QWidget:
        """Create the fluid properties tab.
        
        Returns:
            Widget containing fluid properties settings
        """
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        
        # Fluid type selection
        fluid_type_group = QGroupBox("Fluid Type")
        fluid_type_layout = QFormLayout()
        
        self.fluid_type_combo = QComboBox()
        self.fluid_type_combo.addItems([
            "Incompressible", "Compressible", "Multiphase"
        ])
        fluid_type_layout.addRow("Type:", self.fluid_type_combo)
        
        fluid_type_group.setLayout(fluid_type_layout)
        layout.addWidget(fluid_type_group)
        
        # Physical properties
        physical_group = QGroupBox("Physical Properties")
        physical_layout = QFormLayout()
        
        self.density = QDoubleSpinBox()
        self.density.setRange(0.1, 10000)
        self.density.setValue(1.225)  # Air at STP
        self.density.setSuffix(" kg/m³")
        physical_layout.addRow("Density:", self.density)
        
        self.viscosity = QDoubleSpinBox()
        self.viscosity.setRange(1e-6, 100)
        self.viscosity.setValue(1.825e-5)  # Air at STP
        self.viscosity.setDecimals(6)
        self.viscosity.setSuffix(" Pa·s")
        physical_layout.addRow("Dynamic Viscosity:", self.viscosity)
        
        self.specific_heat = QDoubleSpinBox()
        self.specific_heat.setRange(1, 10000)
        self.specific_heat.setValue(1005)  # Air at STP
        self.specific_heat.setSuffix(" J/kg·K")
        physical_layout.addRow("Specific Heat:", self.specific_heat)
        
        self.thermal_conductivity = QDoubleSpinBox()
        self.thermal_conductivity.setRange(0.001, 1000)
        self.thermal_conductivity.setValue(0.0261)  # Air at STP
        self.thermal_conductivity.setDecimals(4)
        self.thermal_conductivity.setSuffix(" W/m·K")
        physical_layout.addRow("Thermal Conductivity:", self.thermal_conductivity)
        
        physical_group.setLayout(physical_layout)
        layout.addWidget(physical_group)
        
        # Add advanced options
        advanced_group = QGroupBox("Advanced Properties")
        advanced_layout = QFormLayout()
        
        self.prandtl_number = QDoubleSpinBox()
        self.prandtl_number.setRange(0.01, 100)
        self.prandtl_number.setValue(0.7)  # Air
        advanced_layout.addRow("Prandtl Number:", self.prandtl_number)
        
        self.schmidt_number = QDoubleSpinBox()
        self.schmidt_number.setRange(0.01, 100)
        self.schmidt_number.setValue(0.7)
        advanced_layout.addRow("Schmidt Number:", self.schmidt_number)
        
        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)
        
        layout.addStretch()
        content.setLayout(layout)
        tab.setWidget(content)
        
        return tab
    
    def _create_thermal_tab(self) -> QWidget:
        """Create the thermal settings tab.
        
        Returns:
            Widget containing thermal settings
        """
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        
        # Energy equation settings
        energy_group = QGroupBox("Energy Settings")
        energy_layout = QFormLayout()
        
        self.energy_enabled = QCheckBox("Enable Energy Equation")
        self.energy_enabled.setChecked(True)
        energy_layout.addRow(self.energy_enabled)
        
        self.buoyancy_enabled = QCheckBox("Enable Buoyancy")
        energy_layout.addRow(self.buoyancy_enabled)
        
        self.reference_temperature = QDoubleSpinBox()
        self.reference_temperature.setRange(0, 1000)
        self.reference_temperature.setValue(300)
        self.reference_temperature.setSuffix(" K")
        energy_layout.addRow("Reference Temperature:", self.reference_temperature)
        
        energy_group.setLayout(energy_layout)
        layout.addWidget(energy_group)
        
        # Radiation model
        radiation_group = QGroupBox("Radiation Model")
        radiation_layout = QFormLayout()
        
        self.radiation_enabled = QCheckBox("Enable Radiation")
        radiation_layout.addRow(self.radiation_enabled)
        
        self.radiation_model = QComboBox()
        self.radiation_model.addItems([
            "None", "P1", "Discrete Ordinates (DO)", 
            "Surface-to-Surface (S2S)", "Discrete Transfer (DTM)"
        ])
        radiation_layout.addRow("Model:", self.radiation_model)
        
        radiation_group.setLayout(radiation_layout)
        layout.addWidget(radiation_group)
        
        layout.addStretch()
        content.setLayout(layout)
        tab.setWidget(content)
        
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
        
        # Turbulence model selection
        model_group = QGroupBox("Turbulence Model")
        model_layout = QFormLayout()
        
        self.turbulence_enabled = QCheckBox("Enable Turbulence")
        self.turbulence_enabled.setChecked(True)
        model_layout.addRow(self.turbulence_enabled)
        
        self.turbulence_model = QComboBox()
        self.turbulence_model.addItems([
            "k-epsilon", "k-omega", "k-omega SST", 
            "Spalart-Allmaras", "LES", "DES", "DNS"
        ])
        model_layout.addRow("Model:", self.turbulence_model)
        
        self.wall_function = QComboBox()
        self.wall_function.addItems([
            "Standard Wall Functions", 
            "Enhanced Wall Treatment",
            "Low-Re Treatment"
        ])
        model_layout.addRow("Wall Treatment:", self.wall_function)
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # Advanced turbulence settings
        advanced_group = QGroupBox("Advanced Settings")
        advanced_layout = QFormLayout()
        
        self.turbulent_intensity = QDoubleSpinBox()
        self.turbulent_intensity.setRange(0.001, 1.0)
        self.turbulent_intensity.setValue(0.05)  # 5%
        self.turbulent_intensity.setSingleStep(0.01)
        advanced_layout.addRow("Turbulent Intensity:", self.turbulent_intensity)
        
        self.turbulent_length_scale = QDoubleSpinBox()
        self.turbulent_length_scale.setRange(0.0001, 100)
        self.turbulent_length_scale.setValue(0.1)
        self.turbulent_length_scale.setSuffix(" m")
        advanced_layout.addRow("Turbulent Length Scale:", self.turbulent_length_scale)
        
        self.turbulent_viscosity_ratio = QDoubleSpinBox()
        self.turbulent_viscosity_ratio.setRange(0.1, 1000)
        self.turbulent_viscosity_ratio.setValue(10)
        advanced_layout.addRow("Turbulent Viscosity Ratio:", self.turbulent_viscosity_ratio)
        
        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)
        
        # Model-specific coefficients
        coefficients_group = QGroupBox("Model Coefficients")
        coefficients_layout = QFormLayout()
        
        self.cmu = QDoubleSpinBox()
        self.cmu.setRange(0.01, 1.0)
        self.cmu.setValue(0.09)
        self.cmu.setSingleStep(0.01)
        coefficients_layout.addRow("Cμ:", self.cmu)
        
        self.c1epsilon = QDoubleSpinBox()
        self.c1epsilon.setRange(0.1, 10.0)
        self.c1epsilon.setValue(1.44)
        self.c1epsilon.setSingleStep(0.01)
        coefficients_layout.addRow("C1ε:", self.c1epsilon)
        
        self.c2epsilon = QDoubleSpinBox()
        self.c2epsilon.setRange(0.1, 10.0)
        self.c2epsilon.setValue(1.92)
        self.c2epsilon.setSingleStep(0.01)
        coefficients_layout.addRow("C2ε:", self.c2epsilon)
        
        coefficients_group.setLayout(coefficients_layout)
        layout.addWidget(coefficients_group)
        
        layout.addStretch()
        content.setLayout(layout)
        tab.setWidget(content)
        
        return tab
    
    def _create_multiphase_tab(self) -> QWidget:
        """Create the multiphase settings tab.
        
        Returns:
            Widget containing multiphase settings
        """
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        
        # Multiphase model selection
        model_group = QGroupBox("Multiphase Model")
        model_layout = QFormLayout()
        
        self.multiphase_enabled = QCheckBox("Enable Multiphase")
        model_layout.addRow(self.multiphase_enabled)
        
        self.multiphase_model = QComboBox()
        self.multiphase_model.addItems([
            "Volume of Fluid (VOF)", 
            "Eulerian", 
            "Mixture", 
            "Discrete Phase Model (DPM)"
        ])
        model_layout.addRow("Model:", self.multiphase_model)
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # Phase settings
        phases_group = QGroupBox("Phase Settings")
        phases_layout = QVBoxLayout()
        
        phases_layout.addWidget(QLabel("Primary Phase:"))
        self.primary_phase = QLineEdit()
        self.primary_phase.setText("water")
        phases_layout.addWidget(self.primary_phase)
        
        phases_layout.addWidget(QLabel("Secondary Phase:"))
        self.secondary_phase = QLineEdit()
        self.secondary_phase.setText("air")
        phases_layout.addWidget(self.secondary_phase)
        
        phases_group.setLayout(phases_layout)
        layout.addWidget(phases_group)
        
        # Interface settings
        interface_group = QGroupBox("Interface Settings")
        interface_layout = QFormLayout()
        
        self.surface_tension = QDoubleSpinBox()
        self.surface_tension.setRange(0, 1)
        self.surface_tension.setValue(0.072)  # Water-air at STP
        self.surface_tension.setSingleStep(0.001)
        self.surface_tension.setSuffix(" N/m")
        interface_layout.addRow("Surface Tension:", self.surface_tension)
        
        interface_group.setLayout(interface_layout)
        layout.addWidget(interface_group)
        
        layout.addStretch()
        content.setLayout(layout)
        tab.setWidget(content)
        
        return tab
    
    def _create_reactions_tab(self) -> QWidget:
        """Create the chemical reactions tab.
        
        Returns:
            Widget containing chemical reaction settings
        """
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        
        # Reaction model
        model_group = QGroupBox("Reaction Model")
        model_layout = QFormLayout()
        
        self.reactions_enabled = QCheckBox("Enable Chemical Reactions")
        model_layout.addRow(self.reactions_enabled)
        
        self.reaction_model = QComboBox()
        self.reaction_model.addItems([
            "Finite-Rate", 
            "Eddy-Dissipation", 
            "Finite-Rate/Eddy-Dissipation",
            "Eddy-Dissipation Concept (EDC)",
            "Laminar Finite-Rate"
        ])
        model_layout.addRow("Model:", self.reaction_model)
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # Species settings
        species_group = QGroupBox("Species")
        species_layout = QVBoxLayout()
        
        species_layout.addWidget(QLabel("Species List:"))
        self.species_list = QLineEdit()
        self.species_list.setText("O2, N2, H2O, CO2")
        species_layout.addWidget(self.species_list)
        
        species_button = QPushButton("Manage Species...")
        species_layout.addWidget(species_button)
        
        species_group.setLayout(species_layout)
        layout.addWidget(species_group)
        
        # Reaction settings
        reaction_group = QGroupBox("Reactions")
        reaction_layout = QVBoxLayout()
        
        reaction_button = QPushButton("Manage Reactions...")
        reaction_layout.addWidget(reaction_button)
        
        reaction_group.setLayout(reaction_layout)
        layout.addWidget(reaction_group)
        
        layout.addStretch()
        content.setLayout(layout)
        tab.setWidget(content)
        
        return tab
    
    def _create_numerics_tab(self) -> QWidget:
        """Create the numerical settings tab.
        
        Returns:
            Widget containing numerical settings
        """
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        
        # Discretization settings
        discretization_group = QGroupBox("Discretization Schemes")
        discretization_layout = QFormLayout()
        
        self.gradient_scheme = QComboBox()
        self.gradient_scheme.addItems([
            "Gauss linear", 
            "Least squares", 
            "Gauss cubic"
        ])
        discretization_layout.addRow("Gradient:", self.gradient_scheme)
        
        self.divergence_scheme = QComboBox()
        self.divergence_scheme.addItems([
            "Gauss upwind", 
            "Gauss linear", 
            "Gauss linearUpwind",
            "Gauss QUICK",
            "Gauss limitedLinear"
        ])
        discretization_layout.addRow("Divergence:", self.divergence_scheme)
        
        self.laplacian_scheme = QComboBox()
        self.laplacian_scheme.addItems([
            "Gauss linear corrected", 
            "Gauss linear limited",
            "Gauss linear orthogonal"
        ])
        discretization_layout.addRow("Laplacian:", self.laplacian_scheme)
        
        self.interpolation_scheme = QComboBox()
        self.interpolation_scheme.addItems([
            "linear", 
            "cubic", 
            "midPoint"
        ])
        discretization_layout.addRow("Interpolation:", self.interpolation_scheme)
        
        discretization_group.setLayout(discretization_layout)
        layout.addWidget(discretization_group)
        
        # Solver settings
        solver_group = QGroupBox("Solver Controls")
        solver_layout = QFormLayout()
        
        self.pressure_solver = QComboBox()
        self.pressure_solver.addItems([
            "GAMG", 
            "PCG", 
            "PBiCGStab",
            "smoothSolver"
        ])
        solver_layout.addRow("Pressure Solver:", self.pressure_solver)
        
        self.velocity_solver = QComboBox()
        self.velocity_solver.addItems([
            "smoothSolver", 
            "PBiCGStab", 
            "GAMG"
        ])
        solver_layout.addRow("Velocity Solver:", self.velocity_solver)
        
        self.convergence_tolerance = QDoubleSpinBox()
        self.convergence_tolerance.setRange(1e-12, 1e-1)
        self.convergence_tolerance.setValue(1e-5)
        self.convergence_tolerance.setDecimals(10)
        solver_layout.addRow("Convergence Tolerance:", self.convergence_tolerance)
        
        self.max_iterations = QSpinBox()
        self.max_iterations.setRange(1, 10000)
        self.max_iterations.setValue(1000)
        solver_layout.addRow("Maximum Iterations:", self.max_iterations)
        
        solver_group.setLayout(solver_layout)
        layout.addWidget(solver_group)
        
        # Relaxation factors
        relaxation_group = QGroupBox("Relaxation Factors")
        relaxation_layout = QFormLayout()
        
        self.pressure_relaxation = QDoubleSpinBox()
        self.pressure_relaxation.setRange(0.1, 1.0)
        self.pressure_relaxation.setValue(0.3)
        self.pressure_relaxation.setSingleStep(0.05)
        relaxation_layout.addRow("Pressure:", self.pressure_relaxation)
        
        self.velocity_relaxation = QDoubleSpinBox()
        self.velocity_relaxation.setRange(0.1, 1.0)
        self.velocity_relaxation.setValue(0.7)
        self.velocity_relaxation.setSingleStep(0.05)
        relaxation_layout.addRow("Velocity:", self.velocity_relaxation)
        
        self.energy_relaxation = QDoubleSpinBox()
        self.energy_relaxation.setRange(0.1, 1.0)
        self.energy_relaxation.setValue(0.7)
        self.energy_relaxation.setSingleStep(0.05)
        relaxation_layout.addRow("Energy:", self.energy_relaxation)
        
        self.turbulence_relaxation = QDoubleSpinBox()
        self.turbulence_relaxation.setRange(0.1, 1.0)
        self.turbulence_relaxation.setValue(0.7)
        self.turbulence_relaxation.setSingleStep(0.05)
        relaxation_layout.addRow("Turbulence:", self.turbulence_relaxation)
        
        relaxation_group.setLayout(relaxation_layout)
        layout.addWidget(relaxation_group)
        
        layout.addStretch()
        content.setLayout(layout)
        tab.setWidget(content)
        
        return tab
    
    def _apply_settings(self) -> None:
        """Apply the settings to the OpenFOAM case."""
        # Here we would save all settings to OpenFOAM dictionaries
        # For now, this is a placeholder
        logger.info("Applying simulation settings")
        
        QMessageBox.information(
            self, 
            "Settings Applied", 
            "Simulation settings have been applied."
        )
        
        # Emit signal to notify others that settings have changed
        self.settings_changed.emit()
    
    def _reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        # This would reset all inputs to default values
        logger.info("Resetting simulation settings to defaults")
        
        reply = QMessageBox.question(
            self, 
            "Reset Settings", 
            "Are you sure you want to reset all settings to defaults?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Reset UI elements
            # This is a placeholder
            QMessageBox.information(
                self, 
                "Settings Reset", 
                "All simulation settings have been reset to defaults."
            )
 
