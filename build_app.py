#!/usr/bin/env python3
"""
Build script for PASS // FAIL Hash Verifier
Creates standalone executables for different platforms
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔨 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error output: {e.stderr}")
        return False

def build_app():
    """Build the application for the current platform"""
    
    # Get the virtual environment Python path
    if platform.system() == "Windows":
        python_cmd = os.path.join(".venv", "Scripts", "python.exe")
        if not os.path.exists(python_cmd):
            python_cmd = "python"
    else:
        python_cmd = os.path.join(".venv", "bin", "python")
        if not os.path.exists(python_cmd):
            python_cmd = "python3"
    
    # Clean previous builds
    print("🧹 Cleaning previous builds...")
    for folder in ["build", "dist", "__pycache__"]:
        if os.path.exists(folder):
            if platform.system() == "Windows":
                os.system(f'rmdir /s /q "{folder}" 2>nul')
            else:
                os.system(f'rm -rf "{folder}"')
    
    # Remove spec files
    for spec_file in ["PASS-FAIL-Hash-Verifier.spec"]:
        if os.path.exists(spec_file):
            os.remove(spec_file)
    
    print("✅ Cleanup completed!")
    
    # Build command based on platform
    current_os = platform.system()
    
    if current_os == "Darwin":  # macOS
        # Create app icon from image02.png with macOS rounded corners
        print("🎨 Creating macOS-style app icon from image02.png...")
        if os.path.exists("src/images/image02.png"):
            # Use the standalone rounded icon creator script
            run_command(f'{python_cmd} create_macos_icon.py src/images/image02.png', "Creating rounded macOS icon")
        
        # First create a spec file for better dependency handling
        print("🔧 Creating optimized spec file...")
        spec_content = '''# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

# Collect all data and imports from problematic modules
datas = []
binaries = []
hiddenimports = []

# PIL/Pillow support
tmp_ret = collect_all('PIL')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# tkinterdnd2 support
tmp_ret = collect_all('tkinterdnd2')
datas += tmp_ret[0] 
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# Add explicit hidden imports that PyInstaller might miss
hiddenimports += [
    'PIL._imaging', 'PIL.Image', 'PIL.ImageTk', 'tkinterdnd2',
    'tkinter', 'tkinter.messagebox', 'tkinter.filedialog', 'tkinter.ttk',
    'hashlib', 'threading', 'os', 'sys', 'time', 'math', 'collections',
]

# Add our data files
datas += [('src/images', 'images'), ('src/wordlists', 'wordlists')]

a = Analysis(['src/main.py'], pathex=[], binaries=binaries, datas=datas,
             hiddenimports=hiddenimports, hookspath=[], hooksconfig={},
             runtime_hooks=[], excludes=[], noarchive=False, optimize=0)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='PASS-FAIL-Hash-Verifier',
          debug=False, bootloader_ignore_signals=False, strip=False, upx=True,
          console=False, disable_windowed_traceback=False, argv_emulation=False,
          target_arch=None, codesign_identity=None, entitlements_file=None)

coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=True, upx_exclude=[], name='PASS-FAIL-Hash-Verifier')

app = BUNDLE(coll, name='PASS-FAIL-Hash-Verifier.app', icon='app_icon.icns',
             bundle_identifier='com.yourname.pass-fail-hash-verifier',
             info_plist={'NSPrincipalClass': 'NSApplication', 'NSAppleScriptEnabled': False, 'NSHighResolutionCapable': 'True'})
'''
        with open("PASS-FAIL-Hash-Verifier.spec", "w") as f:
            f.write(spec_content)
        
        cmd = f'{python_cmd} -m PyInstaller --noconfirm PASS-FAIL-Hash-Verifier.spec'
        build_type = "macOS App Bundle (.app)"
        
    elif current_os == "Windows":  # Windows
        cmd = f'{python_cmd} -m PyInstaller --onefile --windowed --add-data "src/images;images" --add-data "src/wordlists;wordlists" --name "PASS-FAIL-Hash-Verifier" --clean --noconfirm src/main.py'
        build_type = "Windows Executable (.exe)"
        
    elif current_os == "Linux":  # Linux
        cmd = f'{python_cmd} -m PyInstaller --onefile --add-data "src/images:images" --add-data "src/wordlists:wordlists" --name "PASS-FAIL-Hash-Verifier" --clean --noconfirm src/main.py'
        build_type = "Linux Executable"
        
    else:
        print(f"❌ Unsupported platform: {current_os}")
        return False
    
    print(f"🎯 Building {build_type} for {current_os}...")
    
    if run_command(cmd, f"Building {build_type}"):
        print(f"\n🎉 Build completed successfully!")
        print(f"📂 Output location: dist/")
        
        # List what was created
        if os.path.exists("dist"):
            print("📋 Created files:")
            for item in os.listdir("dist"):
                item_path = os.path.join("dist", item)
                if os.path.isfile(item_path):
                    size = os.path.getsize(item_path)
                    size_mb = size / (1024 * 1024)
                    print(f"   📄 {item} ({size_mb:.1f} MB)")
                elif os.path.isdir(item_path):
                    print(f"   📁 {item}/")
        
        # Platform-specific instructions
        if current_os == "Darwin":
            print(f"\n🚀 To run: double-click 'PASS-FAIL-Hash-Verifier.app' in the dist/ folder")
            print(f"📦 To share: zip the entire 'PASS-FAIL-Hash-Verifier.app' folder")
            
        elif current_os == "Windows":
            print(f"\n🚀 To run: double-click 'PASS-FAIL-Hash-Verifier.exe' in the dist/ folder")
            print(f"📦 To share: just share the 'PASS-FAIL-Hash-Verifier.exe' file")
            
        elif current_os == "Linux":
            print(f"\n🚀 To run: ./dist/PASS-FAIL-Hash-Verifier")
            print(f"📦 To share: just share the 'PASS-FAIL-Hash-Verifier' file")
            
        return True
    else:
        return False

def main():
    """Main function"""
    print("🔧 PASS // FAIL Hash Verifier - Build Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("src/main.py"):
        print("❌ Error: Please run this script from the pass_fail_gui directory")
        print("   Expected to find: src/main.py")
        return False
    
    # Get the virtual environment Python path
    if platform.system() == "Windows":
        python_cmd = os.path.join(".venv", "Scripts", "python.exe")
        if not os.path.exists(python_cmd):
            python_cmd = "python"
    else:
        python_cmd = os.path.join(".venv", "bin", "python")
        if not os.path.exists(python_cmd):
            python_cmd = "python3"
    
    # Check if PyInstaller is installed
    try:
        subprocess.run([python_cmd, "-c", "import PyInstaller"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ PyInstaller not found. Installing...")
        if not run_command(f"{python_cmd} -m pip install pyinstaller", "Installing PyInstaller"):
            return False
    
    # Build the app
    return build_app()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
    
    print("\n✨ Build process completed!")
