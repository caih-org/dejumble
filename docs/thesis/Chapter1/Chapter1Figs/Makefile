OBJFILES := $(patsubst %.dia,%.pdf,$(wildcard *.dia))

all: $(OBJFILES)

%.eps: %.dia
	dia -e $@ $<

%.pdf: %.eps
	epstopdf $<
	rm $< 

clean:
	rm *.pdf

