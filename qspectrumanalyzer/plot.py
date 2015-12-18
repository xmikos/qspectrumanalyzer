import collections, math

import numpy as np
import pyqtgraph as pg

from qspectrumanalyzer.utils import smooth

# Basic PyQtGraph settings
pg.setConfigOptions(antialias=True)


class SpectrumPlotWidget:
    """Main spectrum plot"""
    def __init__(self, layout):
        if not isinstance(layout, pg.GraphicsLayoutWidget):
            raise ValueError("layout must be instance of pyqtgraph.GraphicsLayoutWidget")

        self.layout = layout

        self.main_curve = True
        self.main_color = pg.mkColor("y")
        self.persistence = False
        self.persistence_length = 5
        self.persistence_decay = "exponential"
        self.persistence_color = pg.mkColor("g")
        self.peak_hold = False
        self.peak_hold_color = pg.mkColor("r")
        self.average = False
        self.average_color = pg.mkColor("c")
        self.smooth = False
        self.smooth_length = 11
        self.smooth_window = "hanning"

        self.counter = 0
        self.peak_hold_data = None
        self.average_data = None
        self.persistence_data = None
        self.persistence_curves = None

        self.create_plot()

    def create_plot(self):
        """Create main spectrum plot"""
        self.posLabel = self.layout.addLabel(row=0, col=0, justify="right")
        self.plot = self.layout.addPlot(row=1, col=0)
        self.plot.showGrid(x=True, y=True)
        self.plot.setLabel("left", "Power", units="dBm")
        self.plot.setLabel("bottom", "Frequency", units="Hz")
        self.plot.setLimits(xMin=0)
        self.plot.showButtons()

        self.create_persistence_curves()
        self.create_average_curve()
        self.create_main_curve()
        self.create_peak_hold_curve()

        # Create crosshair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.vLine.setZValue(1000)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.vLine.setZValue(1000)
        self.plot.addItem(self.vLine, ignoreBounds=True)
        self.plot.addItem(self.hLine, ignoreBounds=True)
        self.mouseProxy = pg.SignalProxy(self.plot.scene().sigMouseMoved,
                                         rateLimit=60, slot=self.mouse_moved)

    def create_peak_hold_curve(self):
        """Create peak hold curve"""
        self.curve_peak_hold = self.plot.plot(pen=self.peak_hold_color)
        self.curve_peak_hold.setZValue(900)

    def create_main_curve(self):
        """Create main spectrum curve"""
        self.curve = self.plot.plot(pen=self.main_color)
        self.curve.setZValue(800)

    def create_average_curve(self):
        """Create average curve"""
        self.curve_average = self.plot.plot(pen=self.average_color)
        self.curve_average.setZValue(700)

    def create_persistence_curves(self):
        """Create spectrum persistence curves"""
        z_index_base = 600
        decay = self.get_decay()
        self.persistence_curves = []
        for i in range(self.persistence_length):
            alpha = 255 * decay(i + 1, self.persistence_length + 1)
            color = self.persistence_color
            curve = self.plot.plot(pen=(color.red(), color.green(), color.blue(), alpha))
            curve.setZValue(z_index_base - i)
            self.persistence_curves.append(curve)

    def set_colors(self):
        """Set colors of all curves"""
        self.curve.setPen(self.main_color)
        self.curve_peak_hold.setPen(self.peak_hold_color)
        self.curve_average.setPen(self.average_color)

        decay = self.get_decay()
        for i, curve in enumerate(self.persistence_curves):
            alpha = 255 * decay(i + 1, self.persistence_length + 1)
            color = self.persistence_color
            curve.setPen((color.red(), color.green(), color.blue(), alpha))

    def decay_linear(self, x, length):
        """Get alpha value for persistence curve (linear decay)"""
        return (-x / length) + 1

    def decay_exponential(self, x, length, const=1/3):
        """Get alpha value for persistence curve (exponential decay)"""
        return math.e**(-x / (length * const))

    def get_decay(self):
        """Get decay function"""
        if self.persistence_decay == 'exponential':
            return self.decay_exponential
        else:
            return self.decay_linear

    def update_plot(self, data):
        """Update main spectrum plot"""
        self.counter += 1

        # Apply smoothing to data
        if self.smooth:
            data["y"] = smooth(data["y"],
                               window_len=self.smooth_length,
                               window=self.smooth_window)

        # Draw main curve
        if self.main_curve:
            self.curve.setData(data["x"], data["y"])

        # Update peak hold data and draw peak hold curve
        if self.peak_hold:
            if self.peak_hold_data is None:
                self.peak_hold_data = data["y"].copy()
            else:
                for i, y in enumerate(data["y"]):
                    if y > self.peak_hold_data[i]:
                        self.peak_hold_data[i] = y
            self.curve_peak_hold.setData(data["x"], self.peak_hold_data)

        # Update average data and draw average curve
        if self.average:
            if self.average_data is None:
                self.average_data = data["y"].copy()
            else:
                for i, y in enumerate(data["y"]):
                    self.average_data[i] = (self.counter * self.average_data[i] + y) / (self.counter + 1)
            self.curve_average.setData(data["x"], self.average_data)

        # Draw persistence curves
        if self.persistence:
            if self.persistence_data is None:
                self.persistence_data = collections.deque(maxlen=self.persistence_length)
            else:
                for i, y in enumerate(self.persistence_data):
                    self.persistence_curves[i].setData(data["x"], y)
            self.persistence_data.appendleft(data["y"].copy())

    def mouse_moved(self, evt):
        """Update crosshair when mouse is moved"""
        pos = evt[0]
        if self.plot.sceneBoundingRect().contains(pos):
            mousePoint = self.plot.vb.mapSceneToView(pos)
            self.posLabel.setText(
                "<span style='font-size: 12pt'>f={:0.3f} MHz, P={:0.3f} dBm</span>".format(mousePoint.x() / 1e6,
                                                                                           mousePoint.y())
            )
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())

    def main_clear(self):
        """Clear main spectrum curve"""
        self.curve.clear()
        self.plot.removeItem(self.curve)
        self.create_main_curve()

    def peak_hold_clear(self):
        """Clear peak hold curve"""
        self.peak_hold_data = None
        self.curve_peak_hold.clear()
        self.plot.removeItem(self.curve_peak_hold)
        self.create_peak_hold_curve()

    def average_clear(self):
        """Clear average curve"""
        self.counter = 0
        self.average_data = None
        self.curve_average.clear()
        self.plot.removeItem(self.curve_average)
        self.create_average_curve()

    def persistence_clear(self):
        """Clear spectrum persistence curves"""
        self.persistence_data = None
        for curve in self.persistence_curves:
            curve.clear()
            self.plot.removeItem(curve)
        self.create_persistence_curves()


