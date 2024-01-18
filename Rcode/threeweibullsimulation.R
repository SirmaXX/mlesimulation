
#3 parametreli weibull dağılım fonksiyonu
threeweibullcdf <- function(tvalue, alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0))
  
  cdf_values <- ifelse(tvalue > alpha, 1 - exp(-((tvalue - alpha) / eta)^beta), 0)
  return(cdf_values)
}

# cdf deneme
result <- threeweibullcdf(1, 0.5,2, 1.5)
print(result)
 
#3 parametreli weibull olasılık yoğunluk fonksiyonu
threeweibullpdf <- function(tvalue, alpha,beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0))
  pdf_values <- ifelse(tvalue > alpha, ((beta/eta)*((tvalue-alpha)/eta)^(beta-1)*exp(-((tvalue - alpha) / eta))), 0)
  return(pdf_values)
}

# pdf deneme
result <- threeweibullpdf(1, 0.5, 2,1.5)
print(result)

#weibulun ortalama fonksiyonu
mean_of_threeweibull <- function(alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0))
  result <- eta * (gamma(1 + (1 / beta))) + alpha
  return(result)
}

# ortalamanın testi
print(mean_of_threeweibull(1, 1, 1))

#weibulun varyans fonksiyonu
variance_of_threeweibull<- function(alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0))
  result <- (eta^2) * (gamma(1 + (2 / beta)) - (gamma(1 + (1 / beta)))^2) 
  return(result)
  
}
print(variance_of_threeweibull(1, 1, 1))

Likeehoodthreeweibull<-function(tarray,alpha,beta, eta,n){
  stopifnot(alpha >= 0, beta >= 0, eta >= 0,n>0)
  result=1
  for (i in n) {
    result=result *( (beta/eta)*((tarray[i]-alpha)/eta)^(beta-1)*exp(-((tarray[i] - alpha) / eta)) )
  }
  
}

lnlikehoodthreeweibull<-function(tarray,alpha,beta, eta,n){
  stopifnot(alpha >= 0, beta >= 0, eta >= 0,n>0)
  result=0
  for (i in n) {
    result =result + (ln(beta)+ (beta-1)*ln(tarray[i]- alpha) -(beta*ln(eta)) -  ((tarray[i]-alpha)/eta)^(beta))
  }
}

lnlikehoodthreeweibull_l1 <- function(params, tarray) {
  alpha <- params[1]
  beta <- params[2]
  eta <- 1
  n <- length(tarray)
  stopifnot(alpha >= 0, beta >= 0, eta >= 0, n > 0)
  
  result <- 0
  for (i in 1:n) {
    result <- result + (log(beta) + (beta - 1) * log(tarray[i] - alpha) - (beta * log(eta)) - ((tarray[i] - alpha) / eta) ^ (beta))
  }
  
  return(result)
}
################################# Grafik çizimi ###########################
# Define the range of x values
x <- seq(0.05, 1, 0.001)

# Calculate the PDF values for different values of beta
pdf_beta0 <- threeweibullpdf(x, 0, 0.5, 1.5)
pdf_beta1 <- threeweibullpdf(x, 0, 1, 1.5)
pdf_beta2 <- threeweibullpdf(x, 0, 2, 1.5)
pdf_beta3 <- threeweibullpdf(x, 0, 3, 1.5)
pdf_beta4 <- threeweibullpdf(x, 0, 4, 1.5)
pdf_beta9 <- threeweibullpdf(x, 0, 9, 1.5)




library(ggplot2)

# Create a data frame with PDF values for different values of beta
df <- data.frame(
  x = rep(x, 6),
  pdf = c(pdf_beta0, pdf_beta1, pdf_beta2, pdf_beta3,pdf_beta4,pdf_beta9),
  beta = rep(c("beta=0", "beta=1", "beta=2", "beta=3", "beta=4", "beta=9"), each = length(x))
)

# Plot with ggplot2
ggplot(df, aes(x, pdf, color = beta, linetype = beta)) +
  geom_line(size = 0.5) +
  labs(title = "Three-Parameter Weibull PDFs with Various Values of Beta", x = "x", y = "PDF") +
  theme_minimal() +
  scale_color_manual(values = c("blue", "red", "green", "pink","lightblue","purple")) +
  scale_linetype_manual(values = c(1, 1, 1, 1,1,1,1)) +
  theme(legend.position = "topright")
