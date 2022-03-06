from math import *
import sys

##from .errors import *

class geometricDist(list):
    def __init__(self, successRate, accuracy = 4, trials = 50):
        self.trials      = trials
        self.successRate = successRate
        self.accuracy    = accuracy

        if self.successRate < 0 or self.successRate > 1: raise ProbabilityError()

        for i in range(1,self.trials+2):
            self.append(self.probability(i))

    def probability(self, value):
        return round(((1-self.successRate)**(value-1)) * self.successRate, self.accuracy)

    def expectation(self):
        return round(1/self.successRate, self.accuracy)

    def variance(self):
        return round((1-self.successRate)/self.successRate**2, self.accuracy)

    def sd(self):
        return sqrt(self.variance)

    def cumulativeProbability(self, probFrom = 0, probTo = None):
        if not probTo: probTo = self.trials
        probTo += 1
        return round(sum(self[probFrom:probTo]), self.accuracy)

    def criticalRegionLeft(self, significance):
        _tempSum = 0
        
        for i in range(len(self)-1):
            if _tempSum > significance: return i-1
            else: _tempSum += self[i]

    def criticalRegionRight(self, significance):
        _tempSum = 0

        for i in range(len(self)-1, 0, -1):
            if _tempSum > significance: return i+1
            else: _tempSum += self[i]

class binomialDist(list):
    def __init__(self, trials, successRate, accuracy = 4):
        self.trials      = trials
        self.successRate = successRate
        self.accuracy    = accuracy

        if self.successRate < 0 or self.successRate > 1: raise ProbabilityError()

        for i in range(self.trials+1):
            self.append(round(self.probability(i), self.accuracy))

    def _ncr(self, n, r):
        return factorial(n)/(factorial(r) * factorial(n-r))

    def probability(self, value):
        return round(self._ncr(self.trials, value) * self.successRate**value * (1-self.successRate)**(self.trials-value), self.accuracy)

    def expectation(self):
        return round(self.trials * self.successRate, self.accuracy)

    def variance(self):
        return round(self.trials * self.successRate * (1-self.successRate), self.accuracy)

    def sd(self):
        return sqrt(self.variance)

    def cumulativeProability(self, probFrom = 0, probTo = None):
        if not probTo: probTo = self.trials
        probTo += 1
        return round(sum(self[probFrom:probTo]), self.accuracy)

    def criticalRegionLeft(self, significance):
        _tempSum = 0
        
        for i in range(len(self)):
            if _tempSum > significance: return i-1
            else: _tempSum += self[i]

    def criticalRegionRight(self, significance):
        _tempSum = 0

        for i in range(len(self)-1, 0, -1):
            if _tempSum > significance: return i+1
            else: _tempSum += self[i]

class poissonDist(list):
    def __init__(self, lambdaValue, accuracy = 4, trials = 50):
        self.lambdaValue = lambdaValue
        self.accuracy    = accuracy
        self.trials      = trials

        for i in range(self.trials+1):
            self.append(self.probability(i))

    def probability(self, value):
        return round((self.lambdaValue**value * e**-self.lambdaValue)/(factorial(value)), self.accuracy)

    def expectation(self):
        return round(self.lambdaValue, self.accuracy)

    def variance(self):
        return round(self.lambdaValue, self.accuracy)

    def sd(self):
        return sqrt(self.variance)

    def cumulativeProbability(self, probFrom = 0, probTo = None):
        if not probTo: probTo = self.trials
        probTo += 1
        return round(sum(self[probFrom:probTo]), self.accuracy)

    def criticalRegionLeft(self, significance):
        _tempSum = 0
        
        for i in range(len(self)):
            if _tempSum > significance: return i-1
            else: _tempSum += self[i]

    def criticalRegionRight(self, significance):
        _tempSum = 0

        for i in range(len(self)-1, 0, -1):
            if _tempSum > significance: return i+1
            else: _tempSum += self[i]

class normalDist(list):
    def __init__(self, mean, variance, accuracy = 4, trials = 50):
        self.mean     = mean
        self.variance = variance
        self.sd       = sqrt(variance)
        self.accuracy = accuracy
        self.trials   = trials

        for i in range(-self.trials//2, (self.trials+1)//2):
            self.append(self.probability(i))

    def probability(self, value):
        return (1/(self.sd * sqrt(2*pi))) * e**(-0.5 * ((value-self.mean)/self.sd)**2)

    def expectation(self):
        return self.mean

    def variance(self):
        return self.variance

    def sd(self):
        return sqrt(self.variance)

    def cumulativeProbability(self, probFrom = 0, probTo = None):
        if not probTo: probTo = self.trials
        probTo += 1
        return round(sum(self[probFrom:probTo]), self.accuracy)

    def criticalRegionLeft(self, significance):
        _tempSum = 0
        
        for i in range(len(self)-1):
            if _tempSum > significance: return i-1
            else: _tempSum += self[i]

    def criticalRegionRight(self, significance):
        _tempSum = 0

        for i in range(len(self)-1, 0, -1):
            if _tempSum > significance: return i+1
            else: _tempSum += self[i]

def excepthook(e, v, t):
    return sys.__excepthook__(e, v, t)

sys.excepthook = excepthook
