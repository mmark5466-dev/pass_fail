# PASS // FAIL - Hash Verification Tool

🎨 **Beautiful hash verification tool with animated progress display**

An intuitive, visual GUI application for testing password security through hash verification. Watch a delightful stick figure animation as your hashes are checked against password dictionaries!

## ✨ What Makes This Special

- 🎨 **Gorgeous Purple Theme** - Professional, modern interface design
- 🏃‍♂️ **Animated Progress** - Stick figure carries a key to unlock a padlock (no boring progress bars!)
- 🎉 **Celebration Animation** - Lock opens and pulses when verification completes
- 📂 **Easy File Handling** - Drag & drop support for both hashes and wordlists
- 💬 **Live Updates** - Real-time terminal output shows exactly what's happening
- 🧵 **Smooth Performance** - Background processing keeps the interface responsive
- ⌨️ **Keyboard Shortcuts** - Press Enter to start/stop verification
- 🖥️ **Cross-Platform** - Works on macOS, Windows, and Linux

## � Download & Install

### 🚀 **Ready-to-Use Applications** (Recommended)
Head to our **[Releases](../../releases)** page to download pre-built applications:

- **macOS**: Download the `.zip` file, extract, and double-click the `.app`
- **Linux**: Download the `.tar.gz` file, extract, and run the executable
- **Windows**: Download the `.exe` file and run

*No installation required - just download and run!*

## 🛠️ Development Setup

### Quick Start
```bash
# Clone the repository
git clone https://github.com/mmark5466-dev/pass_fail.git
cd pass_fail

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

### Build Your Own
```bash
# Build for your current platform
python build_cross_platform.py