################################# Grafik çizimi ###########################


library(weibullness)

#F(X)'in tersi (veri üretmek için tersini aldım)
inverse_of_threeweibull <- function(p, alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0))
  quantile_value <- alpha + eta * (-log(1 - p))^(1/beta)
  return(quantile_value)
}
# veri üretim fonksiyonu(uniformdan veri ürettik çünkü 0-1 arası bütün sayılar eşit olasılıkta çekiliyor)
datagenerator <- function(n, alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0), n > 0)
  generateddata <- runif(n = n, min = 0, max = 1)
  dataset <- c()
  for (i in generateddata) {
    xvalue <- inverse_of_threeweibull(i, alpha, beta, eta)
    dataset <- append(dataset, xvalue)
  }
  return(dataset)
}

# Tveri üretimi
datas <- datagenerator(1000, 1, 1, 1)  # Increase the sample size
initial_guess <- c(1, 1, 1)
print(mean(datas))
print(var(datas))


#################################### MLE METHOD ################################################


#################################### MLE METHOD ################################################


#F(X)'in tersi (veri üretmek için tersini aldım)
# Inverse of threeweibull function
inverse_of_threeweibull <- function(p, alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0))
  quantile_value <- alpha + eta * (-log(1 - p))^(1/beta)
  return(quantile_value)
}

# Data generation function
datagenerator <- function(n, alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0), n > 0)
  generated_data <- runif(n, min = 0, max = 1)
  dataset <- sapply(generated_data, function(i) inverse_of_threeweibull(i, alpha, beta, eta))
  return(dataset)
}

# Log-likelihood function
log_likelihood <- function(params, data) {
  alpha <- params[1]
  beta <- params[2]
  eta <- params[3]
  
  result_sum <- 0
  n <- length(data)
  
  for (i in 1:n) {
    term <- 0  # Initialize term to zero
    
    if (data[i] > alpha) {
      term <- log(beta) + (beta - 1) * log(data[i] - alpha) - beta * log(eta) - ((data[i] - alpha) / eta)^beta
    }
    
    result_sum <- result_sum + term
  }
  
  return(result_sum)
}

# Negative log-likelihood function
neg_log_likelihood <- function(params, data) {
  nll <- -log_likelihood(params, data)
  
  if (!is.finite(nll)) {
    # If non-finite value encountered, return a large positive value
    return(1e10)
  }
  
  return(nll)
}

# Data generation and optimization
datas <- datagenerator(1000, 1, 1, 1)  # Increase the sample size
initial_guess <- c(1, 1, 1)

# Minimize the negative log-likelihood using L-BFGS-B method
res <- optim(par = initial_guess, fn = neg_log_likelihood, data = datas, method = "L-BFGS-B")
optimized_params <- res$par



#################################### least square regression  METHOD ################################################

dataset<-datas

# Fit a linear model using lm
model <- lm(datas ~ 1 + I(datas^2))

# Print the summary of the model
summary(model)

# Extract the estimated coefficients
estimated_alpha_ls <- coef(model)[1]
estimated_beta_ls <- coef(model)[2]
estimated_eta_ls <- coef(model)[3]
# Calculate MSE for least squares regression
mse_alpha_ls <- calculate_mse(estimated_alpha_ls, estimated_beta_ls, 0, 1, 1, 1)

# Print results
print(paste("True Alpha:", 1))
print(paste("Estimated Alpha (LS):", estimated_alpha_ls))
print(paste("MSE for Alpha (LS):", mse_alpha_ls))




#################################### least square regression METHOD ################################################



#################################### weighted least squares regressionMETHOD ################################################

wt <- 1 / lm(abs(model$residuals) ~ model$fitted.values)$fitted.values^2

#perform weighted least squares regression
wls_model <- lm(datas ~ 1 + I(datas^2), weights=wt)

#view summary of model
summary(wls_model)

