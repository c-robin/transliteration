name=report
pres=presentation

pres:
	pdflatex $(pres)
	bibtex $(pres)
	pdflatex $(pres)
	pdflatex $(pres)
report:
	pdflatex $(name)
	bibtex $(name)
	pdflatex $(name)
	pdflatex $(name)
clean2:
	rm -f $(pres).out $(pres).aux $(pres).log $(pres).bbl $(pres).blg $(pres).out $(pres).toc $(pres).nav $(pres).snm
clean:
	rm -f $(name).out $(name).aux $(name).log $(name).bbl $(name).blg $(name).out $(name).toc $(name).nav $(name).snm
