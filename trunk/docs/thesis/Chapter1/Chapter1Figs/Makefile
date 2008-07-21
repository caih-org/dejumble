OBJFILES := $(patsubst %.dia,%.png,$(wildcard *.dia))

all: $(OBJFILES)

%.png: %.dia
	dia -e $@ $<

clean:
	rm *.png

