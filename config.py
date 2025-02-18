"""
This file contains the configuration for the pipeline.
"""

import os


def create_run_file() -> None:
    """
    Create a run_prizma_to_brapa.bat file in the same directory as the current
    file. This file will execute the main.py script in the same directory
    using the python installed in the virtual environment.

    The file will be created in the same directory as this file, and will
    contain the following commands:

    @echo off
    cd <current directory>
    <current directory>\.venv\Scripts\python.exe <current directory>\main.py
    """

    actual_folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(actual_folder, 'run_prizma_to_brapa.bat'), 'w', encoding='utf-8') as f:
        f.write('@echo off\n')
        f.write(f'cd "{actual_folder}"\n')
        f.write(
            f'"{actual_folder}\\.venv\\Scripts\\python.exe" "{actual_folder}\\main.py\n"pause')


if __name__ == '__main__':
    create_run_file()
