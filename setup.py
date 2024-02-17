from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='folder_synchronizer',
    version='0.0.1',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'folder_synchronizer = folder_synchronizer.__main__:main',
        ],
    },
    author='Jorge Ribeiro',
    author_email='mateusribeirojorge@gmail.com',
    description='Package Python to synchronize two folders',
    url='https://github.com/Jmateusribeiro/folder-synchronizer',
)