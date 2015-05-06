# QSpectrumAnalyzer

Spectrum analyzer for RTL-SDR (GUI for rtl_power based on PyQtGraph)

## Screenshot

![Alt text](http://xmikos.github.io/qspectrumanalyzer/qspectrumanalyzer_screenshot.png "Screenshot")

## Requirements

- Python >= 3.3
- PyQt >= 4.5
- PyQtGraph (http://www.pyqtgraph.org)
- rtl-sdr (https://github.com/keenerd/rtl-sdr)

You should use Keenerds fork of rtl-sdr (latest Git revision),
bacause ``rtl_power`` in original rtl-sdr (from osmocom.org) is broken
(especially when used with cropping).

## Install for Ubuntu

Misc

    sudo apt-get install python3-setuptools

PyQt

    sudo apt-get install pyqt4-dev-tools python3-pyqt4

Numpy

    sudo apt-get install python3-numpy

PyQtGraph

    git clone https://github.com/pyqtgraph/pyqtgraph.git
    cd pyqtgraph
    sudo python3 setup.py install

## Usage

    git clone https://github.com/xmikos/qspectrumanalyzer.git
    cd qspectrumanalyzer
    python3 setup-qt.py
    sudo python3 setup.py install
    
After that start QSpectrumAnalyzer by just running ``qspectrumanalyzer``.

If you don't have ``rtl_power`` executable in system path, you can specify
location of it manually in *File* -> *Settings*. You can also specify waterfall
plot history size in there. Default is 100 lines, be aware that really large
sweeps (with a lot of bins) would require a lot of system memory, so don't make
this number too big.

Controls should be intuitive, but if you want consistent results, you should
turn off automatic gain control (set it to some fixed number) and also set
crop to 20% or more. For finding out ppm correction factor for your rtl-sdr
stick, use `kalibrate-rtl <https://github.com/steve-m/kalibrate-rtl>`_.

You can move and zoom plot with mouse, change plot settings or export plots
from right-click menu. Waterfall plot black/white levels and color lookup
table can be changed in mini-histogram widget.
