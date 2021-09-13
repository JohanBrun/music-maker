import numpy as np
from numpy.random import default_rng

rng = default_rng()


def gen_normal(mu: float, sigma: float, length: int):
    noise = rng.normal(mu, sigma, length)
    noise = noise * 60
    noise = np.rint(noise)
    return noise
