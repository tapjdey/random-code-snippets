# A -> B, A -> C; Dl_A, Dl_B, Dl_C are in target matrix t

t = c(22, 10, 10) # target matrix
z = matrix(c(1,  1,  1,  1,
             NA, 1,  NA, 1,
             NA, NA, 1, 1), byrow = T, nrow = 3) # coeff matrix
z
while (abs(sum(abs(t - rowSums(z, na.rm = T))))> 1e-12) {
  z2= z + (t - rowSums(z, na.rm = T))/rowSums(!is.na(z))
  z = t(apply(z2, 1, function(x) {x+colSums(z2, na.rm = T) / colSums(!is.na(z2), na.rm = T)-x}))
}

z
#em -scaling
l = 0.5
z = matrix(c(1,  1,  1,  l,
             NA, 1,  NA, l,
             NA, NA, 1,  l), byrow = T, nrow = 3) # coeff matrix
z
k = 1e6
i = 0
while (abs(abs(sum(abs(t - rowSums(z, na.rm = T)))) - k) > 1e-15) {
  i = i+1
  k = abs(sum(abs(t - rowSums(z, na.rm = T))))
  z2= z*(t/rowSums(z, na.rm = T) )
  z = t(apply(z2, 1, function(x) {x+colSums(z2, na.rm = T) / colSums(!is.na(z2), na.rm = T)-x}))
}

z

################################
# parametric simulation
################################
v1 = v2 = numeric(0)
rn = seq(1e-18,20,0.1)
for (l in rn) {
  z = matrix(c(1,  1,  1,  l,
               NA, 1,  NA, l,
               NA, NA, 1,  l), byrow = T, nrow = 3) # coeff matrix
  k = 1e6
  i = 0
  
  while (abs(abs(sum(abs(t - rowSums(z, na.rm = T)))) - k) > 1e-15) {
    i = i+1
    k = abs(sum(abs(t - rowSums(z, na.rm = T))))
    z2= z*(t/rowSums(z, na.rm = T) )
    z = t(apply(z2, 1, function(x) {x+colSums(z2, na.rm = T) / colSums(!is.na(z2), na.rm = T)-x}))
  }
  v1 = c(v1, z[1,4])
  z = matrix(c(1,  1,  1,  l,
               NA, 1,  NA, l,
               NA, NA, 1,  l), byrow = T, nrow = 3) # coeff matrix
  while (abs(sum(abs(t - rowSums(z, na.rm = T))))> 1e-12) {
    z2= z + (t - rowSums(z, na.rm = T))/rowSums(!is.na(z))
    z = t(apply(z2, 1, function(x) {x+colSums(z2, na.rm = T) / colSums(!is.na(z2), na.rm = T)-x}))
  }
  v2 = c(v2, z[1,4])
}
plot(rn, v1)
plot(rn, v2)

