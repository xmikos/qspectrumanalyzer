#!/usr/bin/env python

import setuptools
from setuptools import setup

from qspectrumanalyzer.version import __version__

setup_cmdclass = {}
setup_entry_points = {
    "gui_scripts": [
        "qspectrumanalyzer=qspectrumanalyzer.__main__:main",
    ],
}

# Allow compilation of Qt .qrc, .ui and .ts files (build_qt command)
try:
    from setup_qt import build_qt
    setup_cmdclass['build_qt'] = build_qt
except ImportError:
    pass

# Allow building frozen executables with PyInstaller / subzero (build_exe command)
try:
    from subzero import setup, Executable
    setup_entry_points = {
        "console_scripts": [
            Executable('qspectrumanalyzer=qspectrumanalyzer.__main__:main',
                       console=True, icon_file='qspectrumanalyzer.ico'),
            Executable('soapy_power=soapypower.__main__:main',
                       console=True),
        ],
    }
except ImportError:
    pass


setup(
    name="QSpectrumAnalyzer",
    version=__version__,
    description=("Spectrum analyzer for multiple SDR platforms "
                 "(PyQtGraph based GUI for soapy_power, hackrf_sweep, rtl_power, rx_power and other backends)"),
    long_description=open('README.rst').read(),
    author="Michal Krenek (Mikos)",
    author_email="m.krenek@gmail.com",
    url="https://github.com/xmikos/qspectrumanalyzer",
    license="GNU GPLv3",
    packages=["qspectrumanalyzer", "qspectrumanalyzer.backends"],
    package_data={
        "qspectrumanalyzer": [
            "qspectrumanalyzer.svg",
            "*.ui",
            "languages/*.qm",
            "languages/*.ts",
        ],
    },
    data_files=[
        ("share/applications", ["qspectrumanalyzer.desktop"]),
        ("share/pixmaps", ["qspectrumanalyzer.png"]),
    ],
    install_requires=[
        "soapy_power>=1.6.0",
        "PyQt6>=6.6.0",
        "pyqtgraph>=0.13.3",
    ],
    options={
        'build_qt': {
            'packages': ['qspectrumanalyzer'],
            'languages': ['cs'],
            'replacement_bindings': 'PyQt6',
        },
        'build_exe': {
            'datas': [
                ('qspectrumanalyzer/qspectrumanalyzer.svg', 'qspectrumanalyzer'),
                ('qspectrumanalyzer/*.ui', 'qspectrumanalyzer'),
                ('qspectrumanalyzer/languages/*.ts', 'qspectrumanalyzer/languages'),
                ('qspectrumanalyzer/languages/*.qm', 'qspectrumanalyzer/languages'),
                ('README.rst', '.'),
                ('LICENSE', '.'),
            ],
        },
        'bdist_msi': {
            'upgrade_code': '30740ef4-84e7-4e67-8e4a-12b53492c387',
            'shortcuts': [
                'QSpectrumAnalyzer=qspectrumanalyzer',
            ],
        },
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Communications :: Ham Radio",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    entry_points=setup_entry_points,
    cmdclass=setup_cmdclass,
)
