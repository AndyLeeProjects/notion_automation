<<<<<<< HEAD


library(tidyverse)

all_dat <- read.table("C:/Users/anddy/OneDrive/Desktop/data.csv", sep = ',', stringsAsFactors = TRUE, header=TRUE)

model <- lm(Total ~ X.Phone.pickups + X.Screen.time + Drink...over.3.beer. + Meditation..min.,
            Total.To.do.List, Personal.Reading,
            data = all_dat)
=======


library(tidyverse)

all_dat <- read.table("C:/Users/anddy/OneDrive/Desktop/data.csv", sep = ',', stringsAsFactors = TRUE, header=TRUE)

model <- lm(Total ~ X.Phone.pickups + X.Screen.time + Drink...over.3.beer. + Meditation..min.,
            Total.To.do.List, Personal.Reading,
            data = all_dat)
>>>>>>> 572dc86 (update)
