# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 15:15:32 2025

@author: adamp
"""

from PyQt5.QtWidgets import (QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, 
                            QLabel, QComboBox, QFormLayout, QDoubleSpinBox,
                            QCheckBox, QRadioButton, QStackedWidget)
from PyQt5.QtCore import pyqtSignal

class TurbulenceModelWidget(QGroupBox):
    """Widget for configuring turbulence models."""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__("Turbulence", parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the turbulence model UI."""
        main_layout = QVBoxLayout()
        
        # Turbulence type
        type_layout = QFormLayout()
        
        self.turbulence_enabled = QCheckBox("Enable Turbulence")
        self.turbulence_enabled.setChecked(True)
        self.turbulence_enabled.toggled.connect(self.on_turbulence_toggled)
        type_layout.addRow("", self.turbulence_enabled)
        
        self.model_combo = QComboBox()
        turbulence_models = [
            "k-epsilon",
            "k-omega SST",
            "Spalart-Allmaras",
            "Reynolds Stress Model (RSM)",
            "LES Smagorinsky",
            "LES Dynamic"
        ]
        self.model_combo.addItems(turbulence_models)
        self.model_combo.currentIndexChanged.connect(self.on_model_changed)
        type_layout.addRow("Model:", self.model_combo)
        
        # Near wall treatment
        self.wall_treatment = QComboBox()
        wall_treatments = [
            "Wall Functions",
            "Enhanced Wall Treatment",
            "Low-Re Approach"
        ]
        self.wall_treatment.addItems(wall_treatments)
        self.wall_treatment.currentIndexChanged.connect(self.settings_changed)
        type_layout.addRow("Wall Treatment:", self.wall_treatment)
        
        main_layout.addLayout(type_layout)
        
        # Stacked widget for model-specific settings
        self.model_settings = QStackedWidget()
        
        # k-epsilon settings
        self.k_epsilon_widget = QWidget()
        k_epsilon_layout = QFormLayout(self.k_epsilon_widget)
        
        self.k_epsilon_cmu = QDoubleSpinBox()
        self.k_epsilon_cmu.setRange(0.01, 1.0)
        self.k_epsilon_cmu.setSingleStep(0.01)
        self.k_epsilon_cmu.setValue(0.09)
        k_epsilon_layout.addRow("Cμ:", self.k_epsilon_cmu)
        
        self.k_epsilon_c1 = QDoubleSpinBox()
        self.k_epsilon_c1.setRange(0.1, 5.0)
        self.k_epsilon_c1.setSingleStep(0.1)
        self.k_epsilon_c1.setValue(1.44)
        k_epsilon_layout.addRow("C1ε:", self.k_epsilon_c1)
        
        self.k_epsilon_c2 = QDoubleSpinBox()
        self.k_epsilon_c2.setRange(0.1, 5.0)
        self.k_epsilon_c2.setSingleStep(0.1)
        self.k_epsilon_c2.setValue(1.92)
        k_epsilon_layout.addRow("C2ε:", self.k_epsilon_c2)
        
        self.model_settings.addWidget(self.k_epsilon_widget)
        
        # k-omega SST settings
        self.k_omega_widget = QWidget()
        k_omega_layout = QFormLayout(self.k_omega_widget)
        
        self.k_omega_alpha = QDoubleSpinBox()
        self.k_omega_alpha.setRange(0.01, 1.0)
        self.k_omega_alpha.setSingleStep(0.01)
        self.k_omega_alpha.setValue(0.52)
        k_omega_layout.addRow("α∞*:", self.k_omega_alpha)
        
        self.k_omega_beta = QDoubleSpinBox()
        self.k_omega_beta.setRange(0.01, 1.0)
        self.k_omega_beta.setSingleStep(0.01)
        self.k_omega_beta.setValue(0.09)
        k_omega_layout.addRow("β*:", self.k_omega_beta)
        
        self.model_settings.addWidget(self.k_omega_widget)
        
        # Add placeholder widgets for other models
        for _ in range(4):
            self.model_settings.addWidget(QWidget())
        
        main_layout.addWidget(self.model_settings)
        
        # Advanced options
        advanced_group = QGroupBox("Advanced Options")
        advanced_layout = QFormLayout()
        
        self.yplus_target = QDoubleSpinBox()
        self.yplus_target.setRange(1, 1000)
        self.yplus_target.setValue(30)
        advanced_layout.addRow("Target y+:", self.yplus_target)
        
        self.turbulent_schmidt = QDoubleSpinBox()
        self.turbulent_schmidt.setRange(0.1, 10.0)
        self.turbulent_schmidt.setSingleStep(0.1)
        self.turbulent_schmidt.setValue(0.9)
        advanced_layout.addRow("Turbulent Schmidt Number:", self.turbulent_schmidt)
        
        self.turbulent_prandtl = QDoubleSpinBox()
        self.turbulent_prandtl.setRange(0.1, 10.0)
        self.turbulent_prandtl.setSingleStep(0.1)
        self.turbulent_prandtl.setValue(0.85)
        advanced_layout.addRow("Turbulent Prandtl Number:", self.turbulent_prandtl)
        
        advanced_group.setLayout(advanced_layout)
        main_layout.addWidget(advanced_group)
        
        main_layout.addStretch(1)
        self.setLayout(main_layout)
        
    def on_turbulence_toggled(self, checked):
        """Handle turbulence enabling/disabling."""
        self.model_combo.setEnabled(checked)
        self.wall_treatment.setEnabled(checked)
        self.model_settings.setEnabled(checked)
        self.settings_changed.emit()
        
    def on_model_changed(self, index):
        """Handle turbulence model selection change."""
        self.model_settings.setCurrentIndex(index)
        self.settings_changed.emit()
        
    def get_settings(self):
        """Get current turbulence settings."""
        settings = {
            "enabled": self.turbulence_enabled.isChecked(),
            "model": self.model_combo.currentText() if self.turbulence_enabled.isChecked() else "laminar",
            "wall_treatment": self.wall_treatment.currentText(),
            "target_yplus": self.yplus_target.value(),
            "turbulent_schmidt": self.turbulent_schmidt.value(),
            "turbulent_prandtl": self.turbulent_prandtl.value()
        }
        
        # Add model-specific settings
        if self.turbulence_enabled.isChecked():
            model_index = self.model_combo.currentIndex()
            
            if model_index == 0:  # k-epsilon
                settings.update({
                    "Cmu": self.k_epsilon_cmu.value(),
                    "C1": self.k_epsilon_c1.value(),
                    "C2": self.k_epsilon_c2.value()
                })
            elif model_index == 1:  # k-omega SST
                settings.update({
                    "alpha": self.k_omega_alpha.value(),
                    "beta": self.k_omega_beta.value()
                })
        
        return settings
        
    def reset_settings(self):
        """Reset turbulence settings to defaults."""
        self.turbulence_enabled.setChecked(True)
        self.model_combo.setCurrentIndex(0)
        self.wall_treatment.setCurrentIndex(0)
        self.yplus_target.setValue(30)
        self.turbulent_schmidt.setValue(0.9)
        self.turbulent_prandtl.setValue(0.85)
        
        # Reset model-specific settings
        self.k_epsilon_cmu.setValue(0.09)
        self.k_epsilon_c1.setValue(1.44)
        self.k_epsilon_c2.setValue(1.92)
        self.k_omega_alpha.setValue(0.52)
        self.k_omega_beta.setValue(0.09)
        
        self.settings_changed.emit()
