library(jsonlite)
library(readr)
library(cluster)
library(Matrix)
library(arules)
library(e1071)

raw_users <- fromJSON("C:\\Users\\ei08047\\Desktop\\StackOverflowRecomender\\stack_api\\users.json")
raw_users_top_questions_by_tag <- fromJSON("C:\\Users\\ei08047\\Desktop\\StackOverflowRecomender\\stack_api\\top-answer-tags.json")

## discretization & cleaning method
processUsers <- function(raw){
  raw <- na.omit(raw)
  ### Data Cleaning
  raw$website_url <- NULL
  raw$age <- NULL
  raw$last_modified_date <- NULL
  ##raw$account_id <- NULL
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
  raw
}

proc_users <- processUsers(raw_users)



processUserTopTags<- function(users,topTags){
  l1 <- list()
  l2 <- list()
  x <- 1
  c <- 1
  while(x < 500 )
  {
    xf <-x + 4
    a <- topTags[x:xf,]
    
    tag1 <-  a$tag_name[1]
    answer_score1 <- a$answer_score[1]
    
    
    l1[[c]] <- tag1
    l2[[c]] <- answer_score1
    
    
    x <- x + 5
    c <- c +1
    ##print(a$user_id)
    ##print(a$answer_count)
    ##print(a$tag_name)
  }
  
  s <- data.frame(l1,l2, row.names = c('tag1','answer_score1'))
}

proc_top_q <- processUserTopTags(proc_users,raw_users_top_questions_by_tag)



dataFrameToTransaction <- function(raw){
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

# function to find medoid in cluster i
clust.centroid = function(i, dat, clusters) {
  ind = (clusters == i)
  colMeans(dat[ind,])
}

sapply(unique(groups), clust.centroid, raw$reputation , groups)

result <- cmeans(raw, centers=2, iter.max=100, m=2, method="cmeans")  # 3 clusters
plot(raw$account_id, raw$reputation_change_week, col=result$cluster)
points(result$centers[,c(raw$account_id,raw$reputation_change_week)], col=1:3, pch=19, cex=2)




trans<-cbind(trans,groups)

x1<- subset(trans, groups==1)
x2<- subset(trans, groups==2)
x3<- subset(trans, groups==3)
x4<- subset(trans, groups==4)

plot(cluster, hang=-1, label=cluster$order)








##



#####################################################################

server <- function(){
  while(TRUE){
    writeLines("Listening...")
    con <- socketConnection(host="localhost", port = 6022, blocking=TRUE,
                            server=TRUE, open="r+")
    data <- readLines(con, 1,warn = TRUE,skipNul=TRUE)
    print(data)
    ##process response
    ##switch
      ##case its a id
        ##check if already have this id in raw 
        ##predict medoid
        ## return
    response <- toupper(data)
    writeLines(response, con) 
    close(con)
  }
}
server()

######################################################################





