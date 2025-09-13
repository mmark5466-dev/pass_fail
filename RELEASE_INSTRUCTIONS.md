# GitHub Release Instructions

## Creating a GitHub Release

1. **Go to your GitHub repository**: https://github.com/mmark5466-dev/pass_fail

2. **Navigate to Releases**:
   - Click on "Releases" in the right sidebar (or go to `/releases`)
   - Click "Create a new release"

3. **Release Details**:
   - **Tag version**: `v1.0.0`
   - **Release title**: `PASS:FAIL Hash Verifier v1.0.0`
   - **Description**:
   ```markdown
   ## PASS:FAIL Hash Verifier v1.0.0
   
   Cross-platform hash verification and cracking tool with graphical interface.
   
   ### Features
   - Hash verification (MD5, SHA1, SHA256, SHA512)
   - Hash cracking with wordlist support
   - User-friendly GUI built with tkinter
   - Cross-platform compatibility
   
   ### Downloads
   - **macOS**: Compatible with Intel and Apple Silicon Macs (macOS 10.14+)
   - **Linux**: x86_64 executable (Ubuntu 18.04+ or equivalent)
   
   ### Installation
   - **macOS**: Download, unzip, and double-click the `.app` file
   - **Linux**: Download, extract, make executable, and run
   
   No additional dependencies required - everything is bundled!
   ```

4. **Upload Files**:
   - Drag and drop or browse to upload:
     - `releases/PASS-FAIL-Hash-Verifier-macOS-v1.0.0.zip`
     - `releases/PASS-FAIL-Hash-Verifier-Linux-v1.0.0.tar.gz`

5. **Publish**:
   - Check "Set as the latest release"
   - Click "Publish release"

## File Locations
The release files are ready in the `releases/` directory:

- `PASS-FAIL-Hash-Verifier-macOS-v1.0.0.zip` (67MB)
- `PASS-FAIL-Hash-Verifier-Linux-v1.0.0.tar.gz` (22MB)
- `README.md` (instructions for users)

## Next Steps
After creating the release:
1. Update the main README.md to direct users to the Releases page
2. Consider adding installation verification steps
3. Set up automated release builds for future versions