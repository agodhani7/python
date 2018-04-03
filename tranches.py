'''
creating tranche class

Anuj Godhani
'''

import logging
import numpy as np

# create the class
class Tranche(object):

    # initialize the class with notional and rate
    def __init__(self, notional, notionalPercent, rate, subLevel):
        self._notional = notional
        self._annualRate = rate
        self._rate = rate/12.0
        self._subLevel = subLevel
        self._ntl_per = notionalPercent
        # set flag default to Sequential
        self._flag = 'Sequential'

    @property
    def notional(self):
        return self._notional

    @property
    def ntlper(self):
        return self._ntl_per

    @property
    def rate(self):
        return self._annualRate

    @property
    def subLevel(self):
        return self._subLevel

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, f):
        self._flag = f

    def IRR(self, payments):
        return np.irr([-self.notional] + payments) * 12

    def DIRR(self, payments):
        return self.rate - self.IRR(payments)

    def AL(self, payments):
        return sum((i + 1) * payments[i] for i in xrange(len(payments))) / self.notional


# create a derived class
class StandardTranche(Tranche):
    # initialize and super the base class
    def __init__(self, notional, notionalPercent, rate, subLevel):
        super(StandardTranche, self).__init__(notional, notionalPercent, rate, subLevel)
        # set current time equal to 0
        self._cur_time = 0
        # set current notional balance to notional
        self._cur_ntl_balance = self._notional
        # set current interest due to 0
        self._cur_int_due = 0
        # set current interest shortfall to 0
        self._cur_int_shortfall = 0
        # set current interest paid to 0
        self._cur_int_paid = 0
        # set current principal paid to 0
        self._cur_prp_paid = 0
        # we will define principal due later
        self._cur_prp_due = 0
        # principal shortfall
        self._cur_prp_shortfall = 0
        # will set principal due in waterfall
        self._prpCollections = 0




    @property
    def notionalBalance(self):
        return self._cur_ntl_balance

    @property
    def intDue(self):
        return self._cur_int_due

    @property
    def interestPaid(self):
        return self._cur_int_paid

    @property
    def principalPaid(self):
        return self._cur_prp_paid

    @property
    def interestShortfall(self):
        return self._cur_int_shortfall

    @property
    def prpDue(self):
        return self._cur_prp_due

    @prpDue.setter
    def prpDue(self, pdue):
        self._cur_prp_due = pdue

    @property
    def principalShortfall(self):
        return self._cur_prp_shortfall


    # this method increases time period by 1 and changes the related variables that changes with time
    def increaseTimePeriod(self):
        # increase current time by 1
        self._cur_time += 1
        # set current interest due to rate times notional balance of the last period,
        # plus any interest shortfall from the last period
        self._cur_int_due = self._rate * self._cur_ntl_balance + self._cur_int_shortfall
        # principal due depends on the principal received
        self._cur_prp_due = min(self._cur_prp_shortfall + self._prpCollections, self._cur_ntl_balance) if \
            self._flag == 'Sequential' else min(self._cur_ntl_balance, self._ntl_per * self._prpCollections + self._cur_prp_shortfall)
        # now, set interest shortfall, interest and principal paid to 0 because we havent paid anything with this method
        self._cur_int_shortfall = 0
        self._cur_int_paid = 0
        self._cur_prp_paid = 0
        self._cur_prp_shortfall = 0

    # this method makes principal payments
    # takes amount as an argument
    def makePrincipalPayment(self, amount):
        # if current principal paid log a warning
        if self._cur_prp_paid > 0:
            logging.info("Principal already paid!")
            return amount
        # if the notional balance is 0, we dont need to pay anything
        elif self._cur_ntl_balance == 0:
            logging.info("Current notional balance is 0. Payment not accepted!")
            return amount
        # else make a payment
        else:
            # set current principal paid to min of balance and amount
            self._cur_prp_paid = min(self._cur_prp_due, amount)
            # shortfall
            self._cur_prp_shortfall = self._cur_prp_due - self._cur_prp_paid
            # reduce the current notional balance by the amount of principal paid
            self._cur_ntl_balance -= self._cur_prp_paid
        return amount - self._cur_prp_paid  # return cash left after payment

    # this method makes interest payment
    # takes amount as an argument
    def makeInterestPayment(self, amount):
        # if interest already paid, log an error
        if self._cur_int_paid > 0:
            logging.info("Interest already paid at this time period!")
            return amount
        # if no interest is due, log a warning
        elif self._cur_int_due == 0:
            logging.info("Current interest due is 0. Payment not accepted!")
            return amount
        # make the payment
        else:
            # interest paid will be min of interest due and the amount
            self._cur_int_paid = min(self._cur_int_due, amount)
            # if interest not paid in full, store the difference in current interest shortfall
            self._cur_int_shortfall = self._cur_int_due - self._cur_int_paid  # record shortfall
        # return the amount left
            return amount - self._cur_int_paid

    # reset everything
    def reset(self):
        self._cur_time = 0
        self._cur_ntl_balance = self._notional
        self._cur_int_due = 0
        self._cur_int_shortfall = 0
        self._cur_int_paid = 0
        self._cur_prp_paid = 0
        self._cur_prp_due = 0
        self._cur_prp_shortfall = 0
        self._prpCollections = 0

