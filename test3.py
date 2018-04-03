'''
our final step
BE PATIENT

Anuj Godhani
'''

from loan.pool import poolCSV
from montecarlo import runMonte
import logging

# input your file path
def main():
    lp = poolCSV('/Users/anujgodhani/Downloads/Level-7-Case-Study/Loans.csv')
    logging.basicConfig(level=logging.ERROR)

    # Testing runMonte with 200 simulations and 0.005 tolerance level
    print runMonte(lp, 200, 0.005)

if __name__ == '__main__':
    main()
