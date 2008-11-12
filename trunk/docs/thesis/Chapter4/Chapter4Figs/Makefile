OBJFILES := $(patsubst %.dat,%.pdf,$(wildcard *.dat))

all: $(OBJFILES)

%.pdf: %.dat
	./prueba $< | gnuplot - > /dev/null

clean:
	rm *.pdf

