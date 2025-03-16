from cx_Freeze import setup, Executable

build_options = {
    'packages': ['strings_with_arrows.py'],
    'excludes': ['setup.py','Dustc.py','Dust.py']
}

setup(
    name="Bov",
    version='4.0.0',
    description='Bov Interpreter',
    options={'build_exe': build_options},
    executables=[Executable('Bov.py')]
)
