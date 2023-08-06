from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'Translating a sympy expression to its latex equivalent.'
LONG_DESCRIPTION = 'Translating a sympy expression to its latex equivalent'

# Setting up
setup(
    name="latexconverter",
    version=VERSION,
    author="Dariokula",
    author_email="<dario.kulaszewski@web.de>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'latex', 'sympy', 'sockets'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
