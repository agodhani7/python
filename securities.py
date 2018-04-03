'''
creating StructuredSecurities class

Anuj Godhani
'''

from tranches import *


class StructuredSecurities(object):
    # initialize
    def __init__(self, totalNotional):
        self._total_ntl = totalNotional
        # manage all tranches in a list
        self._tr_list = []
        # setting the mode to sequential. can be changed later
        self._mode = 'Sequential'
        # maintain a reserved account that is balance left after making payments
        self._reserved_account = 0

    @property
    def reservedAccount(self):
        return self._reserved_account

    # this method adds tranches to our list
    # takes the class, rate, flag and notional percent as arguments
    def addTranche(self, cls, ntl_per, rate, subLevel):
        # check if the cls is a Tranche class object
        if issubclass(cls, Tranche) == False:
            raise Exception('Input class type must be a tranche')
        else:
            new_tr = cls(ntl_per * self._total_ntl, ntl_per, rate, subLevel)
        # append the list
        self._tr_list.append(new_tr)
        # sort the list based on subordination level
        self._tr_list = sorted(self._tr_list, key=lambda x: x._subLevel)

    # change mode
    def changeMode(self, mode):
        # check if its a valid mode
        assert mode in {'Sequential', 'Pro-Rata'}, 'Invalid choice of mode'
        # change the mode
        self._mode = mode

    # increase time period for all tranches
    def increaseTimePeriod(self):
        for tr in self._tr_list:
            tr.increaseTimePeriod()

    # make payments as per the guidelines
    def makePayments(self, cash_amount, principalcollections):
        # the amount of money we have will be sum of cash amount and reserved account
        cash_left = cash_amount + self._reserved_account
        # loop through the tranches
        for tr in self._tr_list:
            # if a tranche has notional balance
            if tr.notionalBalance > 0:
                # pay interest and set our cash left accordingly. any shortages gets recorded in interest shortfall
                cash_left = tr.makeInterestPayment(cash_left)

        # now check if we have any cash left
        if cash_left > 0:
            # payment as per the mode
            if self._mode == 'Sequential':
                # look through the sorted list
                for tr in self._tr_list:
                    tr._prpCollections = principalcollections
                    # if there is notional balance and we have cash left - pay principal
                    if tr.notionalBalance > 0 and cash_left > 0:
                        cash_left = tr.makePrincipalPayment(cash_left)

            elif self._mode == 'Pro-Rata':
                # maintain cah left
                temp_cash_left = 0
                # loop through the tranches
                for tr in self._tr_list:
                    tr.flag = 'Pro-Rata'
                    tr._prpCollections = principalcollections
                    if tr.notionalBalance > 0:
                        # make principal payments based on notional percent. If any tranche returns positive balance,
                        # store it in temporary cash left
                        temp_cash_left += tr.makePrincipalPayment(cash_left)
                # after looping, set temporary cash left to cash left
                cash_left = temp_cash_left

        # after making payments, set the reserved account to the cash left
        self._reserved_account = cash_left

    # todo: keep this or not?
    #def totalInterestDue(self):
        #return sum(tr.interestDue() for tr in self._tr_list)

    # define waterfall
    def getWaterfall(self):
        # create a list of lists. one for each tranche
        sw = [[tr.intDue, tr.interestPaid, tr.interestShortfall, tr.principalPaid, tr.notionalBalance] for tr in self._tr_list]

        return sw

    # todo: keep this or not?
    def reset(self):
        self._reserved_account = 0
        for tr in self._tr_list:
            tr.reset()