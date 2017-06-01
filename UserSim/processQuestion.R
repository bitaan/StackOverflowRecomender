library(jsonlite)
library(readr)
library(cluster)
library(Matrix)
library(arules)


raw <- fromJSON("C:\\Users\\ei08047\\Desktop\\StackOverflowRecomender\\stack_api\\questions.json")

dataFrameToTransaction <- function(raw){
  
  raw <- na.omit(raw)
  ### Data Cleaning
  raw$creation_date <- NULL
  raw$creation_date <- NULL
  raw$last_edit_date <- NULL
  raw$answer_count <- NULL
  raw$title <- NULL
  raw$link <- NULL
  raw$view_count <-discretize( raw$reputation, method = "cluster")
  raw$owner$reputation <-discretize( raw$reputation, method = "cluster")
  raw$owner$user_id <-discretize( raw$owner$user_id, method = "cluster")
  raw$owner$accept_rate <-discretize( raw$owner$accept_rate, method = "cluster")

  

 while(FALSE)
 {
   for(line in raw$tags)
   {
     for(tag in line)
     {
       split <- strsplit(line[tag], " ")
       name <- paste ("tag",tag , sep = "", collapse = NULL)
       raw[name] <- c(split[tag])
     }
   }
   colnames(raw)
 }

  
  

  trans = as(raw$tags,"transactions")
  return (trans)
}



