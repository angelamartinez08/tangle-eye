#!/usr/bin/env Rscript

# plot eyelink traces colored by event
# 

library(eyelinker)
library(ggplot2)
library(dplyr)
library(tidyr)
eyedata <- read_asc('example/wf_20241126.asc') 

msg <- eyedata$msg %>%
   separate(text, c('trial','what', 'xpos','ypos'), sep=" ") %>%
   mutate(across(c(xpos,ypos), as.numeric))

traces <- eyedata$raw %>%
   merge(msg,all=T,by='time') %>%
   fill(c(trial,what,xpos,ypos), .direction="down") %>%
   mutate(y=eyedata$info$screen.y - ypl)

event_pos <- msg %>%
   transmute(what,
             xpl=(xpos+1)/2*eyedata$info$screen.x,
             y=(ypos+1)/2*eyedata$info$screen.y) %>%
  unique

p <- ggplot(traces) +
   aes(x=xpl, y=y,
       color=what) +
   geom_point(alpha=.3) +
   # show where expected gaze is
   #geom_point(data=event_pos, color='black',aes(color=NULL)) +
   labs(title="wf example traces",
        y="left eye y",
        x="left eye x") +
   see::theme_modern()

ggsave("example/wf_20241126.png", p)
