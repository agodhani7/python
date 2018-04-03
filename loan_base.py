'''
5.2.3
updating loan base class

Anuj Godhani
'''

import asset
import logging
from functools import wraps


class Loan(object):

    # initializing with asset
    def __init__(self, Asset, face, rate, term):
        self._term = term
        self._rate = rate
        self._face = face
        # checking if asset us an Asset class object
        if isinstance(Asset, asset.Asset) == True:
            self._asset = Asset
        else:
            # part a
            logging.error('not an asset class')
            raise Exception('Error: enter a valid asset object')
        self._defaulted = False

    # the getters and setters
    @property
    def term(self):
        return self._term

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, ir):
        self._rate = ir

    @property
    def face(self):
        return 0 if self._defaulted else self._face

    @face.setter
    def face(self, ifa):
        self._face = ifa

    # 2.2.1 we use this rate method from now on. default period is 0
    def rate(self, period=0):
        return self._rate

    @property
    def defaulted(self):
        return self._defaulted

    # 2.1.4
    # define classmethod using decorators
    @classmethod
    # monthly payment takes face, rate and term as parameters
    def calcMonthlyPmt(cls, face, rate, term):
        pmt = (face * rate) / (1 - (1 + rate)**(-term))
        logging.debug('calculating pmt')
        return pmt

    # function to calculate balance
    @classmethod
    def calcBalance(cls, face, rate, term, period):
        bal = (face * (1 + rate) ** period) - Loan.calcMonthlyPmt(face, rate, term) * (((1 + rate) ** period - 1) / rate)

        if period > term:
            logging.info('n is greater than term')
            return 0

        elif bal > 0:
            logging.debug('calculating bal')
            return bal
        else:
            logging.debug('balance is 0')
            return 0

    # 2.1.4 part d
    def monthlyPayment(self, period = 1):
        if period == 0:
            return 0
        else:
            return 0 if self._defaulted else self.calcMonthlyPmt(self._face, self.rate(period), self.term)


    def totalPayments(self):
        return self.monthlyPayment() * self.term

    # we define the total interest function as total payments less the principal amount
    def totalInterest(self):
        return self.totalPayments() - self._face

    def balance(self, n):

        if n > self.term:
            logging.info('n is greater than term')
            return 0
        elif self._defaulted:
            logging.info("Loan defaulted")
            return 0
        else:
            logging.debug('calculating balance')
            return self.calcBalance(self._face, self.rate(n), self.term, n)

    def interestDue(self, n):
        # we know that for t=0 we don't have any interest due. So, the if condition is to ensure
        # that the function returns None for t or n less than 0
        if n > self.term:
            logging.info('n is greater than term')
            return 0

        elif n > 0:
            idue = self.balance(n-1) * self.rate(n)
            if idue >= 0:
                logging.debug('calculating interest due')
                return idue
            else:
                logging.debug(0)
                return 0
        else:
            logging.info('n is less than 0')
            return 0

    def principalDue(self, n):
        # for t=0 we don't have any principal due
        if n > self.term:
            logging.info('n is greater than term')
            return 0

        elif n > 0:
            pdue = self.monthlyPayment() - self.interestDue(n)
            if pdue >= 0:
                logging.debug('calculating principal due')
                return pdue
            else:
                return 0
        else:
            logging.info('n is less than 0')
            return 0


    @staticmethod
    def monthlyRate(annualrate):
        return annualrate/12

    # returns an annual rate for a passed-in monthly rate
    @staticmethod
    def annualRate(monthlyrate):
        return monthlyrate*12

    # 2.2.7
    # recoveryValue returns the current asset value for the given period, times a recovery multiplier of 0.6.
    def recoveryValue(self, n):
        logging.debug('calculating current value')
        return 0.6 * self._asset.currentValue(n)

    # equity returns the available equity (the asset value less the loan balance)
    def equity(self, n):
        logging.debug('calculating equity')
        return self._asset.currentValue(n) - self.balance(n)

    def checkDefault(self, flag):
        if flag == 0:
            self._defaulted = True

    def reset(self):
        self._defaulted = False
