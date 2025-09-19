# macOS Security Guide for PASS-FAIL Hash Verifier

## About macOS Gatekeeper

macOS includes a security feature called **Gatekeeper** that automatically quarantines any application downloaded from the internet. This is a normal security measure to protect your system.

## If You See "App is Damaged" Error

When you download the app from GitHub and try to open it, you will likely see a message like:
> "PASS-FAIL-Hash-Verifier" is damaged and can't be opened.

**This is expected behavior** - it doesn't mean the app is actually damaged. macOS automatically adds quarantine flags to ALL downloaded files, and since this app is not code-signed with an Apple Developer certificate, Gatekeeper blocks it as a precaution.

## Solution Options

### Option 1: Remove Quarantine Attributes (Recommended & Fastest)
This is the most reliable method and what you experienced working:

1. Open **Terminal** (found in Applications > Utilities)
2. Navigate to your Downloads folder:
   ```bash
   cd ~/Downloads
   ```
3. Remove quarantine attributes from the downloaded zip file:
   ```bash
   xattr -d com.apple.quarantine PASS-FAIL-Hash-Verifier-macOS-v*.zip
   ```
4. **Alternative:** If you've already extracted the app, you can remove quarantine from the app directly:
   ```bash
   xattr -c PASS-FAIL-Hash-Verifier.app
   ```
5. Extract the app (if you used the first command) and it should run normally

### Option 2: Allow in System Preferences
1. Try to open the app (you'll get the error)
2. Go to **System Preferences** > **Security & Privacy** (or **System Settings** > **Privacy & Security** on newer macOS)
3. In the **General** tab, you should see a message about the blocked app
4. Click **"Open Anyway"**

### Option 3: Right-Click to Open
1. Right-click (or Control+click) on the app
2. Select **"Open"** from the context menu
3. Click **"Open"** when asked to confirm
4. This may need to be done twice - once for the initial warning, then again to actually open

## Why This Happens

This application is not code-signed with an Apple Developer certificate, which requires a paid Apple Developer account ($99/year). The app is completely safe to use - it's built from open source code that you can inspect on GitHub.

**Important:** Even though we create "clean" builds, macOS will ALWAYS add quarantine attributes to any file downloaded from the internet. This is why you'll see the error initially, but the `xattr` command fixes it immediately.

## Quick Reference Commands

```bash
# Remove quarantine from downloaded zip (before extracting)
xattr -d com.apple.quarantine PASS-FAIL-Hash-Verifier-macOS-v*.zip

# Remove all attributes from extracted app (what worked for you)
xattr -c PASS-FAIL-Hash-Verifier.app

# Check what attributes a file has
xattr -l filename
```

## Version History

- **v1.1.1**: Clean build - but macOS still adds quarantine when downloaded
- **v1.1.0**: Original release

## Need Help?

If you continue to have issues, please:
1. Check that you're using the latest version (v1.1.1 or newer)
2. Verify you've extracted the app from the zip file
3. Try the quarantine removal method above

For technical support, please open an issue on our GitHub repository.