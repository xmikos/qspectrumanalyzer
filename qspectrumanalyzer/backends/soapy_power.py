import os, sys, shlex, signal

import numpy as np
from PyQt6 import QtCore

from qspectrumanalyzer import subprocess
from qspectrumanalyzer.backends import BaseInfo, BasePowerThread

try:
    from soapypower.writer import SoapyPowerBinFormat
    formatter = SoapyPowerBinFormat()
except ImportError:
    print('soapy_power module not found!')
    formatter = None


class Info(BaseInfo):
    """soapy_power device metadata"""
    sample_rate_min = 0
    sample_rate_max = 61440000
    bandwidth_min = 0
    bandwidth_max = 61440000
    start_freq_min = 0
    start_freq_max = 7250
    stop_freq_min = 0
    stop_freq_max = 7250
    gain_min = -1
    gain_max = 999
    bin_size_min = 0
    bin_size_max = 10000
    additional_params = '--even --fft-window boxcar --remove-dc'

    @classmethod
    def help_device(cls, executable, device):
        cmdline = shlex.split(executable)
        try:
            text = subprocess.check_output(cmdline + ['--detect'], universal_newlines=True,
                                           stderr=subprocess.DEVNULL, env=dict(os.environ, COLUMNS='125'),
                                           console=False)
            text += '\n'
            text += subprocess.check_output(cmdline + ['--device', device, '--info'], universal_newlines=True,
                                            stderr=subprocess.DEVNULL, env=dict(os.environ, COLUMNS='125'),
                                            console=False)
        except subprocess.CalledProcessError as e:
            text = e.output
        except OSError:
            text = '{} executable not found!'.format(executable)
        return text


class PowerThread(BasePowerThread):
    """Thread which runs soapy_power process"""
    def setup(self, start_freq, stop_freq, bin_size, interval=10.0, gain=-1, ppm=0, crop=0,
              single_shot=False, device="", sample_rate=2560000, bandwidth=0, lnb_lo=0):
        """Setup soapy_power params"""
        self.params = {
            "start_freq": start_freq,
            "stop_freq": stop_freq,
            "device": device,
            "sample_rate": sample_rate,
            "bandwidth": bandwidth,
            "bin_size": bin_size,
            "interval": interval,
            "hops": 0,
            "gain": gain,
            "ppm": ppm,
            "crop": crop * 100,
            "single_shot": single_shot
        }
        self.lnb_lo = lnb_lo
        self.databuffer = {"timestamp": [], "x": [], "y": []}
        self.min_freq = None

        self.pipe_read = None
        self.pipe_read_fd = None
        self.pipe_write_fd = None
        self.pipe_write_handle = None

    def process_start(self):
        """Start soapy_power process"""
        if not self.process and self.params:
            # Create pipe used for communication with soapy_power process
            self.pipe_read_fd, self.pipe_write_fd = os.pipe()
            self.pipe_read = open(self.pipe_read_fd, 'rb')
            os.set_inheritable(self.pipe_write_fd, True)

            if sys.platform == 'win32':
                self.pipe_write_handle = subprocess.make_inheritable_handle(self.pipe_write_fd)

            # Prepare soapy_power cmdline parameters
            settings = QtCore.QSettings()
            cmdline = shlex.split(settings.value("executable_soapy_power", "soapy_power"))
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

            if self.lnb_lo != 0:
                cmdline.extend(["--lnb-lo", "{}".format(self.lnb_lo)])
            if self.params["bandwidth"] > 0:
                cmdline.extend(["-w", "{}".format(self.params["bandwidth"])])
            if self.params["gain"] >= 0:
                cmdline.extend(["-g", "{}".format(self.params["gain"])])
            if self.params["crop"] > 0:
                cmdline.extend(["-k", "{}".format(self.params["crop"])])
            if not self.params["single_shot"]:
                cmdline.append("-c")

            backend_name = __name__.rsplit(".", 1)[-1]
            additional_params = settings.value(f"params_{backend_name}", Info.additional_params)
            if additional_params:
                cmdline.extend(shlex.split(additional_params))

            # Start soapy_power process and close write part of pipe
            if sys.platform == 'win32':
                creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
            else:
                creationflags = 0

            print('Starting backend:')
            print(' '.join(cmdline))
            print()
            self.process = subprocess.Popen(cmdline, close_fds=False, universal_newlines=False,
                                            creationflags=creationflags, console=False)

            os.close(self.pipe_write_fd)
            if sys.platform == 'win32':
                self.pipe_write_handle.Close()

    def process_stop(self):
        """Stop soapy_power process"""
        with self._shutdown_lock:
            if self.process:
                if self.process.poll() is None:
                    try:
                        if sys.platform == 'win32':
                            self.process.send_signal(signal.CTRL_BREAK_EVENT)
                        else:
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

        x_axis = np.linspace(start_freq, stop_freq, round((stop_freq - start_freq) / step))
        if len(x_axis) != len(y_axis):
            print("ERROR: len(x_axis) != len(y_axis)")
            return

        if self.min_freq is None:
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
        if not formatter:
            return

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


def read_from_file(f):
    """Generator for reading data from soapy_power binary files"""
    if not formatter:
        return

    min_freq = None
    databuffer = None

    while True:
        try:
            data = formatter.read(f)
        except ValueError as e:
            print(e, file=sys.stderr)
            continue

        if not data:
            if min_freq is not None:
                yield databuffer
            return

        header, y_axis = data
        x_axis = np.linspace(header.start, header.stop, round((header.stop - header.start) / header.step))
        if len(x_axis) != len(y_axis):
            print("ERROR: len(x_axis) != len(y_axis)")
            continue

        if min_freq is None:
            min_freq = header.start
        elif header.start == min_freq:
            yield databuffer

        if header.start == min_freq:
            databuffer = {"timestamp": header.time_stop,
                          "x": list(x_axis),
                          "y": list(y_axis)}
        else:
            databuffer["x"].extend(x_axis)
            databuffer["y"].extend(y_axis)
