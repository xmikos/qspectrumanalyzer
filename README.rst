QSpectrumAnalyzer
=================

Spectrum analyzer for RTL-SDR (GUI for rtl_power based on PyQtGraph)

Screenshot
----------

.. image:: https://xmikos.github.io/qspectrumanalyzer/qspectrumanalyzer_screenshot.png

Requirements
------------

- Python >= 3.3
- PyQt >= 4.5
- PyQtGraph (http://www.pyqtgraph.org)
- rtl-sdr (https://github.com/keenerd/rtl-sdr)
- Optional: rtl_power_fftw (https://github.com/AD-Vega/rtl-power-fftw)

You should use `Keenerds fork of rtl-sdr <https://github.com/keenerd/rtl-sdr>`_
(latest Git revision), because ``rtl_power`` in original rtl-sdr (from osmocom.org)
is broken (especially when used with cropping).

Another alternative is
`rtl_power_fftw <https://github.com/AD-Vega/rtl-power-fftw>`_ which has various
benefits over ``rtl_power``. E.g. better FFT performance (thanks to
use of ``fftw`` library) and possibility to use much shorter acquisition time
for more real-time continuous measurement (minimum interval in original
``rtl_power`` is 1 second, but in ``rtl_power_fftw`` you are only limited
by number of frequency hops).

Usage
-----

Start QSpectrumAnalyzer by running ``qspectrumanalyzer``.

You can choose if you want to use ``rtl_power`` or ``rtl_power_fftw`` backend in
*File* -> *Settings* (default is ``rtl_power``). Path to ``rtl_power``
(or ``rtl_power_fftw``) executable can be also manually specified there. You can also
set waterfall plot history size in there. Default is 100 lines, be aware that
really large sweeps (with a lot of bins) would require a lot of system memory, so
don't make this number too big.

Controls should be intuitive, but if you want consistent results, you should
turn off automatic gain control (set it to some fixed number) and also set
crop to 20% or more. For finding out ppm correction factor for your rtl-sdr
stick, use `kalibrate-rtl <https://github.com/steve-m/kalibrate-rtl>`_.

You can move and zoom plot with mouse, change plot settings or export plots
from right-click menu. Waterfall plot black/white levels and color lookup
table can be changed in mini-histogram widget.
