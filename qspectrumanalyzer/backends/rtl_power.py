import shlex

import numpy as np
from PyQt6 import QtCore

from qspectrumanalyzer import subprocess
from qspectrumanalyzer.backends import BaseInfo, BasePowerThread


class Info(BaseInfo):
    """rtl_power device metadata"""
    pass


class PowerThread(BasePowerThread):
    """Thread which runs rtl_power process"""
    def setup(self, start_freq, stop_freq, bin_size, interval=10.0, gain=-1, ppm=0, crop=0,
              single_shot=False, device=0, sample_rate=2560000, bandwidth=0, lnb_lo=0):
        """Setup rtl_power params"""
        if bin_size > 2800:
            bin_size = 2800
        self.params = {
            "start_freq": start_freq,
            "stop_freq": stop_freq,
            "bin_size": bin_size,
            "interval": interval,
            "device": device,
            "sample_rate": sample_rate,
            "hops": 0,
            "gain": gain,
            "ppm": ppm,
            "crop": crop,
            "single_shot": single_shot
        }
        self.lnb_lo = lnb_lo
        self.databuffer = {}
        self.last_timestamp = ""
        self._warned_length_mismatch = False

    def process_start(self):
        """Start rtl_power process"""
        if not self.process and self.params:
            settings = QtCore.QSettings()
            cmdline = shlex.split(settings.value("executable_rtl_power", "rtl_power"))
            cmdline.extend([
                "-f", "{}M:{}M:{}k".format(self.params["start_freq"] - self.lnb_lo / 1e6,
                                           self.params["stop_freq"] - self.lnb_lo / 1e6,
                                           self.params["bin_size"]),
                "-i", "{}".format(self.params["interval"]),
                "-d", "{}".format(self.params["device"]),
                "-p", "{}".format(self.params["ppm"]),
                "-c", "{}".format(self.params["crop"])
            ])

            # Sample rate parameter was supported in older rtl_power versions only
            # if self.params["sample_rate"] > 0:
            #     cmdline.extend(["-r", "{}M".format(self.params["sample_rate"] / 1e6)])
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
        """Parse one line of output from rtl_power"""
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
            if not self._warned_length_mismatch:
                print("WARNING: len(x_axis) != len(y_axis); recomputing x-axis to match rtl_power output. "
                      "Upgrade rtl_power for consistent output if possible.")
                self._warned_length_mismatch = True
            # Recompute x_axis to match rtl_power output length
            x_axis = list(np.linspace(start_freq + self.lnb_lo, stop_freq + self.lnb_lo, len(y_axis)))

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
