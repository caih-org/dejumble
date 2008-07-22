OBJFILES := $(patsubst %.gnu,%.pdf,$(wildcard *.gnu))

all: $(OBJFILES)

%.pdf: %.gnu
	gnuplot $<

clean:
	rm *.pdf

