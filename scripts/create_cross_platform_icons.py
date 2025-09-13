#!/usr/bin/env python3
"""
Cross-Platform App Icon Creator

This script creates properly sized app icons for macOS, Windows, and Linux
from any input image (PNG, JPG, etc.).

Usage:
    python scripts/create_cross_platform_icons.py input_image.png

Features:
- Creates macOS ICNS with proper rounded corners and standard sizes
- Creates Windows ICO with multiple embedded sizes
- Creates Linux PNG icons in standard sizes
- Follows platform-specific design guidelines
- Optimizes file sizes for app distribution

The script follows each platform's Human Interface Guidelines for app icons.
"""

import sys
import os
import subprocess
import platform as sys_platform
from PIL import Image, ImageDraw

def create_rounded_icon(input_path, output_path, size, apply_rounding=True):
    """
    Create a rounded corner version of an image at the specified size.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path where the output image should be saved
        size (int): Size in pixels (width and height, square)
        apply_rounding (bool): Whether to apply rounded corners (for macOS)
    """
    try:
        # Open and resize image with high-quality resampling
        img = Image.open(input_path).convert("RGBA")
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        
        if apply_rounding:
            # Calculate corner radius for macOS (18% of icon size for better scaling)
            # Reduced from 22.37% to better match standard macOS app icons
            radius = int(size * 0.18)
            
            # Create a mask for rounded corners
            mask = Image.new("L", (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, size, size), radius=radius, fill=255)
            
            # Apply the mask to create rounded corners
            result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            result.paste(img, (0, 0))
            result.putalpha(mask)
        else:
            # No rounding for Windows/Linux
            result = img
        
        # Save the result
        result.save(output_path, "PNG")
        return True
        
    except Exception as e:
        print(f"❌ Error creating {output_path}: {e}")
        return False

def create_macos_icons(input_image_path):
    """
    Create macOS ICNS file with proper sizing and rounded corners.
    
    Args:
        input_image_path (str): Path to the input image file
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("🍎 Creating macOS ICNS icon...")
    
    # Create iconset directory
    iconset_dir = "icons/app_icon.iconset"
    if os.path.exists(iconset_dir):
        subprocess.run(["rm", "-rf", iconset_dir], check=True)
    os.makedirs(iconset_dir)
    
    # Optimized icon sizes for macOS - reduced maximum size to 512px
    # This prevents the icon from appearing too large compared to system apps
    icon_sizes = [
        (16, "icon_16x16.png"),
        (32, "icon_16x16@2x.png"),
        (32, "icon_32x32.png"), 
        (64, "icon_32x32@2x.png"),
        (128, "icon_128x128.png"),
        (256, "icon_128x128@2x.png"),
        (256, "icon_256x256.png"),
        (512, "icon_256x256@2x.png"),
        (512, "icon_512x512.png")
        # Removed 1024px version to match standard app icon sizes
    ]
    
    # Create each icon size with rounded corners
    success_count = 0
    for size, filename in icon_sizes:
        output_path = os.path.join(iconset_dir, filename)
        print(f"  📐 Creating {filename} ({size}x{size}) with rounded corners")
        
        if create_rounded_icon(input_image_path, output_path, size, apply_rounding=True):
            success_count += 1
    
    # Convert iconset to ICNS format (only on macOS)
    if sys_platform.system() == "Darwin":
        print("🔧 Converting to ICNS format...")
        try:
            subprocess.run(["iconutil", "-c", "icns", iconset_dir], check=True)
            
            if os.path.exists("icons/app_icon.icns"):
                file_size = os.path.getsize("icons/app_icon.icns")
                size_kb = file_size / 1024
                print(f"✅ macOS ICNS created: icons/app_icon.icns ({size_kb:.0f} KB)")
                
                # Clean up iconset directory
                subprocess.run(["rm", "-rf", iconset_dir], check=True)
                return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating ICNS: {e}")
            return False
    else:
        print("⚠️  ICNS creation skipped (requires macOS)")
        # Keep the iconset for manual conversion
        print(f"📁 Icon files available in: {iconset_dir}/")
        return True
    
    return False

def create_windows_ico(input_image_path):
    """
    Create Windows ICO file with multiple embedded sizes.
    
    Args:
        input_image_path (str): Path to the input image file
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("🪟 Creating Windows ICO icon...")
    
    # Windows ICO standard sizes
    ico_sizes = [16, 32, 48, 64, 128, 256]
    
    try:
        # Create temporary PNG files for each size
        temp_files = []
        for size in ico_sizes:
            temp_path = f"temp_icon_{size}.png"
            print(f"  📐 Creating {size}x{size} (no rounded corners)")
            
            if create_rounded_icon(input_image_path, temp_path, size, apply_rounding=False):
                temp_files.append(temp_path)
        
        # Create ICO file with multiple sizes
        if temp_files:
            images = []
            for temp_file in temp_files:
                img = Image.open(temp_file)
                images.append(img)
            
            # Save as ICO with all sizes
            images[0].save("icons/app_icon.ico", format="ICO", 
                          sizes=[(img.width, img.height) for img in images])
            
            file_size = os.path.getsize("icons/app_icon.ico")
            size_kb = file_size / 1024
            print(f"✅ Windows ICO created: icons/app_icon.ico ({size_kb:.0f} KB)")
            
            # Clean up temporary files
            for temp_file in temp_files:
                os.remove(temp_file)
            
            return True
        
    except Exception as e:
        print(f"❌ Error creating Windows ICO: {e}")
        # Clean up any temporary files
        for size in ico_sizes:
            temp_path = f"temp_icon_{size}.png"
            if os.path.exists(temp_path):
                os.remove(temp_path)
        return False
    
    return False

