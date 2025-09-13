# Building PASS // FAIL Hash Verifier

This guide explains how to compile the PASS // FAIL Hash Verifier into a standalone executable that can run without Python installed.

## Quick Build

### Option 1: Using the Build Script (Recommended)
```bash
# Make sure you're in the pass_fail_gui directory
cd pass_fail_gui

# Run the build script
python build_app.py
```

### Option 2: Manual Build

#### macOS (Creates .app bundle)
```bash
python -m PyInstaller --onedir --windowed \
  --add-data "src/images:images" \
  --add-data "src/wordlists:wordlists" \
  --name "PASS-FAIL-Hash-Verifier" \
  --clean --noconfirm src/main.py
```

#### Windows (Creates .exe file)
```bash
python -m PyInstaller --onefile --windowed ^
  --add-data "src/images;images" ^
  --add-data "src/wordlists;wordlists" ^
  --name "PASS-FAIL-Hash-Verifier" ^
  --clean --noconfirm src/main.py
```

#### Linux (Creates executable file)
```bash
python -m PyInstaller --onefile \
  --add-data "src/images:images" \
  --add-data "src/wordlists:wordlists" \
  --name "PASS-FAIL-Hash-Verifier" \
  --clean --noconfirm src/main.py
```

## Prerequisites

1. **Python Environment**: Make sure your virtual environment is activated
2. **PyInstaller**: Will be auto-installed by the build script, or install manually:
   ```bash
   pip install pyinstaller
   ```

## Output Files

After building, you'll find the executable in the `dist/` folder:

### macOS
- **File**: `dist/PASS-FAIL-Hash-Verifier.app/`
- **Type**: Application bundle (folder that looks like a single app)
- **Usage**: Double-click to run, or drag to Applications folder
- **Sharing**: Zip the entire .app folder to share

### Windows  
- **File**: `dist/PASS-FAIL-Hash-Verifier.exe`
- **Type**: Single executable file
- **Usage**: Double-click to run
- **Sharing**: Just share the .exe file (no other files needed)

### Linux
- **File**: `dist/PASS-FAIL-Hash-Verifier`
- **Type**: Executable file
- **Usage**: `./PASS-FAIL-Hash-Verifier` or double-click in file manager
- **Sharing**: Just share the executable file

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Make sure all dependencies are installed in your virtual environment
   - Try: `pip install -r requirements.txt`

2. **Missing images or wordlists**
   - The `--add-data` flags should include these automatically
   - Verify the `src/images/` and `src/wordlists/` folders exist

3. **App won't start on macOS**
   - macOS may block unsigned apps
   - Right-click → "Open" to bypass security warning
   - Or run: `xattr -dr com.apple.quarantine PASS-FAIL-Hash-Verifier.app`

4. **Large file size**
   - This is normal for PyInstaller builds (includes Python runtime)
   - Typical size: 50-100 MB
   - For smaller size, try `--onedir` instead of `--onefile`

### Build Optimization

For smaller executables:
```bash
# Use onedir mode (creates folder with multiple files)
python -m PyInstaller --onedir --windowed ...

# Exclude unused modules (advanced)
python -m PyInstaller --exclude-module matplotlib --exclude-module numpy ...
```

## Alternative Tools

If PyInstaller doesn't work for your needs:

1. **cx_Freeze** - Cross-platform alternative
2. **Nuitka** - Compiles to native code (faster execution)
3. **auto-py-to-exe** - GUI wrapper for PyInstaller

## Performance Notes

- **Startup**: First launch may be slower (cold start)
- **Size**: Includes entire Python runtime (~50-100 MB)
- **Speed**: Runtime performance same as normal Python
- **Compatibility**: Works on systems without Python installed

## Distribution

### For End Users
- **macOS**: Distribute the `.app` bundle (zip it first)
- **Windows**: Distribute just the `.exe` file
- **Linux**: Distribute the executable file

### For Developers
- Include source code and this build guide
- Consider providing multiple platform builds
- Test on clean systems without Python installed
