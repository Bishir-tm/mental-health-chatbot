#!/usr/bin/env python3
"""
Setup script for AI Mental Health Chatbot with TinyLLaMA
This script automates the installation and first-run setup process.
"""

import os
import sys
import subprocess
import platform
import time

def print_step(step, description):
    """Print formatted step information"""
    print(f"\n{'='*60}")
    print(f"STEP {step}: {description}")
    print('='*60)

def run_command(command, description=""):
    """Run a command and handle errors"""
    print(f"Running: {command}")
    if description:
        print(f"Purpose: {description}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success!")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.output}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_disk_space():
    """Check available disk space"""
    try:
        import shutil
        total, used, free = shutil.disk_usage(".")
        free_gb = free / (1024**3)
        print(f"Available disk space: {free_gb:.1f} GB")
        if free_gb < 6:
            print("⚠️  Warning: Less than 6GB free space. Model download may fail.")
            return False
        return True
    except Exception as e:
        print(f"Could not check disk space: {e}")
        return True

def create_virtual_environment():
    """Create and activate virtual environment"""
    venv_name = "venv"
    
    if os.path.exists(venv_name):
        print(f"Virtual environment '{venv_name}' already exists")
        return True
    
    success = run_command(f"{sys.executable} -m venv {venv_name}", 
                         "Creating virtual environment")
    
    if success:
        if platform.system() == "Windows":
            activate_script = f"{venv_name}\\Scripts\\activate.bat"
        else:
            activate_script = f"source {venv_name}/bin/activate"
        
        print(f"✅ Virtual environment created!")
        print(f"To activate manually: {activate_script}")
    
    return success

def install_dependencies():
    """Install required Python packages"""
    
    # Determine pip path based on platform
    if platform.system() == "Windows":
        pip_path = "venv\\Scripts\\pip"
    else:
        pip_path = "venv/bin/pip"
    
    # Upgrade pip first
    print("Upgrading pip...")
    run_command(f"{pip_path} install --upgrade pip")
    
    # Install PyTorch first (it's the biggest dependency)
    print("Installing PyTorch (this may take a while)...")
    torch_command = f"{pip_path} install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu"
    if not run_command(torch_command, "Installing PyTorch CPU version"):
        # Fallback to regular pip install
        run_command(f"{pip_path} install torch", "Installing PyTorch via regular pip")
    
    # Install other requirements
    print("Installing other dependencies...")
    return run_command(f"{pip_path} install -r requirements.txt", 
                      "Installing application dependencies")

def test_model_loading():
    """Test if the model can be loaded"""
    print("Testing model loading (this will download ~2.2GB on first run)...")
    
    test_script = """
import sys
sys.path.append('.')
try:
    from app import initialize_model
    print("Testing model initialization...")
    success = initialize_model()
    if success:
        print("✅ Model loaded successfully!")
        sys.exit(0)
    else:
        print("❌ Model loading failed!")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error during model test: {e}")
    sys.exit(1)
"""
    
    # Write test script to temporary file
    with open("test_model.py", "w") as f:
        f.write(test_script)
    
    try:
        if platform.system() == "Windows":
            python_path = "venv\\Scripts\\python"
        else:
            python_path = "venv/bin/python"
        
        success = run_command(f"{python_path} test_model.py", 
                             "Testing model initialization")
        
        # Clean up test file
        if os.path.exists("test_model.py"):
            os.remove("test_model.py")
        
        return success
    
    except Exception as e:
        print(f"Model test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🤖 AI Mental Health Chatbot Setup")
    print("This script will set up TinyLLaMA chatbot for offline use")
    
    # Step 1: Check system requirements
    print_step(1, "Checking System Requirements")
    
    if not check_python_version():
        print("Please install Python 3.8 or higher and try again.")
        return False
    
    check_disk_space()
    
    # Step 2: Create virtual environment
    print_step(2, "Creating Virtual Environment")
    
    if not create_virtual_environment():
        print("Failed to create virtual environment")
        return False
    
    # Step 3: Install dependencies
    print_step(3, "Installing Dependencies")
    
    if not install_dependencies():
        print("Failed to install dependencies")
        return False
    
    # Step 4: Test model loading
    print_step(4, "Testing Model Loading")
    print("⚠️  This step will download ~2.2GB for the AI model")
    
    user_input = input("Continue with model download? (y/n): ").lower().strip()
    if user_input != 'y':
        print("Setup incomplete. Run this script again when ready to download the model.")
        return False
    
    if not test_model_loading():
        print("Model loading test failed. You may need to run the app manually.")
    
    # Step 5: Final instructions
    print_step(5, "Setup Complete!")
    
    print("🎉 Installation successful!")
    print("\nTo start the chatbot:")
    if platform.system() == "Windows":
        print("1. venv\\Scripts\\activate")
    else:
        print("1. source venv/bin/activate")
    
    print("2. python app.py")
    print("3. Open http://127.0.0.1:5000 in your browser")
    
    print("\n📝 Important Notes:")
    print("- First run may take a few minutes to load the model")
    print("- The model files are cached locally for offline use")
    print("- All conversations remain private on your device")
    print("- This is for educational/supportive purposes only")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Setup failed. Please check the errors above and try again.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)