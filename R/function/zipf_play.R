# Trying to simulate a preferential attachment process
set.seed(50)

n = 10000 # no. of elements
itr = 50000 # no. of iyerations

library(animation)

d = rep(1,n) # initial distribution
for (i in 1:itr){
  pd = d/sum(d) + 0.5*runif(n)
  ind = order(-pd)[1]
  d[ind] = d[ind] + 1
  
}

#plot(hist(d))
plot(sort(d, decreasing = T), log="xy")