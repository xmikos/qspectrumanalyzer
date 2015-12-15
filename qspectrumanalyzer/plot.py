import numpy as np
import pyqtgraph as pg

from qspectrumanalyzer.utils import smooth

# Basic PyQtGraph settings
pg.setConfigOptions(antialias=True)


class SpectrumPlotWidget:
    """Main spectrum plot"""
    def __init__(self, layout):
        if not isinstance(layout, pg.GraphicsLayoutWidget):
            raise ValueError('layout must be instance of pyqtgraph.GraphicsLayoutWidget')

        self.layout = layout
        self.peak_hold_data = None
        self.peak_hold = False
        self.smooth = False
        self.smooth_length = 11
        self.smooth_window = 'hanning'

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

        # Create spectrum curve
        self.curve = self.plot.plot()

        # Create peak hold curve
        self.curve_peak_hold = self.plot.plot(pen='r')

        # Create crosshair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.plot.addItem(self.vLine, ignoreBounds=True)
        self.plot.addItem(self.hLine, ignoreBounds=True)
        self.mouseProxy = pg.SignalProxy(self.plot.scene().sigMouseMoved,
                                         rateLimit=60, slot=self.mouse_moved)

    def update_plot(self, data):
        """Update main spectrum plot"""
        # Apply smoothing to data
        if self.smooth:
            data["y"] = smooth(data["y"],
                               window_len=self.smooth_length,
                               window=self.smooth_window)

        # Update peak hold data and draw peak hold curve
        if self.peak_hold:
            if self.peak_hold_data is None:
                self.peak_hold_data = data["y"]
            else:
                for i, y in enumerate(data["y"]):
                    if y > self.peak_hold_data[i]:
                        self.peak_hold_data[i] = y

            self.curve_peak_hold.setData(data["x"], self.peak_hold_data)

        # Draw main curve
        self.curve.setData(data["x"], data["y"])

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

    def peak_hold_clear(self):
        """Clear peak hold curve"""
        self.peak_hold_data = None
        self.curve_peak_hold.clear()


class WaterfallPlotWidget:
    """Waterfall plot"""
    def __init__(self, layout, histogram_layout=None):
        if not isinstance(layout, pg.GraphicsLayoutWidget):
            raise ValueError('layout must be instance of pyqtgraph.GraphicsLayoutWidget')

        if histogram_layout and not isinstance(histogram_layout, pg.GraphicsLayoutWidget):
            raise ValueError('histogram_layout must be instance of pyqtgraph.GraphicsLayoutWidget')

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
