# Cross-Platform App Icons

This directory contains optimized app icons for all supported platforms.

## 🎯 Icon Improvements

### Before
- ❌ macOS icon was too large (2.6 MB, 1024px max)
- ❌ No Windows or Linux icon support
- ❌ Single platform only

### After  
- ✅ macOS icon properly sized (857 KB, 512px max)
- ✅ Windows ICO with embedded multi-sizes
- ✅ Linux PNG icons in all standard sizes
- ✅ Platform-appropriate styling

## 📁 Generated Files

### macOS
- `app_icon.icns` - Native macOS icon bundle with rounded corners
- Sizes: 16×16, 32×32, 64×64, 128×128, 256×256, 512×512 (with @2x versions)
- Rounded corners: 18% radius for native macOS appearance

### Windows
- `app_icon.ico` - Multi-size ICO file with embedded icons
- Sizes: 16×16, 32×32, 48×48, 64×64, 128×128, 256×256
- Square corners following Windows design guidelines

### Linux
- `linux_icons/` directory with PNG files
- Sizes: 16, 22, 24, 32, 48, 64, 96, 128, 192, 256, 512 pixels
- Compatible with all major desktop environments
- Follows freedesktop.org specifications

## 🔧 Usage

### Building for Specific Platforms

```bash
# Build for macOS (uses app_icon.icns)
python build_cross_platform.py macos

# Build for Windows (uses app_icon.ico)
python build_cross_platform.py windows

# Build for Linux (includes linux_icons/ directory)
python build_cross_platform.py linux

# Build for all platforms
python build_cross_platform.py all
```

### Regenerating Icons

If you want to update the source image or create icons from a different image:

```bash
# Create all platform icons from source image
python create_cross_platform_icons.py src/images/image02.png
```

## 📊 File Sizes

| Platform | File | Size |
|----------|------|------|
| macOS | app_icon.icns | 857 KB |
| Windows | app_icon.ico | 574 bytes |
| Linux | linux_icons/ (all sizes) | ~360 KB total |

## ✨ Key Benefits

1. **Proper Scaling**: macOS icon no longer appears oversized compared to system apps
2. **Native Appearance**: Each platform uses appropriate styling (rounded vs square corners)
3. **Optimized Sizes**: Smaller file sizes without quality loss
4. **Universal Support**: Single build process creates icons for all platforms
5. **High Resolution**: Retina/HiDPI support for all platforms

## 🎨 Design Details

### macOS
- Rounded corners with 18% radius (reduced from 22.37% for better scaling)
- Maximum size reduced from 1024px to 512px
- Follows Apple Human Interface Guidelines

### Windows
- Square corners (Windows design standard)
- Multiple embedded sizes in single ICO file
- Optimized for taskbar and file explorer display

### Linux
- Full range of standard desktop icon sizes
- PNG format for maximum compatibility
- Suitable for all major desktop environments (GNOME, KDE, XFCE, etc.)
