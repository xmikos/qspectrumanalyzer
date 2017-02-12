import subprocess, math, pprint

import numpy as np
from PyQt4 import QtCore
import struct


class RtlPowerBaseThread(QtCore.QThread):
    """Thread which runs rtl_power process"""
    rtlPowerStarted = QtCore.pyqtSignal()
    rtlPowerStopped = QtCore.pyqtSignal()

    def __init__(self, data_storage, parent=None):
        super().__init__(parent)
        self.data_storage = data_storage
        self.alive = False
        self.process = None

    def stop(self):
        """Stop rtl_power thread"""
        self.alive = False
        self.wait()

    def setup(self, start_freq, stop_freq, bin_size, interval=10.0, gain=-1,
              ppm=0, crop=0, single_shot=False, device_index=0, sample_rate=2560000):
        """Setup rtl_power params"""
        raise NotImplementedError

    def process_start(self):
        """Start rtl_power process"""
        raise NotImplementedError

    def process_stop(self):
        """Terminate rtl_power process"""
        if self.process:
            try:
                self.process.terminate()
            except ProcessLookupError:
                pass
            self.process.wait()
            self.process = None

    def parse_output(self, line):
        """Parse one line of output from rtl_power"""
        raise NotImplementedError

    def run(self):
        """Rtl_power thread main loop"""
        self.process_start()
        self.alive = True
        self.rtlPowerStarted.emit()

        for line in self.process.stdout:
            if not self.alive:
                break
            self.parse_output(line)

        self.process_stop()
        self.alive = False
        self.rtlPowerStopped.emit()


class RtlPowerThread(RtlPowerBaseThread):
    """Thread which runs rtl_power process"""
    def setup(self, start_freq, stop_freq, bin_size, interval=10.0, gain=-1,
              ppm=0, crop=0, single_shot=False, device_index=0, sample_rate=2560000):
        """Setup rtl_power params"""
        if bin_size > 2800:
            bin_size = 2800
        self.params = {
            "start_freq": start_freq,
            "stop_freq": stop_freq,
            "bin_size": bin_size,
            "interval": interval,
            "device_index": device_index,
            "hops": 0,
            "gain": gain,
            "ppm": ppm,
            "crop": crop,
            "single_shot": single_shot
        }
        self.databuffer = {}
        self.last_timestamp = ""

        print("rtl_power params:")
        pprint.pprint(self.params)
        print()

    def process_start(self):
        """Start rtl_power process"""
        if not self.process and self.params:
            settings = QtCore.QSettings()
            cmdline = [
                settings.value("rtl_power_executable", "rtl_power"),
                "-f", "{}M:{}M:{}k".format(self.params["start_freq"],
                                           self.params["stop_freq"],
                                           self.params["bin_size"]),
                "-i", "{}".format(self.params["interval"]),
                "-d", "{}".format(self.params["device_index"]),
                "-p", "{}".format(self.params["ppm"]),
                "-c", "{}".format(self.params["crop"])
            ]

            if self.params["gain"] >= 0:
                cmdline.extend(["-g", "{}".format(self.params["gain"])])
            if self.params["single_shot"]:
                cmdline.append("-1")

            self.process = subprocess.Popen(cmdline, stdout=subprocess.PIPE,
                                            universal_newlines=True)

    def parse_output(self, line):
        """Parse one line of output from rtl_power"""
        line = [col.strip() for col in line.split(",")]
        timestamp = " ".join(line[:2])
        start_freq = int(line[2])
        stop_freq = int(line[3])
        step = float(line[4])
        samples = float(line[5])

        x_axis = list(np.arange(start_freq, stop_freq, step))
        y_axis = [float(y) for y in line[6:]]
        if len(x_axis) != len(y_axis):
            print("ERROR: len(x_axis) != len(y_axis), use newer version of rtl_power!")
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
        # if stop_freq == self.params["stop_freq"] * 1e6:
        if stop_freq > (self.params["stop_freq"] * 1e6) - step:
            self.data_storage.update(self.databuffer)


