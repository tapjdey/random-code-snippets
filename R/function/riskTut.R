#Full data is at
# http://mockus.org/riskTut.zip and
# http://sailhome.cs.queensu.ca/~mei/Tutorial/Stats4SE
#Tutorial on building a logistic Model for predicting risk of software changes.
#Version 3.2.1b
#Presented by Audris Mockus, Mei Nagappan, Ahmed E. Hassan
#Email: audris@avaya.com and mei@cs.queensu.ca and ahmed@cs.queensu.ca 
#Except where otherwise noted, content on this site is licensed under a Creative Commons Attribution 3.0 License.
# http://creativecommons.org/licenses/by/3.0/
#License: 

#WARNING: This script is meant to help beginners. So please run the script line by line and not as a whole!
#Avoid too many significant digits
options(digits=2);

#set R's working directory to where the data was extracted
#eg. on windows
#setwd("C:/downloads/risk");
#e.g., on linux
#setwd("/tmp/risk/");

#see
risk <- read.table("risk1.paper",header=T);
#obtain a manageable subset for illustration
#In SE its a no-brainer: log-transform ALL the numeric variables
vars <- cbind (risk$isBad, log(risk$NS),log(risk$NM),log(risk$NF),log(risk$NLOGIN),
           log(risk$NMR),log(risk$ND),log(risk$LA+1),log(risk$LD+1),
           log(risk$LinesUnchanged+1),log(risk$to-risk$from+1),risk$logEXP,risk$logREXP,
           risk$logSEXP,risk$FIX);
dimnames(vars)[[2]] <- c("isBad","lNS", "lNM", "lNF", "lNLgn",  "lNMR", "lND",
                         "lLA", "lLD", "lLOC", "lINT", "lEXP", "lREXP", "lSEXP","FIX"); 

#R likes data.frame: a matrix with (potentially) different types in each column
data <- data.frame(vars);
#Variable names as in the paper: http://mockus.org/papers/bltj13.pdf
#Audris Mockus and David M. Weiss. Predicting risk of software changes. Bell Labs Technical Journal,
# 5(2):169-180, April-June 2000.   

#Reasons:
# 1) may
## | Type       | Name   | Description                             |
## | Response   | isBad  | Did MR cause patch to fail?             |
## |            | NS     | Number of subsystems touched.           |
## | Diffusion  | NM     | Number of modules touched.              |
## |            | NF     | Number of files touched.                |
## |            | NLOGIN | Number of developers involved.          |
## |            | LA     | LOC added.                              |
## | Size       | LD     | LOC deleted.                            |
## |            | LT     | LOC in the files touched by the change. |
## | Diffusion  | NMR    | Number of MRs.                          |
## | and size   | ND     | Number of deltas.                       |
## | Interval   | INT    | Time between the last and first delta.  |
## | Purpose    | FIX    | Fix of a defect found in the field.     |
## |            | EXP    | Developer experience.                   |
## | Experience | REXP   | Recent developer experience.            |
## |            | SEXP   | Developer experience on a subsystem.    | 

#now explore variables
#interpret  basic summaries
summary(data);

#interpret correlations
cor(vars);# OK for normal distrubution
cor(vars,method="spearman"); #OK for any: uses ranks

#just see top corelations
hiCor <- function(x, level){
  res <- cor(x,method="spearman");
  res1 <- res; res1[res<0] <- -res[res < 0];
  for (i in 1:dim(x)[2]){
    res1[i,i] <- 0;
  }
  sel <- apply(res1,1,max) > level;
  res[sel,sel];
}
hiCor(data,.7)
#So much correlation is typical in SE
#How to select an orthogonal subset

#look at principal components
plot(1:15,cumsum(prcomp(vars, retx=F,scale=T)$sdev^2)/sum(prcomp(vars, retx=F,scale=T)$sdev^2),ylim=c(0,1),xlab="Number of coponents",ylab="Fraction of variance");
res<-prcomp(vars, retx=F,scale=T)$rotation[,1:5];
resAbs <- res;
resAbs[res<0] <- -res[res<0];
for (i in 1:5)
  print(t(res[resAbs[,i]>.3,i,drop=FALSE]));
