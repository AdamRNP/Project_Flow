def __init__(self, config_path=None):
    """Initialize OpenFOAM environment with WSL support"""
    import os
    import json
    from pathlib import Path
    
    # Load configuration
    try:
        if config_path is None:
            config_path = Path("config/openfoam_config.json")
        
        with open(config_path, "r") as f:
            self.config = json.load(f)
    except Exception as e:
        print(f"Error loading OpenFOAM config: {e}")
        # Default configuration for WSL
        self.config = {
            "wsl_enabled": True,
            "openfoam_path": "/opt/openfoam10",
            "openfoam_version": "10"
        }
    
    # Store whether WSL should be used
    self.use_wsl = os.name == 'nt' and self.config.get("wsl_enabled", True)
    
    # Environment variables aren't needed when using WSL this way
    self.env_vars = os.environ.copy()