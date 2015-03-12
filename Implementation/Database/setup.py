from cx_Freeze import setup, Executable

includefiles = ['LoginIcon.png', 'PerfectPublishersLtd.png', 'PPIcon.png']

setup(name='Perfect Publishers Database System',
      version='0.1',
      description='*',
      data_files=includefiles,
      executables = [Executable("LoginDB.py", base='Win32GUI')])

