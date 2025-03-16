# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 15:12:33 2025

@author: adamp
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                           QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

class WelcomeWidget(QWidget):
    """Welcome screen shown when the application starts."""
    
    # Signals
    new_project_requested = pyqtSignal()
    open_project_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the welcome screen UI."""
        main_layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Welcome to OpenFOAM CFD Interface")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "A comprehensive user interface for advanced computational fluid dynamics "
            "simulations based on OpenFOAM, supporting complex thermal and fluid flow analyses."
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(desc_label)
        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        new_button = QPushButton(QIcon("resources/icons/new.png"), "New Project")
        new_button.setMinimumWidth(150)
        new_button.clicked.connect(self.on_new_project)
        button_layout.addWidget(new_button)
        
        open_button = QPushButton(QIcon("resources/icons/open.png"), "Open Project")
        open_button.setMinimumWidth(150)
        open_button.clicked.connect(self.on_open_project)
        button_layout.addWidget(open_button)
        
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        main_layout.addLayout(button_layout)
        
        # Recent projects (placeholder)
        recent_label = QLabel("Recent Projects")
        recent_font = QFont()
        recent_font.setBold(True)
        recent_label.setFont(recent_font)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))
        main_layout.addWidget(recent_label)
        
        # Placeholder for recent project list
        main_layout.addWidget(QLabel("No recent projects found"))
        
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(main_layout)
        
    def on_new_project(self):
        """Handle new project button click."""
        if self.parent:
            self.parent.new_project()
        else:
            self.new_project_requested.emit()
            
    def on_open_project(self):
        """Handle open project button click."""
        if self.parent:
            self.parent.open_project()
        else:
            self.open_project_requested.emit()