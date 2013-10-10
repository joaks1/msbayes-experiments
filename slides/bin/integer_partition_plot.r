#!/usr/bin/env Rscript

##############################################################################
## Functions

integer_partition = function(n) {
    part_nums = c()
    for (k in 1:n) {
        part_nums = c(part_nums, A(n=n, k=k))
    }
    return(part_nums)
}

A = function(n, k) {
    if ((k == 1) || (n == k)) {
        return(1)
    }
    if ((k > n) || (k < 1)) {
        return(0)
    }
    return(A(n=(n-1), k=(k-1)) + A(n=(n-k), k=k))
}

expand_integer_vector = function(v) {
    expanded = c()
    for (i in 1:length(v)) {
        expanded = c(expanded, rep(i, v[i]))
    }
    return(expanded)
}

get_psi_prior = function(n) {
    integer_parts = integer_partition(n=n)
    return(1/(n * integer_parts))
}

parse_file_ext = function(path) {
    return(tail(strsplit(path, '\\.')[[1]], n=1))
}

plot_div_model_prior = function(n, output_path="partition_numbers.pdf") {
    prior_probs = get_psi_prior(n=n)
    names(prior_probs) = c(1:n)
    partition_numbers = expand_integer_vector(integer_partition(n=n))
    plot_letters = LETTERS[1:2]
    format = 'pdf'
    ext = parse_file_ext(output_path)
    if ((tolower(ext) == 'eps') || (tolower(ext) == 'ps')) {
        format = 'eps'
    }

    if (format == 'eps') {
        postscript(output_path, onefile = F, paper="special", horizontal=F, width=7.087, height=3)
    } else {
        pdf(output_path, width=7.087, height=3)
    }
    par(yaxs = "i", xaxs = "i")
    par(cex.axis=0.7)
    par(mgp = c(1.4,0.4,0)) # mgp adjusts space of axis labels
    # oma is space around all plots
    par(oma = c(0,0,0.3,0.2), mar = c(2.65,2.45,0.5,0.1))
    par(mfrow = c(1, 2))
    hist(partition_numbers,
            breaks= c(1:(n+1)),
    		right=FALSE,
    		xlab="",
    		ylab=bquote("# of divergence models"),
            main="",
    		# xlim=c(0,22),
    		# ylim=c(0,140),
    		xaxt="n",
    		col="gray50", border="gray50")
    box()
    axis(1, at=seq(1.5, (n+.5), 1), labels=c(1:n), tick=F)
    axis(1, at=c(1:(n+1)), labels=F)
    #mtext("Number of divergence models", WEST<-2, padj=0, cex=1, outer = T)
    mtext(plot_letters[[1]], side=3, adj=0, line=0, cex=0.75, font=2)
    
    par(mgp = c(1,0.4,0)) # mgp adjusts space of axis labels
    barplot(prior_probs, 
            border="gray50",
            space=0,
            # axis.lty=1,
    	    xaxt = "n",
            col="gray50",
    		xlab="",
            ylab=bquote(italic(p)(italic(M)[group("|", bold(tau), "|")*","*italic(i)])),
            ylim=c(0, max(prior_probs))
            )
    box()
    axis(1, at=seq(0.5, (n-.5), 1), labels=c(1:n), tick=F)
    axis(1, at=c(0:n), labels=F)
    mtext(plot_letters[[2]], side=3, adj=0, line=0, cex=0.75, font=2)
	mtext(bquote("# of divergence events, " * group("|", bold(tau), "|")), SOUTH<-1, padj=-0.7, cex=1.1, outer = T)
    dev.off()
}

##############################################################################
## Main CLI

## Option parsing
suppressPackageStartupMessages(library("optparse"))
option_list <- list(
        make_option(c("-n", "--num-elements"), type="integer", dest="n", default=22,
                help="Number of elements (default: 22)"),
        make_option(c("-o", "--output-path"), type="character",
                dest="output_path", default="partition_numbers.pdf",
                help=paste("Output path for plot file (default: ",
                           "'./partition_numbers.pdf'). If you want an EPS-",
                           "formatted plot file, simply specify a path with ",
                           "an '.eps' or '.ps' extension. Otherwise, the ",
                           "plot file will be a PDF."))
)
options <- parse_args(OptionParser(option_list=option_list))

plot_div_model_prior(n = options$n,
                     output_path = options$output_path)

