
import numpy as np
from scipy.stats import weibull_min

def threeweibullcdf(tvalue, alpha, beta, eta):
    assert all(val >= 0 for val in [alpha, beta, eta])
    
    cdf_values = np.where(tvalue > alpha, 1 - np.exp(-((tvalue - alpha) / eta) ** beta), 0)
    return cdf_values


def threeweibullpdf(tvalue, alpha, beta, eta):
    assert all(val >= 0 for val in [alpha, beta, eta])
    
    pdf_values = np.where(tvalue > alpha, (beta / eta) * ((tvalue - alpha) / eta) ** (beta - 1) * np.exp(-((tvalue - alpha) / eta)), 0)
    return pdf_values



def mean_of_threeweibull(alpha, beta, eta):
    assert all(val >= 0 for val in [alpha, beta, eta])
    
    result = eta * (np.math.gamma(1 + (1 / beta))) + alpha
    return result

def variance_of_threeweibull(alpha, beta, eta):
    assert all(val >= 0 for val in [alpha, beta, eta])
    
    result = (eta ** 2) * (np.math.gamma(1 + (2 / beta)) - (np.math.gamma(1 + (1 / beta))) ** 2)
    return result

def inverse_of_threeweibull(p, alpha, beta, eta):
    assert all(val >= 0 for val in [alpha, beta, eta])
    
    quantile_value = alpha + eta * (-np.log(1 - p)) ** (1 / beta)
    return quantile_value


def datagenerator(n, alpha, beta, eta):
    assert all(val >= 0 for val in [alpha, beta, eta]) and n > 0
    
    generated_data = np.random.uniform(0, 1, n)
    dataset = [inverse_of_threeweibull(i, alpha, beta, eta) for i in generated_data]
    return dataset


