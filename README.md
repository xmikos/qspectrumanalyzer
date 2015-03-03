QSpectrumAnalyzer
=================

Spectrum analyzer for RTL-SDR (GUI for rtl_power based on PyQtGraph)

Screenshot
----------

![QSpectrumAnalyzer](https://xmikos.github.io/qspectrumanalyzer/qspectrumanalyzer_screenshot.png)

Requirements
------------

- Python >= 3.3
- PyQt >= 4.5
- PyQtGraph (http://www.pyqtgraph.org)
- rtl-sdr (https://github.com/keenerd/rtl-sdr)

You should use Keenerds fork of rtl-sdr (latest Git revision),
bacause `rtl_power` in original rtl-sdr (from osmocom.org) is broken
(especially when used with cropping).

Usage
-----

Start QSpectrumAnalyzer by running `qspectrumanalyzer`.