class RtlPowerFftwThread(RtlPowerBaseThread):
    """Thread which runs rtl_power_fftw process"""
    def setup(self, start_freq, stop_freq, bin_size, interval=10.0, gain=-1,
              ppm=0, crop=0, single_shot=False, device_index=0, sample_rate=2560000):
        """Setup rtl_power_fftw params"""
        crop = crop * 100
        overlap = crop * 2
        freq_range = stop_freq * 1e6 - start_freq * 1e6
        min_overhang = sample_rate * overlap * 0.01
        hops = math.ceil((freq_range - min_overhang) / (sample_rate - min_overhang))
        overhang = (hops * sample_rate - freq_range) / (hops - 1) if hops > 1 else 0
        if bin_size > 2800:
            bin_size = 2800
        bins = math.ceil(sample_rate / (bin_size * 1e3))
        crop_freq = sample_rate * crop * 0.01

        self.params = {
            "start_freq": start_freq,
            "stop_freq": stop_freq,
            "freq_range": freq_range,
            "device_index": device_index,
            "sample_rate": sample_rate,
            "bin_size": bin_size,
            "bins": bins,
            "interval": interval,
            "hops": hops,
            "time": interval / hops,
            "gain": gain * 10,
            "ppm": ppm,
            "crop": crop,
            "overlap": overlap,
            "min_overhang": min_overhang,
            "overhang": overhang,
            "single_shot": single_shot
        }
        self.freqs = [self.get_hop_freq(hop) for hop in range(hops)]
        self.freqs_crop = [(f[0] + crop_freq, f[1] - crop_freq) for f in self.freqs]
        self.databuffer = {"timestamp": [], "x": [], "y": []}
        self.databuffer_hop = {"timestamp": [], "x": [], "y": []}
        self.hop = 0
        self.prev_line = ""

        print("rtl_power_fftw params:")
        pprint.pprint(self.params)
        print()

    def get_hop_freq(self, hop):
        """Get start and stop frequency for particular hop"""
        start_freq = self.params["start_freq"] * 1e6 + (self.params["sample_rate"] - self.params["overhang"]) * hop
        stop_freq = start_freq + self.params["sample_rate"] - (self.params["sample_rate"] / self.params["bins"])
        return (start_freq, stop_freq)

    def process_start(self):
        """Start rtl_power_fftw process"""
        if not self.process and self.params:
            settings = QtCore.QSettings()
            cmdline = [
                settings.value("rtl_power_executable", "rtl_power_fftw"),
                "-f", "{}M:{}M".format(self.params["start_freq"],
                                       self.params["stop_freq"]),
                "-b", "{}".format(self.params["bins"]),
                "-t", "{}".format(self.params["time"]),
                "-d", "{}".format(self.params["device_index"]),
                "-r", "{}".format(self.params["sample_rate"]),
                "-p", "{}".format(self.params["ppm"]),
            ]

            if self.params["gain"] >= 0:
                cmdline.extend(["-g", "{}".format(self.params["gain"])])
            if self.params["overlap"] > 0:
                cmdline.extend(["-o", "{}".format(self.params["overlap"])])
            if not self.params["single_shot"]:
                cmdline.append("-c")

            self.process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                            universal_newlines=True)

    def parse_output(self, line):
        """Parse one line of output from rtl_power_fftw"""
        line = line.strip()

        # One empty line => new hop
        if not line and self.prev_line:
            self.hop += 1
            self.databuffer["x"].extend(self.databuffer_hop["x"])
            self.databuffer["y"].extend(self.databuffer_hop["y"])
            self.databuffer_hop = {"timestamp": [], "x": [], "y": []}

        # Two empty lines => new set
        elif not line and not self.prev_line:
            self.hop = 0
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
        elif line[0].isdigit():
            freq, power = line.split()
            freq, power = float(freq), float(power)
            start_freq, stop_freq = self.freqs_crop[self.hop]

            # Apply cropping
            if freq >= start_freq and freq <= stop_freq:
                # Skip overlapping frequencies
                if not self.databuffer["x"] or freq > self.databuffer["x"][-1]:
                    #print("  {:.3f} MHz".format(freq / 1e6))
                    self.databuffer_hop["x"].append(freq)
                    self.databuffer_hop["y"].append(power)
                else:
                    #print("  Overlapping {:.3f} MHz".format(freq / 1e6))
                    pass
            else:
                #print("  Cropping {:.3f} MHz".format(freq / 1e6))
                pass

        self.prev_line = line

class HackRFSweepThread(RtlPowerBaseThread):
    """Thread which runs hackrf_sweep process"""
    def setup(self, start_freq=0, stop_freq=6000, bin_size=1000,
            interval=0.0, gain=40, ppm=0, crop=0, single_shot=False,
            device_index=0, sample_rate=20000000):
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
            "start_freq": start_freq, # MHz
            "stop_freq": stop_freq, # MHz
            "hops": 0,
            "device_index": 0,
            "sample_rate": 20e6, # sps
            "bin_size": bin_size, # kHz
            "interval": 0, # seconds
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
                settings.value("rtl_power_executable", "hackrf_sweep"),
                        "-f", "{}:{}".format(int(self.params["start_freq"]),
                                int(self.params["stop_freq"])),
                        "-B",
                        "-w", "{}".format(int(self.params["bin_size"]*1000)),
                        "-l", "{}".format(int(self.params["lna_gain"])),
                        "-g", "{}".format(int(self.params["vga_gain"])),
            ]

            if self.params["single_shot"]:
                cmdline.append("-1")

            self.process = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                            universal_newlines=False)

    def parse_output(self, buf):
        """Parse one buf of output from hackrf_sweep"""
        (low_edge, high_edge) = struct.unpack('QQ', buf[:16])
        data = np.fromstring(buf[16:], dtype='<f4')
        step = (high_edge - low_edge) / len(data)

        if (low_edge//1000000) <= (self.params["start_freq"]):
            # Reset databuffer at the start of each sweep even if we somehow
            # did not complete the previous sweep.
            self.databuffer = {"timestamp": [], "x": [], "y": []}
        x_axis = list(np.arange(low_edge + step/2, high_edge, step))
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
        self.rtlPowerStarted.emit()

        while self.alive:
            buf = self.process.stdout.read(4)
            if buf:
                (record_length,) = struct.unpack('I', buf)
                buf = self.process.stdout.read(record_length)
                if buf:
                    self.parse_output(buf)

        self.process_stop()
        self.alive = False
        self.rtlPowerStopped.emit()
