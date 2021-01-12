from cx_Freeze import setup, Executable

setup(name = 'Monopoly_In_Pygame',
      version = '0.1',
      description = 'A functional game of monopoly using pygame module.',
      executables = [Executable('main.py')])