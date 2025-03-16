# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 15:10:41 2025

@author: adamp
"""

import os
import json
import datetime
from typing import Dict, Any, Optional

class ProjectManager:
    """Manages CFD projects including saving, loading, and tracking project data"""
    
    def __init__(self):
        self.current_project: Optional[Dict[str, Any]] = None
        self.current_project_path: Optional[str] = None
        self.project_modified = False
        
    def new_project(self, project_name: str, project_dir: str) -> bool:
        """Create a new CFD project with basic structure"""
        if not os.path.exists(project_dir):
            try:
                os.makedirs(project_dir)
            except OSError as e:
                print(f"Error creating project directory: {str(e)}")
                return False
                
        # Create basic project structure
        subdirs = ["geometry", "mesh", "case", "results"]
        for subdir in subdirs:
            os.makedirs(os.path.join(project_dir, subdir), exist_ok=True)
            
        # Create project metadata
        self.current_project = {
            "name": project_name,
            "created": datetime.datetime.now().isoformat(),
            "modified": datetime.datetime.now().isoformat(),
            "version": "1.0.0",
            "openfoam_version": "v2306",  # Default OpenFOAM version
            "geometry": None,
            "mesh": None,
            "models": {},
            "boundary_conditions": {},
            "solver_settings": {},
            "simulation_status": "not_started"
        }
        
        # Save project file
        project_file = os.path.join(project_dir, f"{project_name}.ofproj")
        self.current_project_path = project_file
        self.save_project()
        
        return True
        
    def save_project(self) -> bool:
        """Save current project to disk"""
        if not self.current_project or not self.current_project_path:
            return False
            
        try:
            # Update modified timestamp
            self.current_project["modified"] = datetime.datetime.now().isoformat()
            
            # Write to file
            with open(self.current_project_path, 'w') as f:
                json.dump(self.current_project, f, indent=2)
                
            self.project_modified = False
            return True
            
        except Exception as e:
            print(f"Error saving project: {str(e)}")
            return False
            
    def load_project(self, project_path: str) -> bool:
        """Load a project from disk"""
        try:
            with open(project_path, 'r') as f:
                self.current_project = json.load(f)
                
            self.current_project_path = project_path
            self.project_modified = False
            return True
            
        except Exception as e:
            print(f"Error loading project: {str(e)}")
            return False