##       lNM  lNF lNLgn lNMR  lND  lLA lLD
## PC1 0.32 0.33  0.31 0.34 0.34 0.31 0.3
##      lEXP lREXP lSEXP
## PC2 -0.65 -0.66 -0.33
##     isBad FIX
## PC3  0.84 0.5
##       lNS lSEXP
## PC4 -0.46  0.54
##     isBad   FIX
## PC5   0.5 -0.84
#What does that mean?

#regress each predictor on the remaining predictors
# eliminate with the highest adjR^2
res <- c();
vnam <- names(data);
for (i in 2:dim(data)[2]){
  fmla <- as.formula(paste(vnam[i],paste(vnam[-c(1,i)],collapse="+"),sep="~"));
  res <- rbind(res,c(i,round(summary(lm(fmla,data=data))$r.squared,2)));
}
row.names(res) <- vnam[res[,1]];
res[order(-res[,2]),];
## lEXP        12 0.95
## lREXP       13 0.95
## lND          7 0.94
## lNF          4 0.91
## lNM          3 0.87
## lNMR         6 0.86
## lLA          8 0.81
## lNS          2 0.80
## lLD          9 0.76
## lNLgn        5 0.72
## lLOC        10 0.65
## lSEXP       14 0.52
## lINT   11 0.47
## FIX         15 0.08


#finally select the model
# Note, that exploring only the predictor space is not leading to
#  multiple comparisons issue!
#replace lSEXP by lEXP: simpler 
#why lLOC, lLA, lLD, lND, lNlgn: keep lND as most stable, keep lLOC?
#finally, we'll need to do prediction, drop last few years
data1 <- data;
data1$from <- risk$from/3600/24/365.25+1970;
dataFit <- data1[data1$from<=1997,]; #80%
dataTest <- data1[data1$from>1997,]; #20%

mod <- glm(isBad ~ lNS+lLA+FIX+lLOC+lINT+lEXP,family=binomial,data=dataFit);
summary(mod); #AIC: 2753
#good to order by variance explained (Anova Deviance/Df)
anova(mod, test="Chi");
##      Df Deviance Resid. Df Resid. Dev Pr(>Chi)    
## NULL                 13480       3012             
## lNS   1    166.1     13479       2845   <2e-16 ***
## lLA   1     65.1     13478       2780    7e-16 ***
## FIX   1     17.4     13477       2763    3e-05 ***
## lLOC  1     10.7     13476       2752   0.0011 ** 
## lINT  1      5.5     13475       2747   0.0193 *  
## lEXP  1      7.7     13474       2739   0.0054 ** 


mod <- glm(isBad ~ lNS+lND+FIX+lEXP+lINT,family=binomial,data=dataFit);
summary(mod);
#slightly higher AIC: 2762, but a simpler model
#don't chace the best fit, as it leads to overfitting
anova(mod, test="Chi");#it is good to order predictors by deviance explained
##      Df Deviance Resid. Df Resid. Dev Pr(>Chi)    
## NULL                 13480       3012             
## lNS   1    166.1     13479       2845  < 2e-16 ***
## lND   1     64.3     13478       2781  1.1e-15 ***
## FIX   1     17.7     13477       2763  2.6e-05 ***
## lEXP  1      9.3     13476       2754   0.0024 ** 
## lINT  1      3.8     13475       2750   0.0502 .  
#Note: use test="F" for linear models (lm)
#Note: R's anova order matters in variance explained, as
#  each SS is based on the residuals from predictors going before it
#Alternative sum of squares for ANOVA are obtained via drop1
# In this case it is based on the residuals of remaining predictors (not
# just of preceeding predictors
drop1(mod, test="Chi");
##        Df Deviance  AIC  LRT Pr(>Chi)    
## <none>        2750 2762                  
## lNS     1     2759 2769  8.6   0.0033 ** 
## lND     1     2795 2805 44.4  2.6e-11 ***
## FIX     1     2767 2777 16.8  4.1e-05 ***
## lEXP    1     2758 2768  7.5   0.0061 ** 
## lINT    1     2754 2764  3.8   0.0502 .  