# Build for specific platform
python build_cross_platform.py macos     # macOS .app bundle
python build_cross_platform.py windows   # Windows .exe
python build_cross_platform.py linux     # Linux executable
python build_cross_platform.py all       # All platforms
```

## 📁 Project Structure

**Clean and focused structure:**

```
pass_fail_gui/
├── README.md                      # 📖 You are here!
├── requirements.txt               # 📦 Python dependencies
├── BUILD.md                       # 🔧 Build instructions
├── ICONS.md                       # 🎨 Icon documentation
│
├── build_cross_platform.py        # 🚀 MAIN BUILD SCRIPT
├── build_app.py                   # 🔧 Legacy build script
├── create_cross_platform_icons.py # 🎨 Icon creator
│
├── app_icon.icns                  # 🍎 macOS app icon
├── app_icon.ico                   # 🪟 Windows app icon  
├── linux_icons/                   # 🐧 Linux icon variants
│
├── src/                           # 💾 Core application
│   ├── main.py                    # 🚀 App launcher
│   ├── gui.py                     # 🎨 Interface & animations
│   ├── hash_verifier.py           # 🔍 Verification logic
│   ├── images/                    # 🖼️ Interface graphics
│   └── wordlists/                 # 📋 Password dictionaries
│
├── build/                         # 🔧 Build cache (auto-generated)
└── dist/                          # 📦 Final executables (auto-generated)
```

**New to coding?** Start by reading `src/main.py` - it's short and well-commented!

## 🎯 How to Use the App

**First time using a hash verification tool? Follow these simple steps:**

### Step 1: Enter Your Hash
- **Type directly**: Paste a hash into the input field
- **Browse files**: Click anywhere in the field, then double-click to select a file
- **Drag & drop**: Simply drag a text file containing hashes onto the input area

### Step 2: Choose Password Lists
- **Select wordlists**: Click on one or more password dictionaries in the left panel
- **Import your own**: Use the "+ Import Wordlist" button or drag files to the wordlist area
- **Multiple selection**: Hold Ctrl (Windows/Linux) or Cmd (Mac) to select multiple lists

### Step 3: Start the Magic
- **Click "Start"**: Watch the stick figure spring into action!
- **Observe progress**: The figure runs toward the lock as verification progresses
- **Read updates**: The terminal shows real-time status and results

### Step 4: Interpret Results
- **🟢 Match found**: Password was cracked (time to change it!)
- **🔴 No match**: Your password doesn't appear in common lists (good!)
- **🎉 Celebration**: When complete, the lock opens with a victory animation

## 💻 Technical Requirements

**What you need to run this application:**

### Required Software
- **Python 3.10 or newer** - Download from [python.org](https://python.org)
- **Tkinter support** - Usually included with Python automatically

### Operating System Support
- ✅ **Windows** - Works great on all recent versions
- ✅ **macOS** - Best with Python from python.org (includes Tkinter)
- ✅ **Linux** - May need to install: `sudo apt-get install python3-tk`

### Dependencies
The app uses only Python's built-in libraries, making it lightweight and easy to run. The `requirements.txt` file is minimal and mainly for development tools.

**Having trouble with Tkinter?**
- On macOS, Python from python.org includes Tkinter automatically
- On Linux, install the python3-tk package
- On Windows, it's usually included by default

## 📋 Working with Wordlists

**Password dictionaries are the heart of this tool!**

### Built-in Wordlists
- **`password.txt`** - 821KB of common passwords
- **`directory-list-2.3-medium.txt`** - 2MB of web directory names  
- **`common_passwords.txt`** - Top 100 most common passwords
- **`admin_passwords.txt`** - Common admin/system passwords

### Adding Your Own Wordlists
1. **Easy method**: Click the "+ Import Wordlist" button
2. **Drag & drop**: Drop any `.txt` file onto the wordlist area
3. **Manual method**: Place files directly in the `src/wordlists/` folder
4. **Restart**: New wordlists appear automatically when you restart the app

### File Format
Wordlists should be plain text files with one password per line:
```
password123
admin
qwerty
letmein
```

**💡 Pro Tip**: The more wordlists you select, the more comprehensive your password testing will be!

## 🎨 Customization for Developers

**Want to modify the app? Here's where to look:**

### Animation Customization
- **Animation class**: `StickFigureKeyLockProgress` in `gui.py`
- **Default behavior**: No visible progress bar (just the stick figure animation)
- **Show progress bar**: Create widget with `show_track=True` parameter
- **Timing**: Adjust animation speed in the `_schedule()` method

### Theme and Colors  
- **Color palette**: Look for the `colors` dictionary in `HashVerifierGUI.__init__`
- **Purple theme**: All colors are defined in hex format for easy modification
- **Button styles**: Custom ttk styles for Purple.TButton and Muted.TButton
- **Scrollbars**: Custom Purple.Vertical.TScrollbar styling

### Adding Features
- **New hash algorithms**: Extend the detection logic in `hash_verifier.py`
- **UI improvements**: Modify layout and widgets in `gui.py`
- **Animation themes**: Create new animation classes based on StickFigureKeyLockProgress

**The code is extensively commented to help you understand each component!**

## 🐛 Troubleshooting

**Running into issues? Here are the most common solutions:**

### "No module named _tkinter" Error
- **macOS**: Download Python from [python.org](https://python.org) - it includes Tkinter
- **Linux**: Install with `sudo apt-get install python3-tk`
- **Windows**: Usually works automatically, try reinstalling Python

### App Feels Slow or Sluggish
- **Normal behavior**: Large wordlists can take time to process
- **Built-in optimization**: The app already throttles UI refreshes for smooth performance
- **Tip**: Start with smaller wordlists to test, then move to larger ones

### Interface Issues
- **Widgets not appearing**: Check that Python includes Tkinter support
- **Images missing**: Verify `src/images/image01.png` exists
- **Animation not working**: Ensure you have a working graphics environment

### File Problems
- **Wordlists not loading**: Check that files are plain text (.txt) format
- **Hash files not importing**: Verify file contains valid hash values
- **Permission errors**: Make sure you can read/write in the project directory

**Still having trouble?** Check the main project README for more detailed troubleshooting steps!

## 📄 License

This project is licensed under the MIT License. Feel free to use, modify, and share!

---

**🎓 Perfect for Learning**: This application is designed to be educational and beginner-friendly. Every component is documented to help you understand both cybersecurity concepts and GUI development in Python.

**🔗 Part of the PASS // FAIL Project**: See the main project README for complete setup instructions and educational resources.