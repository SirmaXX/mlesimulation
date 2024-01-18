library(rCMA)
library(rJava)
# Negative log-likelihood function
neg_log_likelihood <- function(params, data) {
  alpha <- params[1]
  beta <- params[2]
  eta <- params[3]
  
  # Check parameter constraints
  if (any(params <= 0)) {
    return(Inf)  # Return infinity for infeasible parameters
  }
  data <- datagenerator(1000, 1, 1, 1)
  # Calculate negative log-likelihood
  pdf_values <- pdf_threeweibull(data, alpha, beta, eta)
  
  nll <- -sum(log(pdf_values[is.finite(pdf_values)]))  # Ignore non-finite values
  return(nll)
}

# Probability density function
pdf_threeweibull <- function(tvalue, alpha, beta, eta) {
  pdf_values <- ifelse(tvalue > alpha, ((beta/eta)*((tvalue-alpha)/eta)^(beta-1)*exp(-((tvalue - alpha) / eta))), 0)
  return(pdf_values)
}

# Inverse of the three-parameter Weibull distribution
inverse_of_threeweibull <- function(p, alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0))
  quantile_value <- alpha + eta * (-log(1 - p))^(1/beta)
  return(quantile_value)
}

# Data generator
datagenerator <- function(n, alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0), n > 0)
  generated_data <- runif(n, min = 0, max = 1)
  dataset <- sapply(generated_data, function(i) inverse_of_threeweibull(i, alpha, beta, eta))
  return(dataset)
}

# Sample data for demonstration

# CMA-ES optimization
initial_guess <- c(1.0, 1.0, 1.0)
cma <- cmaNew();
cmaInit(cma,seed=42,dimension=3,initialX= c(1.0, 1.0,1.0));
res1 = cmaOptimDP(cma,neg_log_likelihood,iterPrint=30);
plot(res1$fitnessVec,type="l",log="y",col="blue"
     ,xlab="Iteration",ylab="Fitness");
str(res1);

# Print the optimized parameters
cat("Optimized Parameters:", res1$bestX, "\n")