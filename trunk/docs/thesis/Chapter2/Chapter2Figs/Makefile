OBJFILES := $(patsubst %.eps,%.pdf,$(wildcard *.eps))

all: $(OBJFILES)

%.pdf: %.eps
	epstopdf $<

clean:
	rm *.pdf

