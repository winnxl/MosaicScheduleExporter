# -*- mode: python -*-

block_cipher = None


a = Analysis(['guiClient.py'],
             pathex=['C:\\Users\\Michelle\\Documents\\M3\\Year 3\\3XA3\\Source\\proj_3xa3\\proj_3xa3\\spiders'],
             binaries=[],
             datas=[('C:\\Users\\Michelle\\Anaconda3\\Lib\\site-packages\\lxml\\*.h', '.')],
             hiddenimports=[],
             hookspath=['.\\hooks\\'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='guiClient',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
