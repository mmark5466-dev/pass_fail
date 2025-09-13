# Password Wordlists Directory

🔑 **Your collection of password dictionaries for security testing**

This folder contains sample wordlists that help you test whether passwords appear in common password databases. These are the "dictionaries" that the app uses to try and crack hashes!

## 📋 What's Included

**Ready-to-use wordlists:**
- 📄 **`password.txt`** - Common passwords (821KB, ~14,000 entries)
- 🌐 **`directory-list-2.3-medium.txt`** - Web directory names (2MB, ~220,000 entries)  
- 🔟 **`common_passwords.txt`** - Top 100 most common passwords (quick testing)
- 👔 **`admin_passwords.txt`** - Common admin/system passwords (IT-focused)

**Why these lists?** These represent real passwords found in data breaches and commonly used weak passwords. If your password appears in these lists, it's time for a change!

## 📈 Want Bigger, Better Wordlists?

**Ready for more comprehensive password testing?** Here are some popular options:

### 🎯 RockYou Wordlist (140MB)
- **What it is**: Real passwords from the 2009 RockYou data breach  
- **Why it's useful**: Contains 14+ million actual passwords people used
- **Download**: [GitHub - RockYou.txt](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt)
- **How to use**: Download and save as `rockyou.txt` in this folder

### 🛠️ SecLists Collection
- **What it is**: Huge collection of wordlists for security testing
- **Why it's awesome**: Hundreds of specialized password lists  
- **Get it**: [GitHub - SecLists](https://github.com/danielmiessler/SecLists)
- **How to use**: Clone the repo and copy any wordlists you want to this folder

### 🌍 Other Great Sources
- **Weakpass**: [weakpass.com](https://weakpass.com/) - Massive password collections
- **CrackStation**: [crackstation.net](https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm) - Professional-grade wordlists

**⚠️ Size Warning**: Some wordlists are HUGE (multi-gigabyte files). Start small and work your way up!

## ➕ Adding Your Own Wordlists

**Have a custom password list? Here's how to use it:**

### 3 Easy Ways to Add Wordlists

1. **🖱️ Use the GUI** (Easiest!)
   - Click the "+ Import Wordlist" button in the app
   - Select your `.txt` file
   - It automatically copies to this folder

2. **🎯 Drag & Drop** (Super convenient!)
   - Drag your wordlist file directly onto the wordlist area in the app
   - Works with any text file

3. **📁 Manual Method** (For advanced users)
   - Copy your `.txt` file directly into this folder
   - Restart the app to see it in the list

### 📝 Wordlist File Format

**Keep it simple!** Wordlists should be plain text files with one password per line:

```
password123
admin
qwerty
letmein
welcome
12345678
password1
```

**💡 Pro Tips:**
- ✅ Use `.txt` files (not Word documents!)
- ✅ One password per line
- ✅ No extra spaces or formatting needed
- ✅ Any file size works (though larger = longer processing time)

## 💻 Technical Notes

### File Size Considerations
- **Small files** (< 1MB): Load instantly, great for quick tests
- **Medium files** (1-10MB): Good balance of coverage and speed  
- **Large files** (10MB+): Comprehensive but slower processing
- **Huge files** (100MB+): Cannot be uploaded to GitHub due to size limits

### Storage Options for Large Files
- **Local storage**: Keep big wordlists on your computer only
- **Git LFS**: Use Git Large File Storage for version control
- **Cloud storage**: Store and download as needed
- **External drives**: Keep massive collections on USB drives

### Performance Tips
- Start testing with smaller wordlists first
- Use multiple small lists rather than one giant list
- Monitor memory usage with very large files
- Close other applications when processing huge wordlists

---

**🎓 Happy Password Testing!** Use these tools to build stronger, more secure passwords for yourself and help others understand why password security matters.
