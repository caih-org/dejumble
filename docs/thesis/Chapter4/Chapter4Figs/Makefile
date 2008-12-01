OBJFILES := $(patsubst %.dat,%.pdf,$(wildcard *.dat)) $(patsubst %.dat,%.eps,$(wildcard *.dat))

all: $(OBJFILES)

%.eps: %.dat
	./prueba $< | gnuplot - > /dev/null

%.pdf: %.eps
	epstopdf $<

clean:
	rm *.pdf
	rm *.eps

