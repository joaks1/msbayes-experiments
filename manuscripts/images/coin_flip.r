rm(list=ls(all=TRUE))

prior_heads = 10
prior_tails = 10
heads = 3
tails = 7

post_heads = prior_heads + heads
post_tails = prior_tails + tails
epost_heads = prior_heads + (2 * heads)
epost_tails = prior_tails + (2 * tails)

q = seq(0, 1, 0.005)
prior = dbeta(q, prior_heads, prior_tails)
post = dbeta(q, post_heads, post_tails)
epost = dbeta(q, epost_heads, epost_tails)
ymax = max(epost) + (0.02 * max(epost))

post_prob_unfair_heads = pbeta(0.5, post_heads, post_tails,
                               lower.tail = F)
epost_prob_unfair_heads = pbeta(0.5, epost_heads, epost_tails,
                                lower.tail = F)
post_mode = (post_heads - 1) / (post_heads + post_tails - 2)
epost_mode = (epost_heads - 1) / (epost_heads + epost_tails - 2)
cat(paste('post prob unfair heads: ', post_prob_unfair_heads, '\n'))
cat(paste('emp post prob unfair heads: ', epost_prob_unfair_heads, '\n'))
cat(paste('post mode: ', post_mode, '\n'))
cat(paste('emp post mode: ', epost_mode, '\n'))

pdf('coin_flip.pdf', width=7.087, height=4.5)
par(yaxs="i", xaxs="i", cex.lab=1.2, cex.axis=1.0, mgp=c(2.2, 0.7, 0),
    oma=c(0, 0, 0.2, 0.5), mar=c(3.2, 3.2, 0.5, 0.1))
plot(x=c(), y = c(), xlab=bquote(theta), ylab='Density', xlim=c(0,1),
     ylim=c(0, ymax))
lines(q, prior)
lines(q, post, col='blue')
lines(q, epost, col='red')
dev.off()

