
import numpy as np
from scipy.stats import weibull_min
import cma
from scipy.stats import ks_2samp
from scipy.optimize import minimize,curve_fit
import math 
from scipy.stats import weibull_min
from scipy.stats import kstest
from scipy.optimize import minimize


def threeweibullcdf(tvalue, alpha, beta, eta):
    assert all(val >= 0 for val in [alpha, beta, eta])
    if(tvalue>alpha):
        return np.exp(-((tvalue - alpha) / eta) ** beta)
    else:
        return 0
    



def threeweibullpdf(tvalue, alpha, beta, eta):
    assert all(val >= 0 for val in [alpha, beta, eta])
    if(tvalue>alpha):
        return (beta / eta) * ((tvalue - alpha) / eta)** (beta - 1) * np.exp(-((tvalue - alpha) / eta))
    else:
        return 0
     
    



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


def calculate_mse(e_alpha,e_beta,e_eta,alpha,beta,eta):
    assert all(val >= 0 for val in [e_alpha,e_beta,e_eta,alpha, beta, eta])


    m_weibull= mean_of_threeweibull(alpha, beta, eta)
    estimated_m_weibull= mean_of_threeweibull(e_alpha, e_beta, e_eta)
    variance= variance_of_threeweibull(e_alpha, e_beta, e_eta)
    mse = variance +(estimated_m_weibull - m_weibull)**2
    return mse



def calculate_aic(nll, num_params):
    aic = 2 * num_params - 2 * nll
    return aic



def pdf_threeweibull(tvalue, alpha, beta, eta):
    pdf_values = np.where(tvalue > alpha, ((beta/eta)*((tvalue-alpha)/eta)**(beta-1)*np.exp(-((tvalue - alpha) / eta))), 0)
    return pdf_values



def log_likelihood(params, data):
    #assert np.all(params >= 0)
    alpha, beta, eta = params
    result_sum = 0
    n = len(data)
    
    for i in range(1, n + 1):
        term = 0  # Initialize term to zero
        
        if data[i - 1] > alpha:
            term = np.log(beta) + (beta - 1) * np.log(data[i - 1] - alpha) - beta * np.log(eta) - ((data[i - 1] - alpha) / eta) ** beta
        
        result_sum += term
  
    return result_sum


def neg_log_likelihood(params, data):
    alpha, beta, eta = params
    nll = -log_likelihood(params, data) # Ignore non-finite values
    return nll


def cma_es_func(data,alpha,beta,eta):
# Sample data for demonstration
 initial_guess = [alpha,beta,eta]
 options = {'maxfevals': 1000}
 std=math.sqrt(variance_of_threeweibull(alpha, beta, eta))
 try:
    res = cma.fmin(neg_log_likelihood, initial_guess, std, options=options, args=(data,))
    print("Optimized Parameters:", res[0])
    print(type(res[0]))

     # Calculate AIC
    optimized_nll = neg_log_likelihood(res[0], data)
    num_params = len(initial_guess)
    aic = calculate_aic(optimized_nll, num_params)
   #  print("AIC:", aic)

     # Calculate K-S statistic and p-value
    optimized_cdf = np.cumsum(pdf_threeweibull(np.sort(data), *res[0])) / np.sum(pdf_threeweibull(np.sort(data), *res[0]))
    ks_statistic, p_value = ks_2samp(np.linspace(0, 1, len(data)), optimized_cdf)
    
    # print("K-S Statistic:", ks_statistic)
    # print("P-Value:", p_value)
    
    #liste=[res[0][0],res[0][1],res[0][2],aic,ks_statistic,p_value]
    #print( liste)
    optimized_parameters = res[0]
    liste=[optimized_parameters[0],optimized_parameters[1],optimized_parameters[2],aic,ks_statistic,p_value]
    return liste
 except Exception as e:
    print("Error during optimization:", e)




