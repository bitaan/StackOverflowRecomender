library(jsonlite)
library(readr)
library(cluster)
library(arules)


raw <- fromJSON("C:\\Users\\ei08047\\Desktop\\StackOverflowRecomender\\stack_api\\users.json")

## discretization & cleaning method
dataFrameToTransaction <- function(raw){
  raw <- na.omit(raw)
  ### Data Cleaning
  raw$website_url <- NULL
  raw$age <- NULL
  raw$last_modified_date <- NULL
  raw$account_id <- NULL
  raw$is_employee <- NULL
  raw$profile_image <- NULL
  raw$link <- NULL
  raw$creation_date <- NULL
  raw$location <- NULL
  raw$display_name <- NULL
  raw$last_access_date <- NULL
  
  raw$user_id <- NULL##factor(raw$user_id)
  raw$user_type <- NULL##factor(raw$user_type)

  raw$badge_counts <- NULL
  ##raw$badge_counts$bronze <- discretize( as.numeric(raw$badge_counts$bronze), method="cluster")  
  ##raw$badge_counts$silver <- discretize(as.numeric( raw$badge_counts$silver), method="cluster")  
  ##raw$badge_counts$gold <- discretize(as.numeric(raw$badge_counts$gold), method="cluster") 

  raw$reputation_change_year <- discretize( raw$reputation_change_year, method = "cluster")
  raw$reputation_change_quarter <- discretize( raw$reputation_change_quarter, method = "cluster")
  raw$reputation_change_day <- discretize( raw$reputation_change_day, method = "cluster")
  raw$reputation_change_week <- discretize( raw$reputation_change_week, method = "cluster")
  raw$reputation_change_month <- discretize( raw$reputation_change_month, method = "cluster")
  
  
  raw$accept_rate <- discretize( raw$accept_rate, method = "cluster")##factor(as.numeric(raw$accept_rate))
  raw$reputation <- discretize( raw$reputation, method = "cluster") ##factor(as.numeric(raw$reputation))

  trans = as(raw, "transactions")
  return (trans)
}

trans <- dataFrameToTransaction(raw)

getSample <- function(transactions,numSamples){
  set.seed(1234)
  s<- sample(transactions,numSamples)
  s
}

calcDiss <- function(transactions){

  sample <- getSample(transactions,58)
  diss <- dissimilarity(sample,method="cosine")
  saveRDS(diss,"diss.rds")
  diss
}

diss <- calcDiss(trans)

cluster <- hclust(diss,method = "complete" , members = NULL)

groups<-cutree(cluster, k=4)

trans<-cbind(trans,groups)
x1<- subset(trans, groups==1)
x2<- subset(trans, groups==2)
x3<- subset(trans, groups==3)
x4<- subset(trans, groups==4)



