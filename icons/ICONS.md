
# App Icons

This folder contains icons for all supported platforms:

- **macOS:** `app_icon.icns` (16–512px, rounded corners)
- **Windows:** `app_icon.ico` (16–256px, square corners)
- **Linux:** `linux_icons/` (PNG files, 16–512px)

## Usage

Use these icons when building the app for each platform. To regenerate icons from a source image, run:

```bash
python scripts/create_cross_platform_icons.py src/images/image02.png
```

For platform builds, icons are automatically included by the build scripts in `scripts/`.
