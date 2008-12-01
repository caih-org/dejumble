OBJFILES := $(patsubst %.dia,%.pdf,$(wildcard *.dia)) $(patsubst %.dia,%.eps,$(wildcard *.dia))

all: $(OBJFILES)

%.eps: %.dia
	dia -e $@ $<

%.pdf: %.eps
	epstopdf $<

clean:
	rm *.pdf
	rm *.eps