def  mle_es_func(data,alpha,beta,eta):
 initial_guess = [alpha,beta,eta]
 try:
    res = minimize(neg_log_likelihood, initial_guess, args=(data,), method='L-BFGS-B')
    optimized_params = res.x
   # print(res)

    # Calculate AIC
    optimized_nll = neg_log_likelihood(optimized_params, data)
    num_params = len(initial_guess)
    aic = calculate_aic( optimized_nll , num_params)
   # print("AIC:", aic)

    # Calculate K-S test statistic and p-value
    sorted_data = np.sort(data)
    cdf_data = np.linspace(0, 1, len(data))
    cdf_model = np.cumsum(pdf_threeweibull(sorted_data, *optimized_params)) / np.sum(pdf_threeweibull(sorted_data, *optimized_params))
    ks_statistic, p_value = ks_2samp(cdf_data, cdf_model)

    # Print K-S test result
    #print("K-S Statistic:", ks_statistic)
   # print("P-Value:", p_value)
   # print("Optimized Parameters (MLE):", optimized_params)
  #  print("Optimized Parameters (MLE):", optimized_params[0])
    liste=[optimized_params[0],optimized_params[1],optimized_params[2],aic,ks_statistic,p_value]
    return liste
 except Exception as e:
    print("Error during optimization:", e)



def  least_reg_func(data,alpha,beta,eta):
 try:
  initial_guess = [alpha,beta,eta]
  # Perform least squares regression
  optimized_params, covariance = curve_fit(pdf_threeweibull, data, np.zeros_like(data), p0=initial_guess)

  # Print optimized parameters 
  # print("Optimized Parameters (Least Squares):", optimized_params)
  # Calculate AIC
  residuals = data - pdf_threeweibull(data, *optimized_params)
  #print("optimized parameters", optimized_params[0], optimized_params[1], optimized_params[2])
  ssr = np.sum(residuals**2)
  num_params = len(initial_guess)
  n = len(data)
  aic = n * np.log(ssr/n) + 2 * num_params
  #print("AIC (Least Squares):", aic)
  # Calculate K-S test statistic and p-value
  sorted_data = np.sort(data)
  cdf_data = np.linspace(0, 1, len(data))
  cdf_model = np.cumsum(pdf_threeweibull(sorted_data, *optimized_params)) / np.sum(pdf_threeweibull(sorted_data, *optimized_params))
  ks_statistic, p_value = ks_2samp(cdf_data, cdf_model)

# Print K-S test result
 #print("K-S Statistic:", ks_statistic)
 #print("P-Value:", p_value)
  liste=[optimized_params[0],optimized_params[1],optimized_params[2],aic,ks_statistic,p_value]
  return liste
 except Exception as e:
    print("Error during optimization:", e)




# KS Testi
def ks_test(data, alpha, beta, eta):
    weibull_cdf = weibull_min.cdf(data, beta, scale=eta, loc=alpha)
    ks_statistic, p_value = kstest(data, weibull_cdf)
    return ks_statistic, p_value

# AIC Hesaplama
def calculate_aicc(params, data, weights):
    alpha, beta, ln_eta = params
    eta = np.exp(ln_eta)
    predicted = (beta / eta) * ((data - alpha) / eta)**(beta - 1) * np.exp(-((data - alpha) / eta)**beta)
    log_likelihood = np.sum(weights * np.log(predicted))
    num_params = len(params)
    aic = 2 * num_params - 2 * log_likelihood
    return aic




# Doğal Logaritma Alın
def natural_log_transform(data):
    return np.log(data)

# Ağırlıklı En Küçük Kareler Optimizasyonu
def weighted_least_squares(params, w, x, y):
    alpha, beta, ln_eta = params
    eta = np.exp(ln_eta)
    predicted = (beta / eta) * ((x - alpha) / eta)**(beta - 1) * np.exp(-((x - alpha) / eta)**beta)
    residuals = y - predicted
    weighted_residuals = w * residuals
    return np.sum(weighted_residuals**2)

def bergman(tvalues, alpha, beta, eta):
    weibull_cdf = weibull_min.cdf(tvalues, beta, scale=eta, loc=alpha)
    weights = ((1 - weibull_cdf) * np.log(1 - weibull_cdf))**2
    return weights



