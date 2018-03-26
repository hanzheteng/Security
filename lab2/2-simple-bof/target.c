#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <common.h>

void jump_to_here() {
  read_flag();   // executable has a whole implement, here it is just a function name
}

void start() {
  char buffer[50];
  printf("Please input something...\n");
  fgets(buffer, 512, stdin);
}

int main(int argc, char** argv) {
  /* no warning */
  (void)jump_to_here;
  start();
  return 0;
}

/*
fgets() reads in at most one less than size characters 
  from stream and stores them into the buffer pointed to by s. 
  Reading stops after an EOF or a newline. If a newline is read, 
  it is stored into the buffer. A terminating null byte (aq\0aq) 
  is stored after the last character in the buffer.
*/
