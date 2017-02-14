import subprocess, pprint, re

from PyQt4 import QtCore

from qspectrumanalyzer.backends import BaseInfo, BasePowerThread


class Info(BaseInfo):
    """soapy_power device metadata"""
    pass


class PowerThread(BasePowerThread):
    """Thread which runs soapy_power process"""
    re_two_floats = re.compile(r'^[-+\d.eE]+\s+[-+\d.eE]+$')

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
        self.databuffer_hop = {"timestamp": [], "x": [], "y": []}
        self.hop = 0
        self.run = 0
        self.prev_line = ""

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
            ]

            if self.params["gain"] >= 0:
                cmdline.extend(["-g", "{}".format(self.params["gain"])])
            if self.params["crop"] > 0:
                cmdline.extend(["-k", "{}".format(self.params["crop"])])
            if not self.params["single_shot"]:
                cmdline.append("-c")

            self.process = subprocess.Popen(cmdline, stdout=subprocess.PIPE,
                                            universal_newlines=True)

    def parse_output(self, line):
        """Parse one line of output from soapy_power"""
        line = line.strip()

        # One empty line => new hop
        if not line and self.prev_line:
            self.hop += 1
            print('    => HOP:', self.hop)
            self.databuffer["x"].extend(self.databuffer_hop["x"])
            self.databuffer["y"].extend(self.databuffer_hop["y"])
            self.databuffer_hop = {"timestamp": [], "x": [], "y": []}

        # Two empty lines => new set
        elif not line and not self.prev_line:
            self.hop = 0
            self.run += 1
            print('  * RUN:', self.run)
            self.data_storage.update(self.databuffer)
            self.databuffer = {"timestamp": [], "x": [], "y": []}

        # Get timestamp for new hop and set
        elif line.startswith("# Acquisition start:"):
            timestamp = line.split(":", 1)[1].strip()
            if not self.databuffer_hop["timestamp"]:
                self.databuffer_hop["timestamp"] = timestamp
            if not self.databuffer["timestamp"]:
                self.databuffer["timestamp"] = timestamp

        # Skip other comments
        elif line.startswith("#"):
            pass

        # Parse frequency and power
        elif self.re_two_floats.match(line):
            try:
                freq, power = line.split()
            except ValueError:
                return

            freq, power = float(freq), float(power)
            self.databuffer_hop["x"].append(freq)
            self.databuffer_hop["y"].append(power)

        self.prev_line = line