# Extract the estimated coefficients
estimated_alpha_ls1 <- coef(wls_model)[1]
estimated_beta_ls1 <- coef(wls_model)[2]
estimated_eta_ls1 <- coef(wls_model)[3]
# Calculate MSE for least squares regression
mse_alpha_ls1 <- calculate_mse(estimated_alpha_ls1, estimated_beta_ls1, 0, 1, 1, 1)

# Print results
print(paste("True Alpha:", 1))
print(paste("Estimated Alpha (LS):", estimated_alpha_ls1))
print(paste("MSE for Alpha (LS):", mse_alpha_ls1))


#################################### weighted least squares regression METHOD ################################################



#################################### CMA-ES METHOD ################################################
library(weibullness)
library(rCMA)
library(rJava)

# Set seed and generate some example data
set.seed(123)
true_alpha <- 1
true_beta <- 1

isFeasible <- function(x) {  (sum(x) - length(x)) >= 0;  }

# Create CMA-ES object
cma <- cmaNew(propFile="CMAEvolutionStrategy.properties");

cmaInit(cma,seed=42,dimension=2,initialX = c(1.0, 1.0), initialStandardDeviations=0.2);

neg_log_likelihood <- function(params, data) {
  alpha <- params[1]
  beta <- params[2]
  eta <- params[3]
  
  # Check parameter constraints
  if (any(params <= 0)) {
    return(Inf)  # Return infinity for infeasible parameters
  }
  
  # Calculate negative log-likelihood
  nll <- -sum(dweibull(datas, shape = beta, scale = alpha, log = TRUE))
  return(nll)
}

# Run CMA-ES optimization
res <-  cmaOptimDP(cma, neg_log_likelihood  ,iterPrint=100);

# Print the optimized parameters
print(paste("Optimized Parameters: ", res$bestX))

optimized_alpha <- res[1]
optimized_beta <- res[2]
optimized_eta <- res[3]

# Print the optimized parameters
print(paste("Optimized Alpha: ", optimized_beta$bestX[1]))
print(paste("Optimized Beta: ", optimized_beta$bestX[2]))
print(paste("Optimized Eta: ", optimized_eta))











############################## n tabanlı ################################
variance_of_threeweibull<- function(alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0))
  result <- (eta^2) * (gamma(1 + (2 / beta)) - (gamma(1 + (1 / beta)))^2) 
  return(result)
  
}


#weibulun ortalama fonksiyonu
mean_of_threeweibull <- function(alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0))
  result <- eta * (gamma(1 + (1 / beta))) + alpha
  return(result)
}


#F(X)'in tersi (veri üretmek için tersini aldım)
inverse_of_threeweibull <- function(p, alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0))
  quantile_value <- alpha + eta * (-log(1 - p))^(1/beta)
  return(quantile_value)
}
# veri üretim fonksiyonu(uniformdan veri ürettik çünkü 0-1 arası bütün sayılar eşit olasılıkta çekiliyor)
datagenerator <- function(n, alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0), n > 0)
  generateddata <- runif(n = n, min = 0, max = 1)
  dataset <- c()
  for (i in generateddata) {
    xvalue <- inverse_of_threeweibull(i, alpha, beta, eta)
    dataset <- append(dataset, xvalue)
  }
  return(dataset)
}
calculate_mse <- function(e_alpha, e_beta, e_eta,alpha, beta, eta) {
  
  m_weibull<- mean_of_threeweibull(alpha, beta, eta)
  estimated_m_weibull<-mean_of_threeweibull(e_alpha, e_beta, e_eta)
  variance<-variance_of_threeweibull(e_alpha, e_beta, e_eta)
  mse <- variance + (estimated_m_weibull - m_weibull)^2
  return(mse)
}

# Tveri üretimi
datas <- datagenerator(1009, 1, 1, 1)  # Increase the sample size
gercekortalama =mean_of_threeweibull (1,1,1)
gercekvaryans=variance_of_threeweibull(1,1,1)
cat("gercek ortalama:", gercekortalama, "\n")
cat("gercek varyans:", gercekvaryans, "\n")
print(mean(datas))
print(var(datas))


############################## n tabanlı ################################

