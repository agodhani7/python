'''
2.2.1
creating fixedrateloan and variablerateloan derived from Loan class

Anuj Godhani
'''

from loan_base import Loan
import asset
from mortgage import MortgageMixin

# derived from Loan so takes Loan instead of object as argument
class FixedRateLoan(Loan):
    def rate(self, period=None):
        return self._rate

# derived from Loan class
class VariableRateLoan(Loan):

    # initialize this derived class with rateDict
    def __init__(self, Asset, face, rateDict, term):
        self._ratDict = rateDict
        # we super the rate in loan base
        super(VariableRateLoan, self).__init__(Asset, face, None, term)

    # method to return rate for a given period
    def rate(self, period=0):
        # search through the dictionary to find an appropriate key for a given period
        key = max([key for key, value in self._ratDict.iteritems() if key <= period])
        # return the value for the key
        return self._ratDict[key]


class AutoLoan(Loan):
    # initialize with car
    def __init__(self, car, face, rate, term):
        # check if car is a Car class object
        if isinstance(car, asset.Car) == True:
            super(AutoLoan, self).__init__(car, face, rate, term)
            self._asset = car
        else:
            raise Exception('Error: enter a valid car object')

class VariableMortgage(MortgageMixin, VariableRateLoan):
    pass

# derived from MortgageMixin and FixedRateLoan
class FixedMortgage(MortgageMixin, FixedRateLoan):
    pass
