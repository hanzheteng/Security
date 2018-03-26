#include <stdio.h>
#include <stdlib.h>
#include <string.h>

unsigned long get_esp(void) {
   __asm__("movl %esp,%eax");
}

int main(int argc, char *argv[]) {
	char *ptr;
	long addr;
	if (argc < 3) {
		printf("Usage: %s <environment var> <target program name>\n", argv[0]);
		exit(0);
	} else {
		ptr = getenv(argv[1]); /* Get environment variable location */
		printf("%s originally will be at %p\n", argv[1], ptr);
		ptr += (strlen(argv[0]) - strlen(argv[2])) * 2; /* Adjust for program name */
		printf("%s will be at %p\n", argv[1], ptr);
		addr = get_esp();
		printf("esp address in main(): 0x%x\n", addr);
	}
}
