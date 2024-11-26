library(eyelinker)
library(ggplot2)
eyedata <- read_asc('example/wf_20241126.asc') 
# TODO: merge by event
p <- ggplot(eyedata$raw) +
   aes(x=xpl,y= eyedata$info$screen.y - ypl) +
   geom_point() +
   labs(title="wf example traces", y="left eye y", x="left eye x") +
   see::theme_modern()

ggsave("example/wf_20241126.png", p)
