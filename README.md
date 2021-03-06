Table of Contents
=================

 -  [Overview](#overview)
 -  [Requirements](#requirements)
 -  [Documentation](#documentation)
 -  [Acknowledgements](#acknowledgements)
 -  [License](#license)


Overview
========

This project is archived on [zenodo](https://zenodo.org/record/11557):

<a href="http://dx.doi.org/10.5281/zenodo.11557"><img src="https://zenodo.org/badge/doi/10.5281/zenodo.11557.png" alt="10.5281/zenodo.11557"></a>

This repository serves as an [open-science
notebook](http://en.wikipedia.org/wiki/Open_notebook_science) for research
conducted by [Jamie Oaks](http://www.phyletica.com), Charles Linkem, Jeet
Sukumaran, and others into Bayesian methods of phylogeographcial model choice.
We use simulated and biological data to assess the behavior of existing and
newly developed methods for estimating the probability of models of shared
divergence times across a set of co-distributed populations.

Requirements
============

Replicating our work will require a unix shell and Python. Specifically, we
conducted the work using bash and Python version 2.7.

Also, most of the heavy lifting was performed using the Python package
[`PyMsBayes`](http://www.github.com/joaks1/PyMsBayes), which should work in
Linux and Mac OsX.
An archive of the [`PyMsBayes`](http://www.github.com/joaks1/PyMsBayes) code
repository that will reproduce all our results is included in top-level
directory `software-archive`.

If you want to go so far as to generate the plots used in the manuscripts and
slides, you will also need the Python plotting library
[`matplotlib`](http://matplotlib.org/).
If you want to compile PDFs of manuscripts and slides, you will also need
[LaTeX](http://www.latex-project.org/).

Documentation
=============

All of the analyses we performed for this [open-science
notebook](http://en.wikipedia.org/wiki/Open_notebook_science) are sparsely
documented.
This lack of ``in-text'' documentation is purposeful;
the fine-grained commit history (and associated comments) of the git repository
is a much more detailed, accurate, and useful guide to the step-by-step
progress of this project.
Thus, the history of this repository is meant to be the primary guide for
reproducing our work.

Acknowledgements
================

This project was made possible by funding provided to [Jamie
Oaks](http://www.phyletica.com) from the National Science Foundation (DEB
1011423 and DBI 1308885), University of Kansas (KU) Office of Graduate Studies,
Society of Systematic Biologists, Sigma Xi Scientific Research Society, KU
Ecology and Evolutionary Biology Department, and the KU Biodiversity Institute.

License
=======

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/deed.en_US"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/deed.en_US">Creative Commons Attribution 4.0 International License</a>.

