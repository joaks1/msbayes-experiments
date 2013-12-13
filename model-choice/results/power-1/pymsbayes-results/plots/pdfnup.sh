#! /bin/sh

pdfnup --nup '1x2' --suffix '1x2' -- power-psi-mode-4.pdf power-omega-prob-4-panel.pdf
pdfcrop power-omega-prob-4-panel-1x2.pdf power-4.pdf
rm power-omega-prob-4-panel-1x2.pdf

pdfnup --nup '1x2' --suffix '1x2' -- power-psi-mode-6.pdf power-omega-prob-6-panel.pdf
pdfcrop power-omega-prob-6-panel-1x2.pdf power-6.pdf
rm power-omega-prob-6-panel-1x2.pdf

pdfnup --nup '1x2' --suffix '1x2' -- power-num-excluded-4.pdf power-prob-exclusion-4-panel.pdf
pdfcrop power-prob-exclusion-4-panel-1x2.pdf power-exclusion-4.pdf
rm power-prob-exclusion-4-panel-1x2.pdf

pdfnup --nup '1x2' --suffix '1x2' -- power-num-excluded-6.pdf power-prob-exclusion-6-panel.pdf
pdfcrop power-prob-exclusion-6-panel-1x2.pdf power-exclusion-6.pdf
rm power-prob-exclusion-6-panel-1x2.pdf

pdfnup --nup '1x2' --suffix '1x2' -- power-accuracy-omega-median-6.pdf power-accuracy-omega-mode-glm-6-panel.pdf
pdfcrop power-accuracy-omega-mode-glm-6-panel-1x2.pdf power-accuracy-6.pdf
rm power-accuracy-omega-mode-glm-6-panel-1x2.pdf

pdfnup --nup '1x2' --suffix '1x2' -- power-accuracy-omega-median-4.pdf power-accuracy-omega-mode-glm-4-panel.pdf
pdfcrop power-accuracy-omega-mode-glm-4-panel-1x2.pdf power-accuracy-4.pdf
rm power-accuracy-omega-mode-glm-4-panel-1x2.pdf