#Variance inflation factor
# http://en.wikipedia.org/wiki/Variance_inflation_factor
vif(mod);
# lNS  lND  FIX lINT lEXP 
# 2.3  3.1  1.2  1.9  1.0 
#is less that 5 (max is 3.1 for lND), but lower would be better

#is model stable if some data is dropped?
#what if we change data as in GDF?
#is there a time trend isBad ~ lNS+lND+FIX+lEXP+lINT+from
#independece (residuals)

#interpret the model
# What do estimated coefficients mean?
#Increase NS from 1 to 2, but other predictors matter
# pick what is reasonable or a median
try <- dataFit[1:2,];
for (i in dim(dataFit)[2])
  try[,i] <- median(dataFit[,i]);
try[1,"lNS"] <- 0;
try[2,"lNS"] <- log(2);
res <- 1/(1+exp(-predict(mod,try)));
res[2]*(1-res[1])/res[1]/(1-res[2]);
#[1] 1.9

#do prediction
predicted <- 1/(1+exp(-predict(mod,dataTest)));
tapply(predicted, dataTest$isBad, mean)
    0     1 
0.022 0.059 
#good to know: predicted probability is almost three times higher for the 
# MRs that break patches

#traditional performance:
for (cutof in c(.01, .015, .02, .03, .04, .045,.1)){
  res <- table(predicted>cutof, dataTest$isBad);
  type1 <- res[2,1]/(res[1,1]+res[2,1]);
  type2 <- res[1,2]/(res[1,2]+res[2,2]);
  recall <- 1 - type2;
  precision <- res[2,2]/(res[2,1]+res[2,2]);
  print (c(cutof,type1,type2,recall,precision));
}
##  0.010 0.649 0.120 0.880 0.017
##  0.015 0.434 0.180 0.820 0.024
##  0.020 0.312 0.380 0.620 0.025
##  0.030 0.184 0.420 0.580 0.039
##  0.040 0.130 0.500 0.500 0.047
##  0.045 0.112 0.520 0.480 0.052
##  0.100 0.025 0.740 0.260 0.116

#single number as ROC typically maes little sense:
#in this case primary concern is decent recall

#compare to a random predictor

#compare to a simple predictor, e.g, more than one subsystem

#Other prediction methods
library(rpart);

fmla <- isBad ~ lNS+lND+FIX+lINT+lEXP+lLA;
er <- c();
for (w in c(20,40,60,80, 100, 110)){ 
  cart.fit <- rpart(fmla,data=dataFit,method="class",weights=as.numeric(dataFit$isBad)*w+1);
  cart.pred <- predict(cart.fit,newdata=dataTest,type="class");
  res <- table(cart.pred, dataTest$isBad);
  type1 <- res[2,1]/(res[1,1]+res[2,1]);
  type2 <- res[1,2]/(res[1,2]+res[2,2]);
  recall <- 1 - type2;
  precision <- res[2,2]/(res[2,1]+res[2,2]);
  er <- rbind (er, c(w,type1,type2,recall,precision));
}
er #slightly worse that the regression model
##      [,1]  [,2] [,3] [,4]  [,5]
## [1,]   20 0.087 0.54 0.46 0.064
## [2,]   40 0.363 0.34 0.66 0.023
## [3,]   60 0.481 0.26 0.74 0.019
## [4,]   80 0.553 0.20 0.80 0.018
## [5,]  100 0.645 0.14 0.86 0.017
## [6,]  110 0.645 0.14 0.86 0.017


