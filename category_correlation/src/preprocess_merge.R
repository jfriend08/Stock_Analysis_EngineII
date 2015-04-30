

#get to working dir
setwd('/Volumes/HHD/Users/yun-shaosung/HDD_Doc/NYU/RealTimeBigData/project/Data2/')

#Read in the company list
Symbols<-read.table('./downloadable_List.txt',colClasses='character',comment.char='#', header=F)

#Fetching the infor and combine them together
tickers <- as.array(Symbols$V1)
getSymbols(tickers[3803:length(tickers)], warnings=FALSE,from="2015-01-01", to="2015-04-08")
ClosePrices <- do.call(merge, lapply(tickers[3803:length(tickers)], function(x) Cl(get(x))))
head(ClosePrices)
rownames(ClosePrices)<-ClosePrices[,0]




################### Different method ###################
filenames <- list.files(path="./historicalData2", pattern="*_price.txt", full.names=TRUE)
companyList <- read.csv('./companylist02.csv', sep=",", header=T)

rownames(companyList)<-gsub(" ", "", companyList$Symbol)
  


array<-0
namelist<-list()
Days<-360
for (i in 1:length(filenames)){
  print(i)
  tmp = read.table(filenames[i], row.names = 1 ,sep="\t", header=TRUE)  
  if (nrow(tmp) < Days){
    next
  }
  else{
    end=nrow(tmp)
    start=nrow(tmp)-Days
    name<-gsub("_price.txt", "", basename(filenames[i]))
    namelist <- append(namelist, name)
    array<- cbind(array,tmp[start:end,"Volume"])  
  }  
}
array <- subset(array, select = -c(array))
colnames(array) <- as.array(unlist(namelist))
rownames(array) <- rownames(tmp)[start:end]

tarray<-t(array)

#write.table(array, file="ClosePrice_180daysII.txt",sep="\t", row.names = TRUE, col.names = TRUE)

test <- cbind(companyList[rownames(tarray),c("MarketCap", "industry")], tarray)
write.table(test, file="Volume_360days.txt",sep="\t", row.names = TRUE, col.names = TRUE)
