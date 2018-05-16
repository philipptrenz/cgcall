all: cgcall
	
cgcall: src/cgcall.c
	cc -o $@ $< `pkg-config --cflags --libs libpjproject`
	
clean:
	rm -rf cgcall