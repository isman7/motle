from setuptools import setup
from pathlib import Path

requirements = Path("requirements.txt").read_text().split("\n")

setup(
    name='motle',
    version='0.1.0',
    packages=['motle'],
    url='https://github.com/isman7/motle',
    license='MIT',
    author='Ismael Benito',
    author_email='ismael.benito@pm.me',
    description='motle is a wordle game in catalan',
    package_data={'motle': ['dicts/*.txt']},
    entry_points={
        'console_scripts': [
            'motle = motle:motle_cmd',
        ],
    },
    install_requires=requirements
)
