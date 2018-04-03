'''
updating LoanPool class

Anuj Godhani
'''

from loan_base import Loan
import asset
import csv
import loans
import numpy as np

class LoanPool(object):
    def __init__(self, *args):
        self.args = args
        # start with i = -1
        self.i = -1

    def __iter__(self):
        return self

    # next will help iterate through the loanpool object
    def next(self):
        # if the current position is within the length of the *args we proceed
        if self.i < len(self.args) -1:
            # add 1 to i and index the loan
            self.i += 1
            return self.args[self.i]
        # if we reach the length of *args, stop the iteration
        else:
            # setting it back to -1 so we can iterate through the object again
            self.i = -1
            raise StopIteration()

    default_periods = [1, 11, 60, 120, 180, 210]
    default_rates = [0.0005, 0.001, 0.002, 0.004, 0.002, 0.001]

    def totalPrincipal(self):
        return sum(l.face for l in self.args if not l.defaulted)

    def totalBalance(self, n):
        return sum(l.balance(n) for l in self.args if not l.defaulted)

    def totalPrincipalDue(self, n):
        return sum(l.principalDue(n) for l in self.args if not l.defaulted)

    def totalInterestDue(self, n):
        return sum(l.interestDue(n) for l in self.args if not l.defaulted)

    def totalPaymentDue(self, n):
        return sum(l.monthlyPayment(n) for l in self.args if not l.defaulted)

    def activeLoans(self, n):
        return len([l for l in self.args if l.balance(n) > 0 and not l.defaulted])

    def WAR(self):

        x = [loan.face for loan in self.args]
        y = [loan.face * loan.rate() for loan in self.args]
        war = sum(y) / float(sum(x))
        return str(round(war, 4) * 100) + '%'

    def WAM(self):
        x = [loan.face for loan in self.args]
        y = [loan.face * loan.term for loan in self.args]
        wam = sum(y) / float(sum(x))
        return str(round(wam, 2)) + ' months'

    def getWaterfall(self, n):
        lw = [[loan.monthlyPayment(n), loan.principalDue(n), loan.interestDue(n), loan.balance(n)] for loan in self.args]

        return lw

    def checkDefaults(self, n):

        rate_index = 0 if n==0 else LoanPool.default_periods.index(max([i for i in LoanPool.default_periods if i <= n])) # get the corresponding interval

        default_prob = 0 if n==0 else LoanPool.default_rates[rate_index]  # default rate

        # default flag ~ B(default rate)
        defaults = np.asarray(np.random.uniform(size=len(self.args)) > default_prob, dtype=int)
        recover_amount = 0
        for l, default in zip(self.args, defaults):
            if l.defaulted:
                continue
            l.checkDefault(default)
            if l.defaulted:
                recover_amount += l.recoveryValue(n)
        return recover_amount

    def reset(self):
        for l in self.args:
            l.reset()




# load loans from CSV file and create a loan pool object
def poolCSV(file_path):
    with open(file_path, 'r') as f:
        f = csv.reader(f, delimiter=',')
        # skip first row
        header = next(f, None)
        loanlist = []
        for line in f:
            loan_id, loan_type, face, rate, term, asset_type, asset_value = line[0], line[1], line[2], line[3], line[4], line[5], line[6]
            loan_type = ''.join(loan_type.strip().split(' '))
            face = float(face)
            rate = float(rate)
            term = int(term)
            asset_value = float(asset_value)
            asset_obj = getattr(asset, asset_type)(asset_value)
            loan_obj = getattr(loans, loan_type)(asset_obj, face, rate, term)

            loanlist.append(loan_obj)

    def wrapper(func, args):
        return func(*args)

    return wrapper(LoanPool, loanlist)
