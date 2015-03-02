#!/usr/bin/env python

from distutils.core import setup
from qspectrumanalyzer.version import __version__

setup(name="QSpectrumAnalyzer",
      version=__version__,
      description="Spectrum analyzer for RTL-SDR (GUI for rtl_power based on PyQtGraph)",
      author="Michal Krenek (Mikos)",
      author_email="m.krenek@gmail.com",
      url="https://github.com/xmikos/qspectrumanalyzer",
      license="GNU GPLv3",
      packages=["qspectrumanalyzer"],
      data_files=[("share/applications", ["qspectrumanalyzer.desktop"]),
                  ("share/pixmaps", ["qspectrumanalyzer.png"])],
      scripts=["scripts/qspectrumanalyzer"],
      requires=["PyQt4", "pyqtgraph"])
