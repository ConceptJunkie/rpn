# rpn.spec
from PyInstaller.utils.hooks import collect_submodules, collect_data_files, collect_dynamic_libs
block_cipher = None

hiddenimports = collect_submodules('flint')
datas = collect_data_files('flint')
binaries = collect_dynamic_libs('flint')


# ✅ Concatenate the TOC returned by Tree
datas = datas + Tree( 'rpn/rpndata', prefix='rpn/rpndata')

a = Analysis(
    ['rpn.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='rpn',
    debug=False,
    strip=False,
    upx=False,
    console=True,  # set False if you want a GUI-only exe
)
