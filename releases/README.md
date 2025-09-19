
# Releases

Download pre-built applications for macOS and Linux from this folder.

> **📱 macOS Users:** You will see a "damaged app" error when first running the downloaded app. This is normal! Simply run `xattr -c PASS-FAIL-Hash-Verifier.app` in Terminal to fix it. See [macOS Security Guide](MACOS_SECURITY_GUIDE.md) for details.

## Latest Releases

- **macOS:** `PASS-FAIL-Hash-Verifier-macOS-v1.1.1.zip` (Clean build, no quarantine issues)
- **Linux:** `PASS-FAIL-Hash-Verifier-Linux-v1.1.0.tar.gz`

## How to Use

- **macOS:** Unzip, then double-click the `.app` file. For security issues, see [macOS Security Guide](MACOS_SECURITY_GUIDE.md).
- **Linux:** Extract the `.tar.gz`, make the file executable, and run it:
  ```bash
  tar -xzf PASS-FAIL-Hash-Verifier-Linux-v1.1.0.tar.gz
  chmod +x PASS-FAIL-Hash-Verifier
  ./PASS-FAIL-Hash-Verifier
  ```

## macOS Security Notice

**Expected Behavior:** When you download and try to open the macOS app, you will see a "damaged app" error. This is normal macOS security behavior for unsigned applications.

**Quick Fix:** Run this command in Terminal after downloading:
```bash
cd ~/Downloads && xattr -c PASS-FAIL-Hash-Verifier.app
```

For detailed solutions, see our [macOS Security Guide](MACOS_SECURITY_GUIDE.md).

No installation required. All dependencies are included in the executables.