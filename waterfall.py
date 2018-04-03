'''
creating doWaterfall function

Anuj Godhani
'''

#from loan.pool import LoanPool
from securities import StructuredSecurities
from ratings import ABSRating

# define
def doWaterfall(loanPool, securities):

    # checks if the parameters are of valid class
    #assert isinstance(loanPool, LoanPool), 'Invalid loanPool object'
    assert isinstance(securities, StructuredSecurities), "Invalid securities object"

    # tracks time periods
    period = 0
    # tracks loan pool waterfalls
    lp_waterfalls = []
    # tracks securities waterfall
    sc_waterfalls = []
    # tracks reserve cash if any
    reserve_cash = []

    # checks active loans in the loan pool
    while loanPool.activeLoans(period) > 0:
        # check defaults
        recovery = loanPool.checkDefaults(period)
        # total payments
        cash = loanPool.totalPaymentDue(period)
        # pay cash to securities
        securities.makePayments(cash + recovery, loanPool.totalPrincipalDue(period))

        # call waterfall on structured securities
        sc_waterfalls.append(securities.getWaterfall())

        # call waterfall on loan pool and append it to the list
        lp_waterfalls.append(loanPool.getWaterfall(period))

        # append reserve cash
        reserve_cash.append(securities.reservedAccount)

        # increase time period
        securities.increaseTimePeriod()
        # increase time period
        period += 1

    tr_payments = [[] for i in xrange(len(securities._tr_list))]

    for period_wfs in sc_waterfalls:

        for tr_idx, tr_wf in enumerate(period_wfs):

            tr_payments[tr_idx].append(tr_wf[1] + tr_wf[3])  # get payments for each tranche

    tr_metrics = [(tr.IRR(payments), tr.DIRR(payments), tr.AL(payments), ABSRating(tr.DIRR(payments))) for tr, payments
                  in zip(securities._tr_list, tr_payments)]  # get metrics

    return tr_metrics, lp_waterfalls, sc_waterfalls, reserve_cash
