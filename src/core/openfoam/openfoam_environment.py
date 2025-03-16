"""
OpenFOAM environment handling module for Windows.
Supports both native Windows OpenFOAM (blueCFD) and WSL OpenFOAM.
"""

import os
import json
import subprocess
from pathlib import Path

class OpenFOAMEnvironment:
    """Manages OpenFOAM execution environment on Windows"""
    
    def __init__(self, config_path=None):
        """Initialize with optional custom config path"""
        if config_path is None:
            # Default to script directory
            config_path = Path(__file__).parent / "openfoam_config.json"
        
        self.config = self._load_config(config_path)
        self.use_wsl = self.config.get("use_wsl", True)
        self.config_path = config_path
        
        # If config was created from defaults, save it
        if not os.path.exists(config_path):
            try:
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                with open(config_path, 'w') as f:
                    json.dump(self.config, f, indent=4)
                print(f"Created default configuration at {config_path}")
            except Exception as e:
                print(f"Warning: Could not save default configuration: {e}")
    
    def _load_config(self, config_path):
        """Load OpenFOAM configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Config file not found or invalid. Creating default configuration.")
            # Create default config based on your working setup
            return {
                "use_wsl": True,
                "wsl_distro": "",  # Leave empty to use default distro
                "openfoam_version": "12",
                "openfoam_bashrc": "/opt/openfoam12/etc/bashrc"
            }
    
    def run_command(self, command):
        """Run an OpenFOAM command"""
        if self.use_wsl:
            return self._run_wsl_command(command)
        else:
            return self._run_windows_command(command)
    
    def _run_wsl_command(self, command):
        """Run command through WSL"""
        bashrc_path = self.config.get("openfoam_bashrc", "/opt/openfoam12/etc/bashrc")
        distro = self.config.get("wsl_distro", "")
        
        wsl_prefix = "wsl"
        if distro:
            wsl_prefix += f" -d {distro}"
        
        # Fix: Properly escape the command with double quotes
        full_command = f'{wsl_prefix} bash -c "source {bashrc_path} && {command}"'
        
        print(f"Executing WSL command: {full_command}")
        
        # Run the command
        result = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True
        )
        
        return result
    
    def _run_windows_command(self, command):
        """Run command on native Windows OpenFOAM"""
        # For native Windows OpenFOAM (blueCFD)
        # Implement if needed
        raise NotImplementedError("Native Windows OpenFOAM not implemented yet")
    
    def get_version(self):
        """Get OpenFOAM version"""
        result = self.run_command("foamVersion")
        if result.returncode == 0:
            return result.stdout.strip()
        return "Unknown"

def test_environment():
    """Test the OpenFOAM environment setup"""
    print("\nTesting OpenFOAM environment...\n")
    
    env = OpenFOAMEnvironment()
    
    print(f"OpenFOAM mode: {'WSL' if env.use_wsl else 'Native Windows'}\n")
    
    # Test OpenFOAM version command
    version_result = env.run_command("foamVersion")
    
    if version_result.returncode == 0:
        version = version_result.stdout.strip()
        print(f"OpenFOAM version: {version}\n")
    else:
        version = "Unknown"
        print(f"Could not determine OpenFOAM version. Error: {version_result.stderr}\n")
    
    # Test a simple command
    test_cmd = "foamVersion"
    print(f"Testing command: {test_cmd}")
    result = env.run_command(test_cmd)
    
    print("\nCommand test result:")
    print(f"Return code: {result.returncode}")
    print(f"Output:\n{result.stdout}")
    
    if result.stderr:
        print(f"Error output:\n{result.stderr}")
    
    if result.returncode != 0:
        print("\nTroubleshooting tips:")
        print("1. Check that OpenFOAM is properly installed in WSL")
        print(f"2. Verify the OpenFOAM bashrc path ({env.config.get('openfoam_bashrc')})")
        print("3. Try running the following command in PowerShell:")
        bashrc_path = env.config.get("openfoam_bashrc")
        print(f"   wsl bash -c \"source {bashrc_path} && foamVersion\"")
    else:
        print("\nSuccess! OpenFOAM environment is properly configured.")
        
        # Test an additional simple OpenFOAM command
        print("\nTesting paraFoam command availability...")
        parafoam_result = env.run_command("which paraFoam")
        if parafoam_result.returncode == 0:
            print(f"paraFoam found at: {parafoam_result.stdout.strip()}")
        else:
            print("paraFoam may not be installed or not in PATH")
            print("If you need to use paraFoam, make sure ParaView is installed in your WSL environment")

if __name__ == "__main__":
    test_environment()