def create_linux_icons(input_image_path):
    """
    Create Linux PNG icons in standard sizes.
    
    Args:
        input_image_path (str): Path to the input image file
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("🐧 Creating Linux PNG icons...")
    
    # Create icons/linux_icons directory
    linux_dir = "icons/linux_icons"
    if os.path.exists(linux_dir):
        subprocess.run(["rm", "-rf", linux_dir], check=True)
    os.makedirs(linux_dir)
    
    # Linux standard icon sizes
    linux_sizes = [16, 22, 24, 32, 48, 64, 96, 128, 192, 256, 512]
    
    success_count = 0
    for size in linux_sizes:
        output_path = os.path.join(linux_dir, f"app_icon_{size}x{size}.png")
        print(f"  📐 Creating {size}x{size} (square corners)")
        
        if create_rounded_icon(input_image_path, output_path, size, apply_rounding=False):
            success_count += 1
    
    if success_count == len(linux_sizes):
        print(f"✅ Linux icons created: {linux_dir}/ ({success_count} sizes)")
        return True
    else:
        print(f"⚠️  Linux icons: {success_count}/{len(linux_sizes)} created successfully")
        return False

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("🎨 Cross-Platform App Icon Creator")
        print("=" * 40)
        print("Usage: python scripts/create_cross_platform_icons.py <input_image>")
        print("")
        print("This script creates app icons for:")
        print("  🍎 macOS: .icns with rounded corners (optimized size)")
        print("  🪟 Windows: .ico with multiple embedded sizes")
        print("  🐧 Linux: .png files in standard sizes")
        print("")
        print("Example:")
        print("  python scripts/create_cross_platform_icons.py src/images/image02.png")
        return
    
    input_image = sys.argv[1]
    
    if not os.path.exists(input_image):
        print(f"❌ Error: Input image '{input_image}' not found.")
        return
    
    print("🚀 Cross-Platform App Icon Creator")
    print("=" * 50)
    print(f"📸 Source image: {input_image}")
    print(f"💻 Running on: {sys_platform.system()}")
    print()
    
    # Ensure icons directory exists
    os.makedirs("icons", exist_ok=True)
    
    # Check if PIL is available
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("❌ Error: PIL (Pillow) is required.")
        print("Install it with: pip install Pillow")
        return
    
    success_count = 0
    total_formats = 3
    
    # Create icons for all platforms
    if create_macos_icons(input_image):
        success_count += 1
    
    if create_windows_ico(input_image):
        success_count += 1
        
    if create_linux_icons(input_image):
        success_count += 1
    
    print()
    print("=" * 50)
    if success_count == total_formats:
        print("🎉 All platform icons created successfully!")
        print()
        print("📁 Generated files:")
        print("  🍎 icons/app_icon.icns - macOS (smaller, properly sized)")
        print("  🪟 app_icon.ico - Windows")  
        print("  🐧 linux_icons/ - Linux PNG files")
        print()
        print("🔧 Next steps:")
        print("  • Rebuild your app to use the new smaller macOS icon")
        print("  • Use app_icon.ico for Windows builds")
        print("  • Use linux_icons/ files for Linux packaging")
    else:
        print(f"⚠️  Completed: {success_count}/{total_formats} platform icons created")
        print("Check the error messages above for details.")

if __name__ == "__main__":
    main()
