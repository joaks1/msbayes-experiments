rm(list=ls(all=TRUE))

plot_pca = function(pca_obj, predict_obj, xlim, ylim,
                    xlab = 'PC1', ylab = 'PC2') {
    plot(pca_obj$scores[,1], pca_obj$scores[,2],
         xlab = xlab,
         ylab = ylab,
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
m3_path = '../priors-for-pc-plot/pymsbayes-results/pymsbayes-output/prior-stats-summaries/m4-prior-sample.txt'
m4_path = '../priors-for-pc-plot/pymsbayes-results/pymsbayes-output/prior-stats-summaries/m5-prior-sample.txt'
m5_path = '../priors-for-pc-plot/pymsbayes-results/pymsbayes-output/prior-stats-summaries/m6-prior-sample.txt'
plot_path = '../priors-for-pc-plot/pc-plots.pdf'

stat_indices = c(94:181)

observed <- read.table(observed_path, skip=1)
m1 = read.table(m1_path, skip=1)[stat_indices]
colnames(m1) = colnames(observed)
m1a = read.table(m1a_path, skip=1)[stat_indices]
colnames(m1a) = colnames(observed)
m1b = read.table(m1b_path, skip=1)[stat_indices]
colnames(m1b) = colnames(observed)
m3 = read.table(m3_path, skip=1)[stat_indices]
colnames(m3) = colnames(observed)
m4 = read.table(m4_path, skip=1)[stat_indices]
colnames(m4) = colnames(observed)
m5 = read.table(m5_path, skip=1)[stat_indices]
colnames(m5) = colnames(observed)

m1_pca <- princomp(m1)
m1a_pca <- princomp(m1a)
m1b_pca <- princomp(m1b)
m3_pca <- princomp(m3)
m4_pca <- princomp(m4)
m5_pca <- princomp(m5)

observed_m1 = predict(m1_pca, observed)
observed_m1a = predict(m1a_pca, observed)
observed_m1b = predict(m1b_pca, observed)
observed_m3 = predict(m3_pca, observed)
observed_m4 = predict(m4_pca, observed)
observed_m5 = predict(m5_pca, observed)
plot_letters = LETTERS[1:6]

pdf(plot_path, width=7.087, height=4.0)
    par(yaxs = "i", xaxs = "i")
    par(cex.axis=0.7)
    par(mgp = c(1.5,0.6,0)) # mgp adjusts space of axis labels
    # oma is space around all plots
    par(oma = c(0,0,0.7,0.4), mar = c(2.6,2.9,0.5,0.1))
    par(mfrow = c(2, 3))

    xlim = c(-0.4, 0.4)
    ylim = c(-0.2, 0.2)
    plot_pca(m1_pca, observed_m1, xlim, ylim, xlab = '')
    mtext(plot_letters[[1]], side=3, adj=0, line=0, cex=0.75, font=2)
	mtext(bquote(italic(M)[1]), side=3, adj=0.5, line=0, cex=0.75)

    plot_pca(m1a_pca, observed_m1a, xlim, ylim, xlab = '', ylab = '')
    mtext(plot_letters[[2]], side=3, adj=0, line=0, cex=0.75, font=2)
	mtext(bquote(italic(M)['1A']), side=3, adj=0.5, line=0, cex=0.75)

    plot_pca(m1b_pca, observed_m1b, xlim, ylim, xlab = '', ylab = '')
    mtext(plot_letters[[3]], side=3, adj=0, line=0, cex=0.75, font=2)
	mtext(bquote(italic(M)['1B']), side=3, adj=0.5, line=0, cex=0.75)

    xlim = c(-1.0, 1.5)
    ylim = c(-0.8, 0.8)
    plot_pca(m3_pca, observed_m3, xlim, ylim)
    mtext(plot_letters[[4]], side=3, adj=0, line=0, cex=0.75, font=2)
	mtext(bquote(italic(M)[3]), side=3, adj=0.5, line=0, cex=0.75)

    plot_pca(m4_pca, observed_m4, xlim, ylim, ylab = '')
    mtext(plot_letters[[5]], side=3, adj=0, line=0, cex=0.75, font=2)
	mtext(bquote(italic(M)[4]), side=3, adj=0.5, line=0, cex=0.75)

    xlim = c(-1.0, 2.0)
    ylim = c(-1.2, 1.2)
    plot_pca(m5_pca, observed_m5, xlim, ylim, ylab = '')
    mtext(plot_letters[[6]], side=3, adj=0, line=0, cex=0.75, font=2)
	mtext(bquote(italic(M)[5]), side=3, adj=0.5, line=0, cex=0.75)
dev.off()

