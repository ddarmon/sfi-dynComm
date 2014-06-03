par(mfrow = c(1, 1))

mu = -5; var = 0.85

X = rnorm(8000, mean = mu, sd = sqrt(var))

Y = exp(X)

plot(density(Y, from = 0), xlim = c(0, 0.1), ylim = c(0, 200), lwd = 3, col = 'red')
hist(Y, add = T, probability = TRUE)

mu.hat = sum(log(Y))/length(Y)
var.hat = sum((log(Y) - mu.hat)^2)/length(Y)

x = seq(0.0005, 0.1, by = 0.0005)

lines(x, dlnorm(x, meanlog = mu.hat, sdlog = sqrt(var.hat)), lwd = 3, col = 'blue')