#! /bin/bash

paths="../../validation/images/validation-accuracy-omega-glm.pdf
../../validation/images/validation-accuracy-omega.pdf
../../validation/images/validation-accuracy-psi-glm.pdf
../../validation/images/validation-accuracy-psi.pdf
../../validation/images/validation-accuracy-time-glm.pdf
../../validation/images/validation-accuracy-time.pdf
../../validation/no-sort/results/pymsbayes-results/plots/prior-dpp_prior-dpp_accuracy.pdf
../../power-comparison/images/exp-power-omega-accuracy-6.pdf
../../power-comparison/images/old-power-omega-accuracy-6.pdf
../../power-comparison/images/uniform-power-omega-accuracy-6.pdf"


for f in $paths
do
    n=${f/\.pdf/-compress\.pdf}
    convert -density 300 -compress jpeg -quality 60 $f $n
done

