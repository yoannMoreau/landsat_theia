# -*- mode: python -*-
a = Analysis(['python/landsat_theia.py'],
             pathex=['/home/ouaf/workspace2/landsat_theia/landsat_theia'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='landsat_theia',
          debug=False,
          strip=None,
          upx=True,
          console=True )
