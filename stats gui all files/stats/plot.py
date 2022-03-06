import pyqtgraph as pg

from scipy.interpolate import interp1d

import sys
import random

class plot():
    def __init__(self, data = [], initColor = (0, 255, 25), reColor = (255, 25, 0), expColor=(25, 0, 255), backgroundColor = (0,0,5), bars=1, connect=0):
        self.window = pg.plot()

        self.window.setBackground(pg.mkBrush(backgroundColor))

        self.data      = data
        self.initColor = pg.mkBrush(initColor)
        self.reColor   = pg.mkBrush(reColor)
        self.expColor  = pg.mkBrush(expColor)

        self._drawBars  = bars
        self._drawLines = connect

        self.x = range(len(self.data))

        if self._drawBars:  self.plotBars(True)
        if self._drawLines: self.plotLines(True)

        self.colorRegion(False)

    def reDraw(self, newData, drawBars, drawLines):
        self.data = newData
        
        if drawBars:
            self.barGraph.setOpts(x=list(range(len(self.data))), height=self.data, brushes=[self.initColor for i in range(len(self.data))])
            
        if drawLines:
            self.x = list(range(len(newData)))
            self.plotLines(True)

    def plotBars(self, barsBool):
        if barsBool:
            self.barGraph = pg.BarGraphItem(x=self.x, height=self.data, width=1, brushes=[self.initColor for i in range(len(self.data))])
                    
            self.window.addItem(self.barGraph)
        else:
            try: self.window.removeItem(self.barGraph)
            except: pass
        
    def plotLines(self, linesBool):
        if linesBool:
            try: self.window.removeItem(self.curve)
            except: pass
            
            func = interp1d(x=self.x, y=self.data, kind=2)

            _newX = []

            for i in range((len(self.x)-1)*1000): _newX.append(i/1000)

            _newY = func(_newX)
            
            self.curve  = pg.PlotDataItem(_newX, _newY, connect="all")
            self._spacer = pg.PlotDataItem([1],   [1])

            self.window.addItem(self.curve)
            self.window.addItem(self._spacer)
        else:
            try:    self.window.removeItem(self.curve)
            except: pass

    def colorExp(self, colorUncolor, data):
        for i in range(len(data)):
            if i == data.index(max(data)):
                if colorUncolor: self.barGraph.opts["brushes"][i] = self.expColor
                else: self.barGraph.opts["brushes"][i] = self.initColor

        self.barGraph.setOpts(brushes = self.barGraph.opts["brushes"])
            
    def colorRegion(self, colorUncolor, valueFrom=0, valueTo=None):
        if not valueTo: valueTo = len(self.data)
        
        brushesArr = []
        
        for i in range(len(self.data)):
            brushesArr.append(None)
            
            if colorUncolor:
                try:
                    if i >= valueFrom and i <= valueTo: brushesArr[i] = self.initColor
                    else:                               brushesArr[i] = self.reColor
                except:
                    pass
                
            elif not colorUncolor:
                brushesArr[i] = self.initColor

        self.barGraph.setOpts(brushes = brushesArr)

class plotMulti():
    def __init__(self, dataList = [[]], colorList = [[]], backgroundColor = (0, 0, 5)):
        _window = pg.plot()

        _window.setBackground(pg.mkBrush(backgroundColor))

        self.dataList  = dataList
        self._colorList = []
        
        if len(colorList) == len(dataList):
            for i in colorList: self._colorList.append(pg.mkBrush(i))

        else:
            while len(colorList) != len(dataList):
                self._colorList.append((random.randint(0, 255),
                                        random.randint(0, 255),
                                        random.randint(0, 255),
                                        100))

        for i in self.dataList:
            _barGraph = pg.BarGraphItem(x=range(len(i)), height=i, width=1, brush=self._colorList[self.dataList.index(i)])
            _window.addItem(_barGraph)

        _window.showFullScreen()

class plotBivariate():
    def __init__(self, data1 = [], data2 = [], mainColor = (0, 255, 25), backgroundColor = (0,0,5)):
        self.window = pg.plot()

        self.window.setBackground(pg.mkBrush(backgroundColor))

        self._color = pg.mkBrush(mainColor)

        self.data1 = data1
        self.data2 = data2

        self.scatterPlot = pg.ScatterPlotItem(x=self.data1, y=self.data2, brush=self._color)

        self.window.addItem(self.scatterPlot)

        self.window.showFullScreen()

def excepthook(e, v, t):
    return sys.__excepthook__(e, v, t)

sys.excepthook = excepthook
