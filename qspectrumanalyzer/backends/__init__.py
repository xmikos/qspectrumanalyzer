import os, threading, shlex

from PyQt6 import QtCore

from qspectrumanalyzer import subprocess


class BaseInfo:
    """Default device metadata"""
    sample_rate_min = 0
    sample_rate_max = 3200000
    sample_rate = 2560000
    bandwidth_min = 0
    bandwidth_max = 0
    bandwidth = 0
    gain_min = -1
    gain_max = 49.6
    gain = 37
    start_freq_min = 0
    start_freq_max = 2200
    start_freq = 87
    stop_freq_min = 0
    stop_freq_max = 2200
    stop_freq = 108
    bin_size_min = 0
    bin_size_max = 2800
    bin_size = 10
    interval_min = 0
    interval_max = 3600
    interval = 1
    ppm_min = -999
    ppm_max = 999
    ppm = 0
    crop_min = 0
    crop_max = 99
    crop = 0
    additional_params = ''
    help_device = None

    @classmethod
    def help_params(cls, executable):
        cmdline = shlex.split(executable)
        try:
            text = subprocess.check_output(cmdline + ['-h'], universal_newlines=True,
                                           stderr=subprocess.STDOUT, env=dict(os.environ, COLUMNS='125'),
                                           console=False)
        except subprocess.CalledProcessError as e:
            text = e.output
        except OSError:
            text = '{} executable not found!'.format(executable)
        return text


class BasePowerThread(QtCore.QThread):
    """Thread which runs Power Spectral Density acquisition and calculation process"""
    powerThreadStarted = QtCore.pyqtSignal()
    powerThreadStopped = QtCore.pyqtSignal()

    def __init__(self, data_storage, parent=None):
        super().__init__(parent)
        self.data_storage = data_storage
        self.alive = False
        self.process = None
        self._shutdown_lock = threading.Lock()

    def stop(self):
        """Stop power process thread"""
        self.process_stop()
        self.alive = False
        self.wait()

    def setup(self, start_freq, stop_freq, bin_size, interval=10.0, gain=-1, ppm=0, crop=0,
              single_shot=False, device=0, sample_rate=2560000, bandwidth=0, lnb_lo=0):
        """Setup power process params"""
        raise NotImplementedError

    def process_start(self):
        """Start power process"""
        raise NotImplementedError

    def process_stop(self):
        """Terminate power process"""
        with self._shutdown_lock:
            if self.process:
                if self.process.poll() is None:
                    try:
                        self.process.terminate()
                    except ProcessLookupError:
                        pass
                self.process.wait()
                self.process = None

    def parse_output(self, line):
        """Parse one line of output from power process"""
        raise NotImplementedError

    def run(self):
        """Power process thread main loop"""
        self.process_start()
        self.alive = True
        self.powerThreadStarted.emit()

        for line in self.process.stdout:
            if not self.alive:
                break
            self.parse_output(line)

        self.process_stop()
        self.alive = False
        self.powerThreadStopped.emit()


# Build list of all backends
__all__ = ['soapy_power', 'hackrf_sweep', 'rtl_power', 'rtl_power_fftw', 'rx_power']

# Import all backends
from qspectrumanalyzer.backends import soapy_power, hackrf_sweep, rtl_power, rtl_power_fftw, rx_power
