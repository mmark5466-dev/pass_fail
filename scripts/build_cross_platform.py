#!/usr/bin/env python3
"""
Enhanced Cross-Platform Build Script

This script builds the PASS // FAIL Hash Verifier app for multiple platforms
with platform-appropriate icons and configurations.

Usage:
    python build_cross_platform.py [platform]
    
    platform options:
    - macos (default on macOS)
    - windows (creates Windows executable)  
    - linux (creates Linux executable)
    - all (creates all platform builds)

Features:
- Uses appropriate icon format for each platform
- Optimizes build settings per platform
- Creates platform-specific directory structures
- Follows each platform's packaging conventions
"""

import os
import sys
import shutil
import subprocess
import platform as sys_platform
from pathlib import Path

def clean_previous_builds():
    """Remove previous build and dist directories"""
    print("🧹 Cleaning previous builds...")
    dirs_to_remove = ["build", "dist"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  🗑️  Removed {dir_name}/")
    
    # Also clean up any leftover spec files in root
    cleanup_temp_specs()
    
    print("✅ Cleanup completed!")

def create_macos_spec():
    """Create PyInstaller spec file optimized for macOS"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

# Collect all data and imports
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

# Add explicit hidden imports
hiddenimports += [
    'PIL._imaging', 'PIL.Image', 'PIL.ImageTk', 'tkinterdnd2',
    'tkinter', 'tkinter.messagebox', 'tkinter.filedialog', 'tkinter.ttk',
    'hashlib', 'threading', 'os', 'sys', 'time', 'math', 'collections', 'platform',
]

# Add data files
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

app = BUNDLE(coll, name='PASS-FAIL-Hash-Verifier.app', icon='icons/app_icon.icns',
             bundle_identifier='com.hashverifier.pass-fail-hash-verifier',
             info_plist={
                'NSPrincipalClass': 'NSApplication', 
                'NSAppleScriptEnabled': False, 
                'NSHighResolutionCapable': 'True',
                'CFBundleDisplayName': 'PASS // FAIL Hash Verifier',
                'CFBundleVersion': '2.0.0',
                'CFBundleShortVersionString': '2.0'
             })
'''
    
    with open("PASS-FAIL-Hash-Verifier-macOS.spec", "w") as f:
        f.write(spec_content)
    
    return "PASS-FAIL-Hash-Verifier-macOS.spec"

def create_windows_spec():
    """Create PyInstaller spec file optimized for Windows"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

# Collect all data and imports
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

# Add explicit hidden imports
hiddenimports += [
    'PIL._imaging', 'PIL.Image', 'PIL.ImageTk', 'tkinterdnd2',
    'tkinter', 'tkinter.messagebox', 'tkinter.filedialog', 'tkinter.ttk',
    'hashlib', 'threading', 'os', 'sys', 'time', 'math', 'collections', 'platform',
]

# Add data files
datas += [('src/images', 'images'), ('src/wordlists', 'wordlists')]

a = Analysis(['src/main.py'], pathex=[], binaries=binaries, datas=datas,
             hiddenimports=hiddenimports, hookspath=[], hooksconfig={},
             runtime_hooks=[], excludes=[], noarchive=False, optimize=0)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name='PASS-FAIL-Hash-Verifier',
          debug=False, bootloader_ignore_signals=False, strip=False, upx=True,
          runtime_tmpdir=None, console=False, disable_windowed_traceback=False,
          argv_emulation=False, target_arch=None, codesign_identity=None,
          entitlements_file=None, icon='icons/app_icon.ico')
'''
    
    with open("PASS-FAIL-Hash-Verifier-Windows.spec", "w") as f:
        f.write(spec_content)
    
    return "PASS-FAIL-Hash-Verifier-Windows.spec"

def create_linux_spec():
    """Create PyInstaller spec file optimized for Linux"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

# Collect all data and imports
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

# Add explicit hidden imports
hiddenimports += [
    'PIL._imaging', 'PIL.Image', 'PIL.ImageTk', 'tkinterdnd2',
    'tkinter', 'tkinter.messagebox', 'tkinter.filedialog', 'tkinter.ttk',
    'hashlib', 'threading', 'os', 'sys', 'time', 'math', 'collections', 'platform',
]

# Add data files
datas += [('src/images', 'images'), ('src/wordlists', 'wordlists')]

a = Analysis(['src/main.py'], pathex=[], binaries=binaries, datas=datas,
             hiddenimports=hiddenimports, hookspath=[], hooksconfig={},
             runtime_hooks=[], excludes=[], noarchive=False, optimize=0)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name='PASS-FAIL-Hash-Verifier',
          debug=False, bootloader_ignore_signals=False, strip=False, upx=True,
          runtime_tmpdir=None, console=False, disable_windowed_traceback=False,
          argv_emulation=False, target_arch=None, codesign_identity=None,
          entitlements_file=None)
'''
    
    with open("PASS-FAIL-Hash-Verifier-Linux.spec", "w") as f:
        f.write(spec_content)
    
    return "PASS-FAIL-Hash-Verifier-Linux.spec"

def cleanup_temp_specs():
    """Remove temporary spec files from root directory"""
    spec_files = [
        "PASS-FAIL-Hash-Verifier-macOS.spec",
        "PASS-FAIL-Hash-Verifier-Windows.spec", 
        "PASS-FAIL-Hash-Verifier-Linux.spec"
    ]
    
    for spec_file in spec_files:
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print(f"🧹 Cleaned up: {spec_file}")

