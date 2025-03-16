from src.core.openfoam.openfoam_environment import OpenFOAMEnvironment

def test_environment():
    """Test the OpenFOAM environment configuration"""
    print("Testing OpenFOAM environment...")
    env = OpenFOAMEnvironment()
    print(f"OpenFOAM mode: {'WSL' if env.use_wsl else 'Native Windows'}")
    
    version = env.get_openfoam_version()
    print(f"OpenFOAM version: {version}")
    
    # Test simple command
    result = env.run_command("foamVersion")
    print("\nCommand test result:")
    print(f"Return code: {result.returncode}")
    print(f"Output: {result.stdout}")
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        print("\nTroubleshooting tips:")
        if env.use_wsl:
            print("1. Check that OpenFOAM is properly installed in WSL")
            print(f"2. Verify the OpenFOAM bashrc path ({env.config.get('openfoam_bashrc')})")
            print("3. Try running the following command in PowerShell:")
            bashrc_path = env.config.get("openfoam_bashrc", "/opt/openfoam12/etc/bashrc")
            print(f"   wsl bash -c 'source {bashrc_path} && foamVersion'")
        else:
            print("1. Verify OpenFOAM/blueCFD is installed")
            print("2. Check if the OpenFOAM environment variables are set")
            print("3. Try running the command from the blueCFD command prompt")
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
            print("See troubleshooting tips for running paraFoam in WSL:")
            print("1. Install an X server like VcXsrv on Windows")
            print("2. Configure DISPLAY environment variable in WSL")
            print("3. Follow instructions at https://openfoam.org/download/windows/")

if __name__ == "__main__":
    test_environment()