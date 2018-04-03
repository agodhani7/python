import numpy as np

ABSRatingRates = [-np.inf, 0.06, 0.67, 1.3, 2.7, 5.2, 8.9, 13, 19, 27, 46, 72, 106, 143, 183, 231, 311, 2500]

ABSRatingLetters = ["Aaa", "Aa1", "Aa2", "Aa3", "A1", "A2", "A3",
                    "Baa1", "Baa2", "Baa3", "Ba1", "Ba2", "Ba3", "B1", "B2", "B3", "Caa", "Ca"]


def ABSRating(dirr):
    idx = ABSRatingRates.index(max([i for i in ABSRatingRates if i <= dirr/100.0]))
    return ABSRatingLetters[idx]
