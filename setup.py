#!/usr/bin/env python

import sys, pathlib, subprocess, shutil, re
import setuptools

from qspectrumanalyzer.version import __version__

setup_cmdclass = {}
setup_kwargs = {}

# Allow compilation of Qt .qrc, .ui and .ts files (build_qt command)
try:
    from setup_qt import build_qt
    setup_cmdclass['build_qt'] = build_qt
except ImportError:
    pass

# Allow building of frozen executables with cx_Freeze (build_exe command)
try:
    from cx_Freeze import setup, Executable

    base = 'Win32GUI' if sys.platform == 'win32' else None
    setup_kwargs['executables'] = [
        Executable('qspectrumanalyzer.py', base=base),
        Executable('soapy_power.py', base=None),
    ]
except ImportError:
    from setuptools import setup


setup(
    name="QSpectrumAnalyzer",
    version=__version__,
    description="Spectrum analyzer for multiple SDR platforms (PyQtGraph based GUI for soapy_power, rx_power, rtl_power, hackrf_sweep and other backends)",
    long_description=open('README.rst').read(),
    author="Michal Krenek (Mikos)",
    author_email="m.krenek@gmail.com",
    url="https://github.com/xmikos/qspectrumanalyzer",
    license="GNU GPLv3",
    packages=["qspectrumanalyzer", "qspectrumanalyzer.backends"],
    package_data={
        "qspectrumanalyzer": [
            "*.ui",
            "languages/*.qm",
            "languages/*.ts"
        ]
    },
    data_files=[
        ("share/applications", ["qspectrumanalyzer.desktop"]),
        ("share/pixmaps", ["qspectrumanalyzer.png"])
    ],
    entry_points={
        "gui_scripts": [
            "qspectrumanalyzer=qspectrumanalyzer.__main__:main"
        ],
    },
    install_requires=[
        "soapy_power>=1.5.0",
        "pyqtgraph>=0.10.0",
        "Qt.py"
    ],
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
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    options={
        'build_exe': {
            'packages': ['qspectrumanalyzer', 'qspectrumanalyzer.backends'],
            'excludes': [],
            'includes': [
                'numpy.core._methods', 'numpy.lib.format', 'pyqtgraph.debug', 'pyqtgraph.ThreadsafeTimer'
            ],
            'include_msvcr': True,
            'optimize': 2,
        },
        'build_qt': {
            'packages': ['qspectrumanalyzer'],
            'languages': ['cs'],
            'replacement_bindings': 'Qt'
        },
    },
    cmdclass=setup_cmdclass,
    **setup_kwargs
)
