'''
monte carlo and associated functions

Anuj Godhani
'''

from ABS.waterfall import doWaterfall
import numpy as np
import logging
from ABS.securities import StructuredSecurities
from ABS.tranches import StandardTranche
import multiprocessing
from tabulate import tabulate

def simulateWaterfall(queue, loanPool, securities, SIM):
    # records DIRR & AL for each tranche
    metric_records = np.zeros((2, 2))

    # for each simulation, it resets both objects and gets metrics from the waterfall
    for i in xrange(SIM):
        loanPool.reset()
        securities.reset()
        # logging.info("Simulation {}".format(i))
        try:
            tr_metrics, lp_waterfall, ss_waterfall, res_amounts = doWaterfall(loanPool, securities)

            # for each simulation, add DIRR and AL to our array
            for j, metric in enumerate(tr_metrics):
                metric_records[j] += [metric[1], metric[2]]
        except:
            pass

    # return the sum not the average
    queue.put(metric_records)

# creates securities based on tranche data
def makeSecurities(notional, percents, rates, sub_levels):
    ss = StructuredSecurities(notional)
    for percent, rate, level in zip(percents, rates, sub_levels):
        ss.addTranche(StandardTranche, percent, rate, level)
    return ss


# calculated yields based on the formula given
def calcYields(dirr, wal):
    return .01*(7.0/(1 + .08*np.exp(-.19*wal/12.0)) + .19 * np.sqrt(wal/12.0*dirr*100.0))


# creates processes and returns final average values of DIRR and AL
def runSimulationParallel(loanPool, securities, NSIM, numProcesses = 20):

    # a single queue object to where the returned values from simulateWaterfall will be put
    queue = multiprocessing.Queue()

    num_sims_per_process = int(NSIM/float(numProcesses))

    processes = [multiprocessing.Process(target=simulateWaterfall, args=(queue, loanPool, securities, num_sims_per_process))
                 for i in range(numProcesses)]

    for p in processes:
        p.start()

    for p in processes:
        p.join(timeout=1)

    # store the result in a array
    result = np.zeros((2,2))

    r = [queue.get() for i in range(numProcesses)]

    for res in r:
        result += res

    # return the average values
    return result/float(NSIM)


# run monte function
def runMonte(loanPool, NSIM, tolerance):
    # tranche data
    percents = np.array([0.8, 0.2])
    rates = np.array([0.05, 0.08])
    levels = [1, 2]
    step_sizes = np.array([1.2, 0.8])
    # measures the diff
    diff = np.inf
    # number of iterations
    ii = 0
    # infinite loop
    while np.abs(diff) > tolerance:
        print "Iteration {}, rates {}".format(ii, rates)
        securities = makeSecurities(loanPool.totalPrincipal(), percents, rates, levels)
        # we set 20 processes
        tr_metrics = runSimulationParallel(loanPool, securities, NSIM, 3)

        yields = calcYields(tr_metrics[:, 0], tr_metrics[:, 1])
        new_rates = rates + step_sizes * (yields - rates)  # update rates
        diff = np.dot(percents, (rates - new_rates)/rates)
        ii += 1
        rates = new_rates
        
    print "Done"
    securities = makeSecurities(loanPool.totalPrincipal(), percents, rates, levels)
    loanPool.reset()
    securities.reset()
    tr_metrics, lp_waterfall, ss_waterfall, res_amounts = doWaterfall(loanPool, securities)
    table = [['DIRR', tr_metrics[0][1], tr_metrics[1][1]], ['Rating', tr_metrics[0][3], tr_metrics[1][3]],
              ['WAL', tr_metrics[0][2], tr_metrics[1][2]], ['Rate', rates[0], rates[1]]]
    headers = ['Tranche 1', 'Tranche 2']
    return tabulate(table, headers, tablefmt='rst')

