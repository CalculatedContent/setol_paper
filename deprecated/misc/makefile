clean: 
	rm -f *.aux *.log *.bbl *.blg
draft:
	make clean;
	pdflatex ww_prx
	bibtex ww_prx
	pdflatex ww_prx
	pdflatex ww_prx

TR:
	make clean;
	pdflatex ww_semiempirical_TRfmt
	bibtex ww_semiempirical_TRfmt
	pdflatex ww_semiempirical_TRfmt
	pdflatex ww_semiempirical_TRfmt

