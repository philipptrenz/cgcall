all: cgcall
	
sipserv: cgcall.c
	cc -o $@ $< `pkg-config --cflags --libs libpjproject`
	
clean:
	rm -rf cgcall