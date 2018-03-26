#include <stdio.h>
#include <stdlib.h>
#include <string.h>

unsigned long get_esp(void) {
   __asm__("movl %esp,%eax");
}

int main(int argc, char *argv[]) {
	char *ptr;
	long addr;
	if (argc < 2) {
		printf("Usage: %s <environment var>\n", argv[0]);
		exit(0);
	} else {
		ptr = getenv(argv[1]); 
		printf("%s will be at %p\n", argv[1], ptr);
		addr = get_esp();
		printf("esp address in main(): 0x%x\n", addr);
	}
}
