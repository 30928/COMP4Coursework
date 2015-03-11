from cx_Freeze import setup, Executable

setup(name='Perfect Publishers Database System',
      version='0.1',
      description='*',
      executables = [Executable("LoginDB.py")])
