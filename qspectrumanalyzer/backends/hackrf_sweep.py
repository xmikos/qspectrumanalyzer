import subprocess, pprint, struct, shlex

import numpy as np
from PyQt4 import QtCore

from qspectrumanalyzer.backends import BaseInfo, BasePowerThread


class Info(BaseInfo):
    """hackrf_sweep device metadata"""
    sample_rate_min = 20000000
    sample_rate_max = 20000000
    sample_rate = 20000000
    gain_min = 0
    gain_max = 102
    gain = 40
    start_freq_min = 0
    start_freq_max = 7230
    start_freq = 0
    stop_freq_min = 0
    stop_freq_max = 7250
    stop_freq = 6000
    bin_size_min = 40
    bin_size_max = 5000
    bin_size = 1000
    interval_min = 0
    interval_max = 0
    interval = 0
    ppm_min = 0
    ppm_max = 0
    ppm = 0
    crop_min = 0
    crop_max = 0
    crop = 0


class PowerThread(BasePowerThread):
    """Thread which runs hackrf_sweep process"""
    def setup(self, start_freq=0, stop_freq=6000, bin_size=1000,
              interval=0.0, gain=40, ppm=0, crop=0, single_shot=False,
              device=0, sample_rate=20000000):
        """Setup hackrf_sweep params"""
        # theoretically we can support bins smaller than 40 kHz, but it is
        # unlikely to result in acceptable performance
        if bin_size < 40:
            bin_size = 40
        if bin_size > 5000:
            bin_size = 5000

        # We only support whole numbers of steps with bandwidth equal to the
        # sample rate.
        step_bandwidth = sample_rate / 1000000
        total_bandwidth = stop_freq - start_freq
        step_count = 1 + (total_bandwidth - 1) // step_bandwidth
        total_bandwidth = step_count * step_bandwidth
        stop_freq = start_freq + total_bandwidth

        # distribute gain between two analog gain stages
        if gain < 0:
            gain = 0
        if gain > 102:
            gain = 102
        lna_gain = 8 * (gain // 18)
        vga_gain = 2 * ((gain - lna_gain) // 2)

        self.params = {
            "start_freq": start_freq,  # MHz
            "stop_freq": stop_freq,  # MHz
            "hops": 0,
            "device": 0,
            "sample_rate": 20e6,  # sps
            "bin_size": bin_size,  # kHz
            "interval": 0,  # seconds
            "gain": gain,
            "lna_gain": lna_gain,
            "vga_gain": vga_gain,
            "ppm": 0,
            "crop": 0,
            "single_shot": single_shot
        }
        self.databuffer = {"timestamp": [], "x": [], "y": []}

        print("hackrf_sweep params:")
        pprint.pprint(self.params)
        print()

    def process_start(self):
        """Start hackrf_sweep process"""
        if not self.process and self.params:
            settings = QtCore.QSettings()
            cmdline = [
                settings.value("executable", "hackrf_sweep"),
                "-f", "{}:{}".format(int(self.params["start_freq"]),
                                     int(self.params["stop_freq"])),
                "-B",
                "-w", "{}".format(int(self.params["bin_size"] * 1000)),
                "-l", "{}".format(int(self.params["lna_gain"])),
                "-g", "{}".format(int(self.params["vga_gain"])),
            ]

            if self.params["single_shot"]:
                cmdline.append("-1")

            additional_params = settings.value("params", Info.additional_params)
            if additional_params:
                cmdline.extend(shlex.split(additional_params))

            self.process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                            universal_newlines=False)

    def parse_output(self, buf):
        """Parse one buf of output from hackrf_sweep"""
        (low_edge, high_edge) = struct.unpack('QQ', buf[:16])
        data = np.fromstring(buf[16:], dtype='<f4')
        step = (high_edge - low_edge) / len(data)

        if (low_edge // 1000000) <= (self.params["start_freq"]):
            # Reset databuffer at the start of each sweep even if we somehow
            # did not complete the previous sweep.
            self.databuffer = {"timestamp": [], "x": [], "y": []}
        x_axis = list(np.arange(low_edge + step / 2, high_edge, step))
        self.databuffer["x"].extend(x_axis)
        for i in range(len(data)):
            self.databuffer["y"].append(data[i])
        if (high_edge / 1e6) >= (self.params["stop_freq"]):
            # We've reached the end of a pass, so sort and display it.
            sorted_data = sorted(zip(self.databuffer["x"], self.databuffer["y"]))
            self.databuffer["x"], self.databuffer["y"] = [list(x) for x in zip(*sorted_data)]
            self.data_storage.update(self.databuffer)

    def run(self):
        """hackrf_sweep thread main loop"""
        self.process_start()
        self.alive = True
        self.powerThreadStarted.emit()

        while self.alive:
            buf = self.process.stdout.read(4)
            if buf:
                (record_length,) = struct.unpack('I', buf)
                buf = self.process.stdout.read(record_length)
                if buf:
                    self.parse_output(buf)
                else:
                    break
            else:
                break

        self.process_stop()
        self.alive = False
        self.powerThreadStopped.emit()
