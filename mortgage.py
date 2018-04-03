'''
2.2.7
updating MortgageMixin

Anuj Godhani
'''

import asset

class MortgageMixin(object):
    # add home to initialization
    def __init__(self, home, face, rate, startdate, enddate):
        # check if home is a home class object
        if isinstance(home, asset.HouseBase) == True:
            # super loan base class for the asset
            self._asset = home
            super(MortgageMixin, self).__init__(home, face, rate, startdate, enddate)
        else:
            raise Exception('Error: enter a valid HouseBase object')

    # modifying PMI to calculate based on LTV
    def PMI(self):
        if self._face/self._home._ivalue <= 0.8:
            return 0.000075 * self._face
        # if LTV is greater than 80% then PMI is 0
        else:
            return 0

    # new formula to include PMI
    def monthlyPayment(self):
        # super the method in loan base class
        x = super(MortgageMixin, self).monthlyPayment()
        # add PMI to the original formula
        pmt = (self._face * self.rate()) / (1 - (1 + self.rate()) ** (- self.term)) + self.PMI()
        return x if self.PMI() == 0 else pmt

    # new formula to use new monthlypayment
    def principalDue(self, n):
        # super the method in loan base class
        super(MortgageMixin, self).principalDue(n)
        # for t=0 we don't have any principal due
        if n > 0:
            pdue = self.monthlyPayment() - self.interestDue(n)
            return pdue
        else:
            return None

