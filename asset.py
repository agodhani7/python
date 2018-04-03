'''
asset class

Anuj Godhani
'''

class Asset(object):

    # initialize the class with initial value of the asset
    def __init__(self, ivalue):
        self._ivalue = ivalue

    # getter that returns initial value of the asset
    @property
    def ivalue(self):
        return self._ivalue

    # setter so the value of the asset can be changes just in case
    @ivalue.setter
    def ivalue(self, v):
        self._ivalue = v

    # returns depreciation of the asset
    # NotImplementedError ensures that no one can directly instantiate an Asset object
    def depr(self):
        raise NotImplementedError

    # returns monthly depreciation
    def monthlyDepr(self):
        return self.depr() / 12

    # returns current value of the asset at a time period
    def currentValue(self, period):
        totaldep = (1 + self.monthlyDepr())**period
        return self._ivalue * totaldep

# part b - creating a car class
class Car(Asset):

    def depr(self):
        d = 0.20
        return d

# creating HouseBase class derived from asset class
class HouseBase(Asset):
    pass

# PrimaryHome class derived from HouseBase class
class PrimaryHome(HouseBase):

    def depr(self):
        d = 0.2
        return d

# VacationHome derived from HouseBase class
class VacationHome(HouseBase):

    def depr(self):
        d = 0.12
        return d

