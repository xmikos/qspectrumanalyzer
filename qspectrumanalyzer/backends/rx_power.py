import shlex

import numpy as np
from PyQt6 import QtCore

from qspectrumanalyzer import subprocess
from qspectrumanalyzer.backends import BaseInfo, BasePowerThread


class Info(BaseInfo):
    """rx_power device metadata"""
    sample_rate_min = 0
    sample_rate_max = 0
    sample_rate = 0
    start_freq_min = 0
    start_freq_max = 7250
    stop_freq_min = 0
    stop_freq_max = 7250
    gain_min = -1
    gain_max = 999
    bin_size_min = 0
    bin_size_max = 2800


class PowerThread(BasePowerThread):
    """Thread which runs rx_power process"""
    def setup(self, start_freq, stop_freq, bin_size, interval=10.0, gain=-1, ppm=0, crop=0,
              single_shot=False, device=0, sample_rate=2560000, bandwidth=0, lnb_lo=0):
        """Setup rx_power params"""
        self.params = {
            "start_freq": start_freq,
            "stop_freq": stop_freq,
            "bin_size": bin_size,
            "interval": interval,
            "device": device,
            "hops": 0,
            "gain": gain,
            "ppm": ppm,
            "crop": crop,
            "single_shot": single_shot
        }
        self.lnb_lo = lnb_lo
        self.databuffer = {}
        self.last_timestamp = ""

    def process_start(self):
        """Start rx_power process"""
        if not self.process and self.params:
            settings = QtCore.QSettings()
            cmdline = shlex.split(settings.value("executable_rx_power", "rx_power"))
            cmdline.extend([
                "-f", "{}M:{}M:{}k".format(self.params["start_freq"] - self.lnb_lo / 1e6,
                                           self.params["stop_freq"] - self.lnb_lo / 1e6,
                                           self.params["bin_size"]),
                "-i", "{}".format(self.params["interval"]),
                "-d", "{}".format(self.params["device"]),
                "-p", "{}".format(self.params["ppm"]),
                "-c", "{}".format(self.params["crop"])
            ])

            if self.params["gain"] >= 0:
                cmdline.extend(["-g", "{}".format(self.params["gain"])])
            if self.params["single_shot"]:
                cmdline.append("-1")

            backend_name = __name__.rsplit(".", 1)[-1]
            additional_params = settings.value(f"params_{backend_name}", Info.additional_params)
            if additional_params:
                cmdline.extend(shlex.split(additional_params))

            print('Starting backend:')
            print(' '.join(cmdline))
            print()
            self.process = subprocess.Popen(cmdline, stdout=subprocess.PIPE,
                                            universal_newlines=True, console=False)

    def parse_output(self, line):
        """Parse one line of output from rx_power"""
        line = [col.strip() for col in line.split(",")]
        timestamp = " ".join(line[:2])
        start_freq = int(line[2])
        stop_freq = int(line[3])
        step = float(line[4])
        samples = float(line[5])

        x_axis = list(np.linspace(start_freq + self.lnb_lo, stop_freq + self.lnb_lo,
                                  round((stop_freq - start_freq) / step)))
        y_axis = [float(y) for y in line[6:]]
        if len(x_axis) != len(y_axis):
            print("ERROR: len(x_axis) != len(y_axis)!")
            if len(x_axis) > len(y_axis):
                print("Trimming x_axis...")
                x_axis = x_axis[:len(y_axis)]
            else:
                print("Trimming y_axis...")
                y_axis = y_axis[:len(x_axis)]

        if timestamp != self.last_timestamp:
            self.last_timestamp = timestamp
            self.databuffer = {"timestamp": timestamp,
                               "x": x_axis,
                               "y": y_axis}
        else:
            self.databuffer["x"].extend(x_axis)
            self.databuffer["y"].extend(y_axis)

        # This have to be stupid like this to be compatible with old broken version of rtl_power. Right way is:
        # if stop_freq == (self.params["stop_freq"] - self.lnb_lo / 1e6) * 1e6:
        if stop_freq > ((self.params["stop_freq"] - self.lnb_lo / 1e6) * 1e6) - step:
            self.data_storage.update(self.databuffer)