def ft(tvalues, alpha, beta, eta):
    weibull_cdf = weibull_min.cdf(tvalues, beta, scale=eta, loc=alpha)
    weights = 3.3 *weibull_cdf-27.5*(1-(1-weibull_cdf)**(0.025))
    return weights





def wls(data,alpha,beta,eta):
 
 variance=variance_of_threeweibull(alpha,beta,eta)
 mu=mean_of_threeweibull(alpha,beta,eta)
 sigma=math.sqrt(variance)
 high=mu+3*sigma
 tvalue = np.linspace(alpha,high, len(data))

 try:
    log_tvalue = natural_log_transform(tvalue)
    log_dataset = natural_log_transform(data)

    initial_guess = [alpha,beta,eta]

    weights = np.ones_like(log_dataset)

    result = minimize(weighted_least_squares, initial_guess, args=(weights, log_tvalue, log_dataset), method='L-BFGS-B')

    alpha_estimate, beta_estimate, ln_eta_estimate = result.x
    eta_estimate = np.exp(ln_eta_estimate)
 

    ks_statistic, p_value_ks = ks_test(data, alpha_estimate, beta_estimate, eta_estimate)

    aic_value = calculate_aicc(result.x, log_dataset, weights)

    liste=[alpha_estimate,beta_estimate,eta_estimate, aic_value,ks_statistic,p_value_ks]
    return liste
 except Exception as e:
    print("Error during optimization:", e)





def wls_bergman(data,alpha,beta,eta):
 
 variance=variance_of_threeweibull(alpha,beta,eta)
 mu=mean_of_threeweibull(alpha,beta,eta)
 sigma=math.sqrt(variance)
 high=mu+3*sigma
 tvalue = np.linspace(alpha,high, len(data))

 try:

    log_tvalue = natural_log_transform(tvalue)
    log_dataset = natural_log_transform(data)


    initial_guess = [alpha,beta,eta]


    weights =bergman(data, alpha, beta, eta)


    result = minimize(weighted_least_squares, initial_guess, args=(weights, log_tvalue, log_dataset), method='L-BFGS-B')


    alpha_estimate, beta_estimate, ln_eta_estimate = result.x
    eta_estimate = np.exp(ln_eta_estimate)
 

    ks_statistic, p_value_ks = ks_test(data, alpha_estimate, beta_estimate, eta_estimate)

    aic_value = calculate_aicc(result.x, log_dataset, weights)

    liste=[alpha_estimate,beta_estimate,eta_estimate, aic_value,ks_statistic,p_value_ks]
    return liste
 except Exception as e:
    print("Error during optimization:", e)




def wls_ft(data,alpha,beta,eta):
 
 variance=variance_of_threeweibull(alpha,beta,eta)
 mu=mean_of_threeweibull(alpha,beta,eta)
 sigma=math.sqrt(variance)
 high=mu+3*sigma
 tvalue = np.linspace(alpha,high, len(data))

 try:
# Doğal Logaritma Alın
    log_tvalue = natural_log_transform(tvalue)
    log_dataset = natural_log_transform(data)

# Başlangıç tahmin değerleri
    initial_guess = [alpha,beta,eta]

# Ağırlık faktörleri
    weights =ft(data, alpha, beta, eta)

# Optimizasyon
    result = minimize(weighted_least_squares, initial_guess, args=(weights, log_tvalue, log_dataset), method='L-BFGS-B')

  # Optimize Edilmiş Parametreleri Alın
    alpha_estimate, beta_estimate, ln_eta_estimate = result.x
    eta_estimate = np.exp(ln_eta_estimate)

  # KS Testi
    ks_statistic, p_value_ks = ks_test(data, alpha_estimate, beta_estimate, eta_estimate)

    # AIC Hesaplama
    aic_value = calculate_aicc(result.x, log_dataset, weights)

    liste=[alpha_estimate,beta_estimate,eta_estimate, aic_value,ks_statistic,p_value_ks]
    return liste
 except Exception as e:
    print("Error during optimization:", e)

