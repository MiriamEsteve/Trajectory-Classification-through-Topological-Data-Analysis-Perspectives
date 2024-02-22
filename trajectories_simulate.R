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
      write.csv(as.data.frame(data), paste("./paper/scripts/data/len", as.character(N),"/data", as.character(i), "_ar", as.character(ar_i), "-sd0", as.character(sd0_i), ".csv",sep = ""),  row.names = FALSE)
    }
  }
}

## Plot trajectories
library(plotly) 

ar_i <- 0.001
sd0_i <- 1
N <- 100
fig <- list()
for(i in 1:8){
  data <- read.csv( paste("./paper/scripts/data/len", as.character(N),"/data", as.character(i), "_ar", as.character(ar_i), "-sd0", as.character(sd0_i), ".csv",sep = ""))
  fig[[i]] <- plot_ly(x=data[,c("x")], y=data[,c("y")], type="scatter", mode = 'lines', name=paste("data", as.character(i-1), sep=""))
}
fig <- subplot(fig, nrows = 2)
fig <- fig %>%layout( title = 'Simulated trajectories. ar = 0.001 and sd0 = 1') 
fig
