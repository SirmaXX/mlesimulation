threeweibullcdf <- function(tvalue, alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0))
  
  cdf_values <- ifelse(tvalue > alpha, 1 - exp(-((tvalue - alpha) / eta)^beta), 0)
  return(cdf_values)
}

# cdf deneme
result <- threeweibullcdf(1, 0.5,2, 1.5)
print(result)
 
threeweibullpdf <- function(tvalue, alpha,beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0))
  pdf_values <- ifelse(tvalue > alpha, ((beta/eta)*((tvalue-alpha)/eta)^(beta-1)*exp(-((tvalue - alpha) / eta))), 0)
  return(pdf_values)
}


# pdf deneme
result <- threeweibullpdf(1, 0.5, 2,1.5)
print(result)

mean_of_threeweibull <- function(alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0))
  result <- eta * (gamma(1 + (1 / beta))) + alpha
  return(result)
}

# Test the function
print(mean_of_threeweibull(1, 1, 1))


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

lnlikehoodthreeweibull_l1<-function(tarray,alpha,beta, eta,n){
  stopifnot(alpha >= 0, beta >= 0, eta >= 0,n>0)
  result=0
  for (i in n) {
    result =result + (ln(beta)+ (beta-1)*ln(tarray[i]- alpha) -(beta*ln(eta)) -  ((tarray[i]-alpha)/eta)^(beta))
  }
}

# Define the range of x values
x <- seq(0.05, 5, 0.001)

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

library(weibullness)

inverse_of_threeweibull <- function(p, alpha, beta, eta) {
  stopifnot(all(alpha >= 0), all(beta >= 0), all(eta >= 0))
  quantile_value <- alpha + eta * (-log(1 - p))^(1/beta)
  return(quantile_value)
}

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

# Three-parameter Weibull
datas <- datagenerator(1000, 1, 1, 1)  # Increase the sample size
print(mean(datas))
print(var(datas))
print(mse(datas))
# Fit Weibull distribution using MLE with error handling
weibull_params <- tryCatch(
  {
    weibull.mle(datas)
  },
  error = function(e) {
    message("Error during MLE estimation:", e)
    NULL
  }
)

# Display the estimated parameters
print(weibull_params)
