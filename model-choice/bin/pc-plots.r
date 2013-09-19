rm(list=ls(all=TRUE))

plot_pca = function(pca_obj, predict_obj, xlim, ylim) {
    plot(pca_obj$scores[,1], pca_obj$scores[,2],
         xlab = 'PC1',
         ylab = 'PC2',
         xlim = xlim,
         ylim = ylim)
    points(predict_obj[1], predict_obj[2],
           col='blue',
           lwd=3,
           pch=8)
}

observed_path = '../../response-redux/results/sampling-error/pymsbayes-results/observed-summary-stats/observed-1.txt'
m1_path = '../priors-for-pc-plot/pymsbayes-results/pymsbayes-output/prior-stats-summaries/m3-prior-sample.txt'
m1a_path = '../priors-for-pc-plot/pymsbayes-results/pymsbayes-output/prior-stats-summaries/m2-prior-sample.txt'
m1b_path = '../priors-for-pc-plot/pymsbayes-results/pymsbayes-output/prior-stats-summaries/m1-prior-sample.txt'
plot_path = '../priors-for-pc-plot/pc-plots.pdf'

stat_indices = c(94:181)

observed <- read.table(observed_path, skip=1)
m1 = read.table(m1_path, skip=1)[stat_indices]
colnames(m1) = colnames(observed)
m1a = read.table(m1a_path, skip=1)[stat_indices]
colnames(m1a) = colnames(observed)
m1b = read.table(m1b_path, skip=1)[stat_indices]
colnames(m1b) = colnames(observed)

m1_pca <- princomp(m1)
m1a_pca <- princomp(m1a)
m1b_pca <- princomp(m1b)

observed_m1 = predict(m1_pca, observed)
observed_m1a = predict(m1a_pca, observed)
observed_m1b = predict(m1b_pca, observed)
plot_letters = LETTERS[1:3]

pdf(plot_path, width=7.087, height=2.4)
    par(yaxs = "i", xaxs = "i")
    par(cex.axis=0.7)
    par(mgp = c(1.5,0.6,0)) # mgp adjusts space of axis labels
    # oma is space around all plots
    par(oma = c(0,0,0.7,0.4), mar = c(2.6,2.9,0.5,0.1))
    par(mfrow = c(1, 3))

    xlim = c(-0.4, 0.4)
    ylim = c(-0.2, 0.2)
    plot_pca(m1_pca, observed_m1, xlim, ylim)
    mtext(plot_letters[[1]], side=3, adj=0, line=0, cex=0.75, font=2)
	mtext(bquote(italic(M)[1]), side=3, adj=0.5, line=0, cex=0.75)

    plot_pca(m1a_pca, observed_m1a, xlim, ylim)
    mtext(plot_letters[[2]], side=3, adj=0, line=0, cex=0.75, font=2)
	mtext(bquote(italic(M)['1A']), side=3, adj=0.5, line=0, cex=0.75)

    plot_pca(m1b_pca, observed_m1b, xlim, ylim)
    mtext(plot_letters[[3]], side=3, adj=0, line=0, cex=0.75, font=2)
	mtext(bquote(italic(M)['1B']), side=3, adj=0.5, line=0, cex=0.75)
dev.off()

