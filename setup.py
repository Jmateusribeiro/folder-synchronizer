"""
    setup file
"""
from setuptools import setup, find_packages

with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='folder_synchronizer',
    version='0.0.1',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'folder_synchronizer = folder_synchronizer.__main__:__main__',
        ],
    },
    author='Jorge Ribeiro',
    author_email='mateusribeirojorge@gmail.com',
    description='Package Python to synchronize two folders',
    url='https://github.com/Jmateusribeiro/folder-synchronizer',
)
