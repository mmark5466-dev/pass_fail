# macOS Security Guide for PASS-FAIL Hash Verifier

## About macOS Gatekeeper

macOS includes a security feature called **Gatekeeper** that may prevent unsigned applications downloaded from the internet from running. This is a normal security measure to protect your system.

## If You See "App is Damaged" Error

If you download the app and see a message like:
> "PASS-FAIL-Hash-Verifier" is damaged and can't be opened.

This doesn't mean the app is actually damaged - it's just macOS being cautious about unsigned applications.

## Solution Options

### Option 1: Remove Quarantine Attributes (Recommended)
1. Open **Terminal** (found in Applications > Utilities)
2. Navigate to your Downloads folder:
   ```bash
   cd ~/Downloads
   ```
3. Remove quarantine attributes from the zip file:
   ```bash
   xattr -d com.apple.quarantine PASS-FAIL-Hash-Verifier-macOS-v*.zip
   ```
4. Extract the app and it should run normally

### Option 2: Allow in System Preferences
1. Try to open the app (you'll get the error)
2. Go to **System Preferences** > **Security & Privacy**
3. In the **General** tab, you should see a message about the blocked app
4. Click **"Open Anyway"**

### Option 3: Right-Click to Open
1. Right-click (or Control+click) on the app
2. Select **"Open"** from the context menu
3. Click **"Open"** when asked to confirm

## Version History

- **v1.1.1**: Clean build without quarantine attributes
- **v1.1.0**: Original release (may trigger Gatekeeper warnings)

## Why This Happens

This application is not code-signed with an Apple Developer certificate, which requires a paid Apple Developer account. The app is completely safe to use - it's built from open source code that you can inspect.

## Need Help?

If you continue to have issues, please:
1. Check that you're using the latest version (v1.1.1 or newer)
2. Verify you've extracted the app from the zip file
3. Try the quarantine removal method above

For technical support, please open an issue on our GitHub repository.