class WaterfallPlotWidget:
    """Waterfall plot"""
    def __init__(self, layout, histogram_layout=None):
        if not isinstance(layout, pg.GraphicsLayoutWidget):
            raise ValueError("layout must be instance of pyqtgraph.GraphicsLayoutWidget")

        if histogram_layout and not isinstance(histogram_layout, pg.GraphicsLayoutWidget):
            raise ValueError("histogram_layout must be instance of pyqtgraph.GraphicsLayoutWidget")

        self.layout = layout
        self.histogram_layout = histogram_layout

        self.history_size = 100
        self.counter = 0

        self.create_plot()

    def create_plot(self):
        """Create waterfall plot"""
        self.plot = self.layout.addPlot()
        self.plot.setLabel("bottom", "Frequency", units="Hz")
        self.plot.setLabel("left", "Time")

        self.plot.setYRange(-self.history_size, 0)
        self.plot.setLimits(xMin=0, yMax=0)
        self.plot.showButtons()
        #self.plot.setAspectLocked(True)
        #self.plot.setDownsampling(mode="peak")
        #self.plot.setClipToView(True)

        # Setup histogram widget (for controlling waterfall plot levels and gradients)
        if self.histogram_layout:
            self.histogram = pg.HistogramLUTItem()
            self.histogram_layout.addItem(self.histogram)
            self.histogram.gradient.loadPreset("flame")
            #self.histogram.setHistogramRange(-50, 0)
            #self.histogram.setLevels(-50, 0)

    def update_plot(self, data):
        """Update waterfall plot"""
        self.counter += 1

        # Create waterfall data array and waterfall image on first run
        if self.counter == 1:
            self.waterfallImgArray = np.zeros((self.history_size, len(data["x"])))
            self.waterfallImg = pg.ImageItem()
            self.waterfallImg.scale((data["x"][-1] - data["x"][0]) / len(data["x"]), 1)
            self.plot.clear()
            self.plot.addItem(self.waterfallImg)

        # Roll down one and replace leading edge with new data
        self.waterfallImgArray = np.roll(self.waterfallImgArray, -1, axis=0)
        self.waterfallImgArray[-1] = data["y"]
        self.waterfallImg.setImage(self.waterfallImgArray[-self.counter:].T,
                                   autoLevels=False, autoRange=False)

        # Move waterfall image to always start at 0
        self.waterfallImg.setPos(data["x"][0],
                                 -self.counter if self.counter < self.history_size
                                 else -self.history_size)

        # Link histogram widget to waterfall image on first run
        # (must be done after first data is received or else levels would be wrong)
        if self.counter == 1 and self.histogram_layout:
            self.histogram.setImageItem(self.waterfallImg)
