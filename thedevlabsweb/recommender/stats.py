import random
from math import sqrt
from collections import defaultdict
from scipy.stats import pearsonr

# Get real.

def wilson_ci_lower_bound(n, pos):
    """Returns the lower bound of the 95% confidence interval for a
    Bernoulli parameter p ~ pos/n
    """
    if n == 0:
        return 0
    z = 1.96 # 95%
    phat = pos/float(n)
    return (phat + z*z/(2*n) - z*sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)

def to_vector(u1, all_pks):
    """Vectorizes the queryset of scores. all_pks must be sorted"""
    d = defaultdict(int)
    for score in u1:
        d[score.website.pk] = score.value
    return [d[pk] for pk in all_pks]


def pearson_correlation(u1, u2, all_websites):
    """Computes the Pearson product-moment correlation coefficient
    """
    return pearsonr(u1, u2)
