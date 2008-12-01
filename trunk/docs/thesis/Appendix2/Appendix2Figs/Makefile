OBJFILES := $(patsubst %.png,%.pdf,$(wildcard *.png)) $(patsubst %.png,%.eps,$(wildcard *.png))

all: $(OBJFILES)

%.eps: %.png
	convert $< $@

%.pdf: %.eps
	epstopdf $<

clean:
	rm *.pdf
	rm *.eps
