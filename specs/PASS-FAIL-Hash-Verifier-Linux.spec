# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

# Collect all data and imports
datas = []
binaries = []
hiddenimports = []

# PIL/Pillow support
tmp_ret = collect_all('PIL')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# tkinterdnd2 support
tmp_ret = collect_all('tkinterdnd2')
datas += tmp_ret[0] 
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# Add explicit hidden imports
hiddenimports += [
    'PIL._imaging', 'PIL.Image', 'PIL.ImageTk', 'tkinterdnd2',
    'tkinter', 'tkinter.messagebox', 'tkinter.filedialog', 'tkinter.ttk',
    'hashlib', 'threading', 'os', 'sys', 'time', 'math', 'collections', 'platform',
]

# Add data files
datas += [('src/images', 'images'), ('src/wordlists', 'wordlists')]

a = Analysis(['src/main.py'], pathex=[], binaries=binaries, datas=datas,
             hiddenimports=hiddenimports, hookspath=[], hooksconfig={},
             runtime_hooks=[], excludes=[], noarchive=False, optimize=0)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name='PASS-FAIL-Hash-Verifier',
          debug=False, bootloader_ignore_signals=False, strip=False, upx=True,
          runtime_tmpdir=None, console=False, disable_windowed_traceback=False,
          argv_emulation=False, target_arch=None, codesign_identity=None,
          entitlements_file=None)
