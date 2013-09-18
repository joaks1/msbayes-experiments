rm(list=ls(all=TRUE))

q = seq(0, 1, 0.005)
prior = dbeta(q, 0.5, 0.5)
post = dbeta(q, 4.5, 1.5)
epost = dbeta(q, 8.5, 2.5)

pdf('coin_flip.pdf', width=7.087, height=4.5)
par(yaxs="i", xaxs="i", cex.lab=1.2, cex.axis=1.0, mgp=c(2.2, 0.7, 0),
    oma=c(0, 0, 0.2, 0.5), mar=c(3.2, 3.2, 0.5, 0.1))
plot(x=c(), y = c(), xlab=bquote(theta), ylab='Density', xlim=c(0,1),
     ylim=c(0, 3.5))
lines(q, prior)
lines(q, post, col='blue')
lines(q, epost, col='red')
dev.off()

