# -*- mode: python ; coding: utf-8 -*-
# vi: ft=python


from argparse import ArgumentParser
import sys
from PyInstaller.building.api import COLLECT, EXE, PYZ
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.osx import BUNDLE


parser = ArgumentParser()
parser.add_argument('--portable', action='store_true')
options = parser.parse_args()


name = 'DonkeyDoc' if sys.platform == 'win32' else 'donkeydoc'
icon = None
if sys.platform == 'win32':
    icon = 'docs/logo.ico'
elif sys.platform == 'darwin':
    icon = 'docs/logo.icns'


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('docs', './docs'), ('app', './app'), ('lib', './lib')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    excludes=[],
    runtime_hooks=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

include = [a.scripts]
if options.portable:
    include += (a.binaries, a.datas)
exe = EXE(
    pyz,
    *include,
    [],
    bootloader_ignore_signals=False,
    console=False,
    hide_console='hide-early',
    disable_windowed_traceback=False,
    debug=False,
    name=name,
    exclude_binaries=not options.portable,
    icon=icon,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None
)

coll = None if options.portable else COLLECT(
    exe,
    a.binaries,
    a.datas,
    name=name,
    strip=False,
    upx=True,
    upx_exclude=[],
)

app = BUNDLE(
    exe if coll is None else coll,
    name='DonkeyDoc.app',
    icon=icon,
    bundle_identifier='com.github.donkeydocdev',
    version='0.0.0',
    info_plist={
        'NSAppleScriptEnabled': False,
        'NSPrincipalClass': 'NSApplication',
    }
)