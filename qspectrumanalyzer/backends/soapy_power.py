import subprocess, pprint, sys, shlex

import numpy as np
from PyQt4 import QtCore

from qspectrumanalyzer.backends import BaseInfo, BasePowerThread
from soapypower.writer import SoapyPowerBinFormat

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

        print("soapy_power params:")
        pprint.pprint(self.params)
        print()

    def process_start(self):
        """Start soapy_power process"""
        if not self.process and self.params:
            settings = QtCore.QSettings()
            cmdline = [
                settings.value("executable", "soapy_power"),
                "-f", "{}M:{}M".format(self.params["start_freq"],
                                       self.params["stop_freq"]),
                "-B", "{}k".format(self.params["bin_size"]),
                "-T", "{}".format(self.params["interval"]),
                "-d", "{}".format(self.params["device"]),
                "-r", "{}".format(self.params["sample_rate"]),
                "-p", "{}".format(self.params["ppm"]),
                "-F", "soapy_power_bin",
            ]

            if self.params["gain"] >= 0:
                cmdline.extend(["-g", "{}".format(self.params["gain"])])
            if self.params["crop"] > 0:
                cmdline.extend(["-k", "{}".format(self.params["crop"])])
            if not self.params["single_shot"]:
                cmdline.append("-c")

            additional_params = settings.value("params", Info.additional_params)
            if additional_params:
                cmdline.extend(shlex.split(additional_params))

            self.process = subprocess.Popen(cmdline, stdout=subprocess.PIPE,
                                            universal_newlines=False)

    def parse_output(self, data):
        """Parse data from soapy_power"""
        header, y_axis = data

        timestamp = header.timestamp
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
            self.databuffer = {"timestamp": timestamp,
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
                data = formatter.read(self.process.stdout)
            except ValueError as e:
                print(e, file=sys.stderr)
                break

            if data:
                self.parse_output(data)
            else:
                break

        self.process_stop()
        self.alive = False
        self.powerThreadStopped.emit()
