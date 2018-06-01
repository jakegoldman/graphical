test: lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py scripts/simple_anim.mdl

clean:
	rm *pyc *out parsetab.py

clear:m
	rm *pyc *out parsetab.py *ppm
