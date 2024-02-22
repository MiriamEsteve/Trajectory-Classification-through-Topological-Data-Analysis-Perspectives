#### https://cran.r-project.org/web/packages/trajectories/vignettes/article.pdf ####

library(trajectories)
library(ggplot2)
library("TDA")
set.seed(10)

library("spacetime")
library("sp")
 
ar <- c(0.001) #, 0.1, 0.5,0.99
sd0 <- c(1) #0.1, 0.5,  
m <- matrix(c(0,100,0,100),nrow=2,byrow = T)

for (ar_i in ar){
  for (sd0_i in sd0){
    # z is a simulated track in a same box as w but with a random number of points
    for(i in 1:100){
      N <- 100
      z <- rTrack(n = N, bbox = m, start = as.POSIXct("2023-01-01"), ar = ar_i,
             step = 60, sd0 = sd0_i, transform = T, nrandom = T)
      data <- as.data.frame(cbind(z@sp@coords))
      colnames(data) <- c("x", "y")
      
      
      ## Plot trajectories
      plot(data[,c("x","y")],lwd=2,main="Simulated trajectories", type="l")
      
      #Write CSV
      write.csv(as.data.frame(data), paste("C:/Users/Miriam_Esteve/OneDrive - Fundación Universitaria San Pablo CEU/Documents/CEU/Investigación/2023/UTHECA/paper/scripts/data/len", as.character(N),"/data", as.character(i), "_ar", as.character(ar_i), "-sd0", as.character(sd0_i), ".csv",sep = ""),  row.names = FALSE)
    }
  }
}
 
library(plotly) 

ar_i <- 0.001
sd0_i <- 1
N <- 100
fig <- list()
for(i in 1:8){
  data <- read.csv( paste("C:/Users/Miriam_Esteve/OneDrive - Fundación Universitaria San Pablo CEU/Documents/CEU/Investigación/2023/UTHECA/paper/scripts/data/len", as.character(N),"/data", as.character(i), "_ar", as.character(ar_i), "-sd0", as.character(sd0_i), ".csv",sep = ""))
  fig[[i]] <- plot_ly(x=data[,c("x")], y=data[,c("y")], type="scatter", mode = 'lines', name=paste("data", as.character(i-1), sep=""))
}
fig <- subplot(fig, nrows = 2)
fig <- fig %>%layout( title = 'Simulated trajectories. ar = 0.001 and sd0 = 1') 
fig

# 
# ############## TDA ###############3
# X <- as.data.frame(data)
# Xlim <- c(min(X$x)+1, max(X$x)+1); Ylim <- c(min(X$y)+1, max(X$y)+1); by <- 0.065
# Xseq <- seq(Xlim[1], Xlim[2], by = by)
# Yseq <- seq(Ylim[1], Ylim[2], by = by)
# Grid <- expand.grid(Xseq, Yseq)
# 
# 
# # Rips filtration
# maxscale <- 5
# maxdimension <- 1
# DiagTri <- ripsDiag(X, maxdimension, maxscale,
#                     printProgress = TRUE)
# 
# #points with lifetime = 0 are not shown. e.g. the loop of the triangle.
# P1 <- DiagTri[["diagram"]]
# #Plot
# plot(P1)
# ## Barcode
# plot(P1, barcode = TRUE, main = "Persistence barcode")
# 
# 
# library(reticulate)
# ## Install environment
# python_env <- function(){
#   # check if r-reticulate exists in users environments
#   if (!("r-reticulate" %in% reticulate::conda_list()$name)) {
#     reticulate::install_miniconda()
#   }
#   reticulate::use_miniconda("r-reticulate")
#   
#   # instead of reticulate::use_python,
#   # set the RETICULATE_PYTHON path manually
#   py_path <- reticulate::conda_python()
#   Sys.setenv(RETICULATE_PYTHON = py_path)
#   
#   # check if packages need to be installed
#   installed_py_packages <- reticulate::py_list_packages("r-reticulate")$package
#   req_py_packages <- c("numpy", "pandas", "scikit-learn", "pandas", "matplotlib", "ripser", "persim", "gudhi")
#   
#   for (py_package in req_py_packages) {
#     if (!(py_package %in% installed_py_packages)) {
#       reticulate::conda_install("r-reticulate", py_package)
#     }
#   }
# }
# 
# 
# ## call python code
# persistence_diagram <- function(data, num = "1"){
#   # Load Python environment
#   python_env()
#   source_python(paste(getwd(), '/R/Python/pers_diagram.py', sep=""))
#   imgs <- persim_diagram(data, num)
#   return(imgs)
# }
# 
# 
# ## Wasserstein distance
# Wasserstein_distance <- function(X, X2){
#   # Load Python environment
#   # python_env()
#   source_python(paste(getwd(), '/R/Python/Wasserstein_distance.py', sep=""))
#   diagrams <- wasserstein(X, X2)
#   P1 <<- diagrams[[1]]
#   P2 <<- diagrams[[2]]
#   
# }
# 
# # Barycenter
# barycenter <- function(P1, P2){
#   # Load Python environment
#   python_env()
#   source_python(paste(getwd(), '/R/Python/barycenter.py', sep=""))
#   barycenter(P1$diagram, P2$diagram)
# }
# 
# # Classification
# classfication <- function(imgs1, imgs2){
#   # Load Python environment
#   python_env()
#   source_python(paste(getwd(), '/R/Python/classification.py', sep=""))
#   accuracy <- classification_persim(imgs1, imgs2)
#   
#   return(accuracy)
# }
# 
# imgs <- persistence_diagram(data, num = "1")
# 
# #DTM
# m0 <- 0.001
# data1.dtm <- matrix(dtm(X1, Grid, m0), nrow = length(Xseq), ncol = length(Yseq)) #calculate DTM
# image(data1.dtm) #Plot image of DTM
# 
