from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *

import sys
import warnings
import random

from stats.dists   import *
from stats.plot    import *
from stats.widgets import *

warnings.filterwarnings("ignore")

class main(QWidget):
    def __init__(self, **kwargs):
        QWidget.__init__(self)

        self.setStyleSheet("background-color: black")

        self.setLayout(QGridLayout())
        self.layout().setSpacing(0)

        self.layout().addWidget(widgets(self, dist = "Normal"), 0, 0)
        
        self.showFullScreen()

class widgets(QWidget):
    def __init__(self, parent, dist="Normal"):
        QWidget.__init__(self, parent)

        self.setLayout(QGridLayout())

        self._initDistWidgets(dist)
        self._initWidgets()

        self._colorCountLeft = 0
        self._colorCountRight = 0

    def _initDistWidgets(self, distribution):
        try:
            self.layout().itemAtPosition(1, 0).widget().setParent(None)
            self.layout().itemAtPosition(1, 1).widget().setParent(None)
            self.layout().itemAtPosition(2, 0).widget().setParent(None)
            self.layout().itemAtPosition(2, 1).widget().setParent(None)
        except:
            pass
        
        if distribution == "Normal":
            self._normMean     = -5
            self._normVariance = 3
            self._normSd       = sqrt(self._normVariance)

            _normMeanAcc = 100
            _normVarAcc  = 100

            self._data = normalDist(self._normMean, self._normVariance)
            
            self._meanSlider     = sliderAndLabel(self, -5*_normMeanAcc,  5*_normMeanAcc,  1, 0, text="μ: ",             textDiv=_normMeanAcc, initVal = self._normMean*_normMeanAcc)
            self._varianceSlider = sliderAndLabel(self, 0.01*_normVarAcc, 20*_normVarAcc,  2, 0, text="σ<sup>2</sup>: ", textDiv=_normVarAcc,  initVal = self._normVariance*_normVarAcc)

            self._meanSlider.valueChanged.connect     (lambda: self._plot.reDraw(normalDist(self._meanSlider.value()/_normMeanAcc, self._varianceSlider.value()/_normMeanAcc), self._barCheckBox.checkState(), self._lineCheckBox.checkState()))
            self._meanSlider.valueChanged.connect     (lambda: self._highlightRegions(self._highlightLeftCRBox.checkState(), self._highlightRightCRBox.checkState(), normalDist(self._meanSlider.value()/_normMeanAcc, self._varianceSlider.value()/_normVarAcc), significance=self._significanceSlider.value()/self._signifAcc))

            self._varianceSlider.valueChanged.connect (lambda: self._plot.reDraw(normalDist(self._meanSlider.value()/_normMeanAcc, self._varianceSlider.value()/_normVarAcc), self._barCheckBox.checkState(), self._lineCheckBox.checkState()))
            self._varianceSlider.valueChanged.connect (lambda: self._highlightRegions(self._highlightLeftCRBox.checkState(), self._highlightRightCRBox.checkState(), normalDist(self._meanSlider.value()/_normMeanAcc, self._varianceSlider.value()/_normVarAcc), significance=self._significanceSlider.value()/self._signifAcc))

        if distribution == "Binomial":
            self._binomTrials = 20
            self._binomProb   = 0.5

            _binomProbAcc = 100

            self._data = binomialDist(self._binomTrials, self._binomProb)

            self._trialsSlider = sliderAndLabel(self, 0,               100,             1, 0, text="Trials: ",       initVal = self._binomTrials)
            self._probSlider   = sliderAndLabel(self, 0*_binomProbAcc, 1*_binomProbAcc, 2, 0, text="Success rate: ", initVal = self._binomProb*_binomProbAcc, textDiv=_binomProbAcc)

            self._trialsSlider.valueChanged.connect(lambda: self._plot.reDraw(binomialDist(self._trialsSlider.value(), self._probSlider.value()/_binomProbAcc), self._barCheckBox.checkState(), self._lineCheckBox.checkState()))
            self._trialsSlider.valueChanged.connect(lambda: self._highlightRegions(self._highlightLeftCRBox.checkState(), self._highlightRightCRBox.checkState(), binomialDist(self._trialsSlider.value(), self._probSlider.value()/_binomProbAcc), significance=self._significanceSlider.value()/self._signifAcc))

            self._probSlider.valueChanged.connect  (lambda: self._plot.reDraw(binomialDist(self._trialsSlider.value(), self._probSlider.value()/_binomProbAcc), self._barCheckBox.checkState(), self._lineCheckBox.checkState()))
            self._probSlider.valueChanged.connect  (lambda: self._highlightRegions(self._highlightLeftCRBox.checkState(), self._highlightRightCRBox.checkState(), binomialDist(self._trialsSlider.value(), self._probSlider.value()/_binomProbAcc), significance=self._significanceSlider.value()/self._signifAcc))

        if distribution == "Poisson":
            self._poissonLambda = 5

            _poissonLambdaAcc = 100

            self._data = poissonDist(self._poissonLambda)

            self._lambdaSlider = sliderAndLabel(self, 0*_poissonLambdaAcc, 50*_poissonLambdaAcc, 1, 0, text="λ: ", initVal = self._poissonLambda*_poissonLambdaAcc, textDiv=_poissonLambdaAcc)

            self._lambdaSlider.valueChanged.connect(lambda: self._plot.reDraw(poissonDist(self._lambdaSlider.value()/_poissonLambdaAcc), self._barCheckBox.checkState(), self._lineCheckBox.checkState()))
            self._lambdaSlider.valueChanged.connect(lambda: self._highlightRegions(self._highlightLeftCRBox.checkState(), self._highlightRightCRBox.checkState(), poissonDist(self._lambdaSlider.value()/_poissonLambdaAcc), significance=self._significanceSlider.value()/self._signifAcc))

        if distribution == "Geometric":
            self._geomProb = 0.5

            _geomProbAcc = 1000

            self._data = geometricDist(self._geomProb)

            self._geomProbSlider = sliderAndLabel(self, 0*_geomProbAcc, 1*_geomProbAcc, 1, 0, text="Success rate: ", textDiv = _geomProbAcc, initVal = self._geomProb*_geomProbAcc)

            self._geomProbSlider.valueChanged.connect(lambda: self._plot.reDraw(geometricDist(self._geomProbSlider.value()/_geomProbAcc), self._barCheckBox.checkState(), self._lineCheckBox.checkState()))
            self._geomProbSlider.valueChanged.connect(lambda: self._highlightRegions(self._highlightLeftCRBox.checkState(), self._highlightRightCRBox.checkState(), geometricDist(self._geomProbSlider.value()/_geomProbAcc), significance=self._significanceSlider.value()/self._signifAcc))

    def _initWidgets(self):
        self._plot = plot(self._data, bars=1, connect=1, initColor = (0, 255, 0), reColor = (255, 0, 25))

        self._distComboBox = QComboBox(self)
        self._distComboBox.setStyleSheet("color: white")
        self._distComboBox.addItems(["Normal", "Binomial", "Poisson", "Geometric"])
        self._distComboBox.currentTextChanged.connect(lambda: self._initDistWidgets(self._distComboBox.currentText()))

        self.layout().addWidget(self._distComboBox, 0, 0)
        
        self._barCheckBox  = boxAndLabel(self, 3, 0, True,  "Show bars")
        self._lineCheckBox = boxAndLabel(self, 4, 0, True, "Show lines")

        self._barCheckBox.stateChanged.connect(lambda: self._plot.plotBars(self._barCheckBox.checkState()))
        self._barCheckBox.stateChanged.connect(lambda: self._plot.reDraw(self._data, self._barCheckBox.checkState(), self._lineCheckBox.checkState()))
        self._barCheckBox.stateChanged.connect(lambda: self._highlightRegions(self._highlightLeftCRBox.checkState(), self._highlightRightCRBox.checkState(), self._data, significance=self._significanceSlider.value()/self._signifAcc)) 
        
        self._lineCheckBox.stateChanged.connect(lambda: self._plot.reDraw(self._data, self._barCheckBox.checkState(), self._lineCheckBox.checkState()))
        self._lineCheckBox.stateChanged.connect(lambda: self._plot.plotLines(self._lineCheckBox.checkState()))
        self._lineCheckBox.stateChanged.connect(lambda: self._highlightRegions(self._highlightLeftCRBox.checkState(), self._highlightRightCRBox.checkState(), self._data, significance=self._significanceSlider.value()/self._signifAcc)) 

        self._highlightLeftCRBox  = boxAndLabel(self, 5, 0, False, "Highlight left critical region")
        self._highlightRightCRBox = boxAndLabel(self, 6, 0, False, "Highlight right critical region")

        self._highlightLeftCRBox.stateChanged.connect (lambda: self._highlightRegions(self._highlightLeftCRBox.checkState(), self._highlightRightCRBox.checkState(), self._data, significance=self._significanceSlider.value()/self._signifAcc))
        self._highlightRightCRBox.stateChanged.connect(lambda: self._highlightRegions(self._highlightLeftCRBox.checkState(), self._highlightRightCRBox.checkState(), self._data, significance=self._significanceSlider.value()/self._signifAcc))

        if not self._barCheckBox.checkState():  self._plot.window.removeItem(self._plot.barGraph)
        if not self._lineCheckBox.checkState(): self._plot.window.removeItem(self._plot.curve)

        self._highlightMeanBox = boxAndLabel(self, 7, 0, False, "Highlight mean")

        self._highlightMeanBox.stateChanged.connect(lambda: self._plot.colorExp(self._highlightMeanBox.checkState(), self._data))
        
        self._signifAcc = 1000
        
        self._significanceSlider = sliderAndLabel(self, 0*self._signifAcc, 1*self._signifAcc, 8, 0, text="Significance: ", textDiv = self._signifAcc, initVal = 0.05*self._signifAcc)

        self._significanceSlider.valueChanged.connect(lambda: self._highlightRegions(self._highlightLeftCRBox.checkState(), self._highlightRightCRBox.checkState(), self._data, significance=self._significanceSlider.value()/self._signifAcc))

        self._plotColorSlider = sliderAndLabel(self, 0, 359, 9, 0, text="Hue: ")
        self._plotColorSlider.valueChanged.connect(lambda: self._reColor(self._plotColorSlider.value()))
                
        self.parent().layout().addWidget(self._plot.window, 0, 1)

    def _reColor(self, color):
        initColor = QColor.fromHsl((125+color)%360,  255, 128)
        reColor   = QColor.fromHsl(color,            255, 128)
        expColor  = QColor.fromHsl((225+color)%360, 255, 128)

        brushesArr = self._plot.barGraph.opts["brushes"]

        for i in range(len(brushesArr)):
            if   brushesArr[i] == self._plot.initColor: brushesArr[i] = initColor
            elif brushesArr[i] == self._plot.reColor:   brushesArr[i] = reColor
            elif brushesArr[i] == self._plot.expColor:  brushesArr[i] = expColor

        self._plot.initColor = initColor
        self._plot.reColor   = reColor
        self._plot.expColor  = expColor
        
        self._plot.barGraph.setOpts(brushes = brushesArr)

    def _highlightRegions(self, leftRegion, rightRegion, data, significance):
        self._data = data
        
        if leftRegion and not rightRegion:
            self._plot.colorRegion(False)
            self._plot.colorRegion(True, valueFrom=self._data.criticalRegionLeft(significance))
        if rightRegion and not leftRegion:
            self._plot.colorRegion(False)
            self._plot.colorRegion(True, valueTo=self._data.criticalRegionRight(significance))
        if leftRegion and rightRegion:
            self._plot.colorRegion(False)
            self._plot.colorRegion(True, valueFrom=self._data.criticalRegionLeft(significance), valueTo=self._data.criticalRegionRight(significance))
        if not leftRegion and not rightRegion:
            self._plot.colorRegion(False)

        self._plot.colorExp(self._highlightMeanBox.checkState(), self._data)            

def excepthook(e, v, t):
    return sys.__excepthook__(e, v, t)

sys.excepthook = excepthook

if __name__ == "__main__":
    app = QApplication([])
    m = main()
    app.exec_()
