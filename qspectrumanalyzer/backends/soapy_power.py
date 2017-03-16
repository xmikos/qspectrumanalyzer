import os, subprocess, pprint, sys, shlex

import numpy as np
from Qt import QtCore

from qspectrumanalyzer.backends import BaseInfo, BasePowerThread
from soapypower.writer import SoapyPowerBinFormat

if sys.platform == 'win32':
    import msvcrt
    import _winapi

    def _make_inheritable_handle(fd):
        """Return a duplicate of handle, which is inheritable"""
        h = _winapi.DuplicateHandle(
            _winapi.GetCurrentProcess(),
            msvcrt.get_osfhandle(fd),
            _winapi.GetCurrentProcess(), 0, 1,
            _winapi.DUPLICATE_SAME_ACCESS
        )
        return subprocess.Handle(h)

formatter = SoapyPowerBinFormat()


class Info(BaseInfo):
    """soapy_power device metadata"""
    sample_rate_min = 0
    sample_rate_max = 61440000
    start_freq_min = 0
    start_freq_max = 6000
    stop_freq_min = 0
    stop_freq_max = 6000
    additional_params = '--even --fft-window boxcar --remove-dc'


class PowerThread(BasePowerThread):
    """Thread which runs soapy_power process"""
    def setup(self, start_freq, stop_freq, bin_size, interval=10.0, gain=-1,
              ppm=0, crop=0, single_shot=False, device="", sample_rate=2560000):
        """Setup soapy_power params"""
        self.params = {
            "start_freq": start_freq,
            "stop_freq": stop_freq,
            "device": device,
            "sample_rate": sample_rate,
            "bin_size": bin_size,
            "interval": interval,
            "hops": 0,
            "gain": gain * 10,
            "ppm": ppm,
            "crop": crop * 100,
            "single_shot": single_shot
        }
        self.databuffer = {"timestamp": [], "x": [], "y": []}
        self.min_freq = 0

        self.pipe_read = None
        self.pipe_read_fd = None
        self.pipe_write_fd = None
        self.pipe_write_handle = None

        print("soapy_power params:")
        pprint.pprint(self.params)
        print()

    def process_start(self):
        """Start soapy_power process"""
        if not self.process and self.params:
            # Create pipe used for communication with soapy_power process
            self.pipe_read_fd, self.pipe_write_fd = os.pipe()
            self.pipe_read = open(self.pipe_read_fd, 'rb')
            os.set_inheritable(self.pipe_write_fd, True)

            if sys.platform == 'win32':
                self.pipe_write_handle = _make_inheritable_handle(self.pipe_write_fd)

            # Prepare soapy_power cmdline parameters
            settings = QtCore.QSettings()
            cmdline = shlex.split(settings.value("executable", "soapy_power"))
            cmdline.extend([
                "-f", "{}M:{}M".format(self.params["start_freq"],
                                       self.params["stop_freq"]),
                "-B", "{}k".format(self.params["bin_size"]),
                "-T", "{}".format(self.params["interval"]),
                "-d", "{}".format(self.params["device"]),
                "-r", "{}".format(self.params["sample_rate"]),
                "-p", "{}".format(self.params["ppm"]),
                "-F", "soapy_power_bin",
                "--output-fd", "{}".format(
                    int(self.pipe_write_handle) if sys.platform == 'win32' else self.pipe_write_fd
                ),
            ])

            if self.params["gain"] >= 0:
                cmdline.extend(["-g", "{}".format(self.params["gain"])])
            if self.params["crop"] > 0:
                cmdline.extend(["-k", "{}".format(self.params["crop"])])
            if not self.params["single_shot"]:
                cmdline.append("-c")

            additional_params = settings.value("params", Info.additional_params)
            if additional_params:
                cmdline.extend(shlex.split(additional_params))

            # Start soapy_power process and close write part of pipe
            self.process = subprocess.Popen(cmdline, close_fds=False, universal_newlines=False)
            os.close(self.pipe_write_fd)
            if sys.platform == 'win32':
                self.pipe_write_handle.Close()

    def process_stop(self):
        """Stop soapy_power process"""
        with self._shutdown_lock:
            if self.process:
                try:
                    self.process.terminate()
                except ProcessLookupError:
                    pass
                self.process.wait()
                self.process = None

                # Close pipe used for communication with soapy_power process
                self.pipe_read.close()

                self.pipe_read = None
                self.pipe_read_fd = None
                self.pipe_write_fd = None
                self.pipe_write_handle = None

    def parse_output(self, data):
        """Parse data from soapy_power"""
        header, y_axis = data

        time_start = header.time_start
        time_stop = header.time_stop
        start_freq = header.start
        stop_freq = header.stop
        step = header.step
        samples = header.samples

        x_axis = np.arange(start_freq, stop_freq, step)
        if len(x_axis) != len(y_axis):
            print("ERROR: len(x_axis) != len(y_axis)")

        if not self.min_freq:
            self.min_freq = start_freq

        if start_freq == self.min_freq:
            self.databuffer = {"timestamp": time_stop,
                               "x": list(x_axis),
                               "y": list(y_axis)}
        else:
            self.databuffer["x"].extend(x_axis)
            self.databuffer["y"].extend(y_axis)

        if stop_freq > (self.params["stop_freq"] * 1e6) - step:
            self.data_storage.update(self.databuffer)

    def run(self):
        """soapy_power thread main loop"""
        self.process_start()
        self.alive = True
        self.powerThreadStarted.emit()

        while self.alive:
            try:
                data = formatter.read(self.pipe_read)
            except ValueError as e:
                print(e, file=sys.stderr)
                continue

            if data:
                self.parse_output(data)
            else:
                break

        self.process_stop()
        self.alive = False
        self.powerThreadStopped.emit()