def build_macos():
    """Build macOS application"""
    print("🍎 Building macOS Application...")
    
    if not os.path.exists("icons/app_icon.icns"):
        print("❌ Error: icons/app_icon.icns not found. Run scripts/create_cross_platform_icons.py first.")
        return False
    
    spec_file = create_macos_spec()
    
    try:
        result = subprocess.run([
            "pyinstaller", "--clean", "--noconfirm", spec_file
        ], check=True, capture_output=True, text=True)
        
        if os.path.exists("dist/PASS-FAIL-Hash-Verifier.app"):
            size = shutil.disk_usage("dist").used
            print("✅ macOS build completed successfully!")
            print(f"📂 Output: dist/PASS-FAIL-Hash-Verifier.app")
            return True
        else:
            print("❌ macOS build failed - no output file created")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ macOS build failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout[-500:])  # Last 500 chars
        if e.stderr:
            print("STDERR:", e.stderr[-500:])  # Last 500 chars
        return False
    finally:
        # Clean up temporary spec file
        if spec_file and os.path.exists(spec_file):
            os.remove(spec_file)

def build_windows():
    """Build Windows executable"""
    print("🪟 Building Windows Executable...")
    
    if not os.path.exists("icons/app_icon.ico"):
        print("❌ Error: icons/app_icon.ico not found. Run scripts/create_cross_platform_icons.py first.")
        return False
    
    spec_file = create_windows_spec()
    
    try:
        result = subprocess.run([
            "pyinstaller", "--clean", "--noconfirm", spec_file
        ], check=True, capture_output=True, text=True)
        
        if os.path.exists("dist/PASS-FAIL-Hash-Verifier.exe"):
            file_size = os.path.getsize("dist/PASS-FAIL-Hash-Verifier.exe")
            size_mb = file_size / (1024 * 1024)
            print("✅ Windows build completed successfully!")
            print(f"📂 Output: dist/PASS-FAIL-Hash-Verifier.exe ({size_mb:.1f} MB)")
            return True
        else:
            print("❌ Windows build failed - no output file created")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Windows build failed: {e}")
        return False
    finally:
        # Clean up temporary spec file
        if spec_file and os.path.exists(spec_file):
            os.remove(spec_file)

def build_linux():
    """Build Linux executable"""
    print("🐧 Building Linux Executable...")
    
    spec_file = create_linux_spec()
    
    try:
        result = subprocess.run([
            "pyinstaller", "--clean", "--noconfirm", spec_file
        ], check=True, capture_output=True, text=True)
        
        if os.path.exists("dist/PASS-FAIL-Hash-Verifier"):
            file_size = os.path.getsize("dist/PASS-FAIL-Hash-Verifier")
            size_mb = file_size / (1024 * 1024)
            print("✅ Linux build completed successfully!")
            print(f"📂 Output: dist/PASS-FAIL-Hash-Verifier ({size_mb:.1f} MB)")
            print(f"📁 Icons available in: icons/linux_icons/")
            return True
        else:
            print("❌ Linux build failed - no output file created")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Linux build failed: {e}")
        return False
    finally:
        # Clean up temporary spec file
        if spec_file and os.path.exists(spec_file):
            os.remove(spec_file)

def main():
    """Main build function"""
    # Parse command line arguments
    target_platform = "macos"  # default
    if len(sys.argv) > 1:
        target_platform = sys.argv[1].lower()
    
    print("🚀 Cross-Platform Build Script")
    print("=" * 50)
    print(f"🎯 Target platform: {target_platform}")
    print(f"💻 Running on: {sys_platform.system()}")
    print()
    
    # Check if PyInstaller is available
    try:
        subprocess.run(["pyinstaller", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: PyInstaller not found.")
        print("Install it with: pip install pyinstaller")
        return
    
    # Clean previous builds
    clean_previous_builds()
    print()
    
    success_count = 0
    
    if target_platform == "all":
        # Build all platforms
        platforms = [("macos", build_macos), ("windows", build_windows), ("linux", build_linux)]
        for platform_name, build_func in platforms:
            print(f"Building {platform_name}...")
            if build_func():
                success_count += 1
            print()
    else:
        # Build specific platform
        if target_platform == "macos":
            if build_macos():
                success_count = 1
        elif target_platform == "windows":
            if build_windows():
                success_count = 1
        elif target_platform == "linux":
            if build_linux():
                success_count = 1
        else:
            print(f"❌ Unknown platform: {target_platform}")
            print("Available platforms: macos, windows, linux, all")
            return
    
    # Summary
    print("=" * 50)
    if target_platform == "all":
        print(f"🎉 Build completed: {success_count}/3 platforms successful")
    else:
        if success_count > 0:
            print("🎉 Build completed successfully!")
            print()
            print("🔧 Icon improvements:")
            print("  • macOS icon is now properly sized (won't appear too large)")
            print("  • Windows icon includes multiple embedded sizes")
            print("  • Linux icons available in standard sizes")
        else:
            print("❌ Build failed. Check the error messages above.")
    
    print()
    print("📋 Next steps:")
    print("  • Test the application on target platform(s)")
    print("  • Verify icon sizes look correct")
    print("  • Package for distribution")

if __name__ == "__main__":
    main()
